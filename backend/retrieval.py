"""Validated local retrieval. Model construction happens once, never per request."""
import hashlib
import json
import logging
import os
import threading
from pathlib import Path
from typing import Literal

import numpy as np
from pydantic import BaseModel, ConfigDict, Field, StrictStr, field_validator
from sklearn.feature_extraction.text import TfidfVectorizer

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / 'case-study-1-support-ticket-similarity/starter_kit/data'
MODEL_ID = 'sentence-transformers/all-MiniLM-L6-v2'
MODEL_REVISION = '1110a243fdf4706b3f48f1d95db1a4f5529b4d41'
PREPROCESSING = 'subject-description-v1'
# Evidence gates are finalized using development examples only; see evaluation/README.md.
KEYWORD_THRESHOLD = 0.25
SEMANTIC_THRESHOLD = 0.70
Mode = Literal['keyword', 'semantic', 'hybrid']


class Ticket(BaseModel):
    model_config = ConfigDict(strict=True, extra='forbid')
    ticket_id: str
    subject: str
    description: str
    resolution_notes: str
    category: str
    tags: list[str]
    created_at: str
    status: str

    @field_validator('ticket_id', 'subject', 'description', 'resolution_notes', 'category', 'created_at', 'status')
    @classmethod
    def nonblank(cls, value):
        if not value.strip():
            raise ValueError('must not be blank')
        return value


class SearchRequest(BaseModel):
    subject: StrictStr = Field(min_length=1, max_length=300)
    description: StrictStr = Field(min_length=1, max_length=10000)
    mode: Mode = 'hybrid'
    top_k: int = Field(default=3, ge=1, le=10, strict=True)

    @field_validator('subject', 'description')
    @classmethod
    def trim(cls, value):
        if not value.strip():
            raise ValueError('must not be blank')
        return value.strip()


class Match(BaseModel):
    ticket: Ticket
    keyword_score: float
    semantic_score: float | None
    fusion_score: float | None


class SearchResponse(BaseModel):
    outcome: Literal['matches', 'no_reliable_match']
    requested_mode: Mode
    active_mode: Mode
    degraded: bool
    matches: list[Match]
    evidence_note: str


def load_tickets(path: Path) -> list[Ticket]:
    try:
        raw = json.loads(path.read_text(encoding='utf-8'))
        if not isinstance(raw, dict) or not isinstance(raw.get('tickets'), list) or not raw['tickets']:
            raise ValueError('expected nonempty tickets array')
        tickets = [Ticket.model_validate(row) for row in raw['tickets']]
        if len({t.ticket_id for t in tickets}) != len(tickets):
            raise ValueError('duplicate ticket_id')
        return tickets
    except (ValueError, OSError) as exc:
        raise ValueError(f'Invalid historical dataset {path.name}: {exc}') from exc


def cache_key(dataset_bytes: bytes, model_id=MODEL_ID, revision=MODEL_REVISION, preprocessing=PREPROCESSING):
    return hashlib.sha256(dataset_bytes + json.dumps([model_id, revision, preprocessing]).encode()).hexdigest()


def stable_order(scores, tickets):
    return sorted(range(len(tickets)), key=lambda i: (-float(scores[i]), tickets[i].ticket_id))


def reciprocal_rank_fusion(keyword, semantic, tickets):
    scores = np.zeros(len(tickets))
    for component in (keyword, semantic):
        if component is None:
            continue
        ranking = [i for i in stable_order(component, tickets) if component[i] > 0]
        for rank, i in enumerate(ranking, 1):
            scores[i] += 1 / (60 + rank)
    return scores


class Retriever:
    def __init__(self, path=DATA / 'tickets.json', semantic=True, model=None, cache_dir=None):
        self.tickets = load_tickets(path)
        self.texts = [f'{t.subject}\n{t.description}' for t in self.tickets]
        self.vectorizer = TfidfVectorizer(lowercase=True, ngram_range=(1, 2), sublinear_tf=True,
            token_pattern=r'(?u)\b[\w][\w.\-]*\b')
        self.matrix = self.vectorizer.fit_transform(self.texts)
        self.model = None
        self.embeddings = None
        self.semantic_failure = None
        self.lock = threading.Lock()
        if semantic:
            try:
                if model is None:
                    import torch
                    from sentence_transformers import SentenceTransformer
                    torch.set_num_threads(4)
                    model = SentenceTransformer(MODEL_ID, revision=MODEL_REVISION, device='cpu',
                        local_files_only=os.getenv('SOLARI_OFFLINE') == '1',
                        cache_folder=str(ROOT / '.cache/models'), trust_remote_code=False)
                    model.max_seq_length = 256
                self.model = model
                folder = Path(cache_dir or ROOT / '.cache/embeddings')
                folder.mkdir(parents=True, exist_ok=True)
                cache = folder / (cache_key(path.read_bytes()) + '.npy')
                try:
                    embeddings = np.load(cache, allow_pickle=False)
                    dimension = model.get_sentence_embedding_dimension() if hasattr(model, 'get_sentence_embedding_dimension') else None
                    if embeddings.ndim != 2 or embeddings.shape[0] != len(self.tickets) or (dimension and embeddings.shape[1] != dimension) or not np.isfinite(embeddings).all():
                        raise ValueError('invalid embedding shape/values')
                    if not np.allclose(np.linalg.norm(embeddings, axis=1), 1, atol=1e-4):
                        raise ValueError('unnormalized embeddings')
                except (OSError, ValueError, TypeError):
                    embeddings = model.encode(self.texts, normalize_embeddings=True, convert_to_numpy=True)
                    temporary = cache.with_suffix('.tmp')
                    with temporary.open('wb') as stream:
                        np.save(stream, embeddings, allow_pickle=False)
                    temporary.replace(cache)
                self.embeddings = embeddings
            except Exception:
                # Do not expose local paths, ticket text, or network details through the API.
                logging.getLogger(__name__).warning('Semantic initialization failed; keyword capability remains available')
                self.model = None
                self.semantic_failure = 'Semantic model unavailable. Pre-download model and restart.'

    @property
    def capabilities(self):
        return ['keyword', 'semantic', 'hybrid'] if self.model is not None else ['keyword']

    def search(self, request: SearchRequest) -> SearchResponse:
        if request.mode != 'keyword' and self.model is None:
            raise RuntimeError('Requested retrieval capability unavailable')
        text = f'{request.subject}\n{request.description}'
        keyword = (self.matrix @ self.vectorizer.transform([text]).T).toarray().ravel()
        semantic = None
        if request.mode != 'keyword':
            with self.lock:
                query = self.model.encode([text], normalize_embeddings=True, convert_to_numpy=True)
            semantic = (self.embeddings @ query[0]).clip(-1, 1)
        fusion = reciprocal_rank_fusion(keyword, semantic, self.tickets) if request.mode == 'hybrid' else None
        scores = keyword if request.mode == 'keyword' else semantic if request.mode == 'semantic' else fusion
        # Gate individual candidates, so weak tail matches are not displayed as evidence.
        def reliable(i):
            if request.mode == 'keyword':
                return keyword[i] >= KEYWORD_THRESHOLD
            if request.mode == 'semantic':
                return semantic[i] >= SEMANTIC_THRESHOLD
            return semantic[i] >= SEMANTIC_THRESHOLD or keyword[i] >= KEYWORD_THRESHOLD
        ranking = [i for i in stable_order(scores, self.tickets) if reliable(i)][:request.top_k]
        return SearchResponse(outcome='matches' if ranking else 'no_reliable_match',
            requested_mode=request.mode, active_mode=request.mode, degraded=self.model is None,
            matches=[Match(ticket=self.tickets[i], keyword_score=float(keyword[i]),
                semantic_score=float(semantic[i]) if semantic is not None else None,
                fusion_score=float(fusion[i]) if fusion is not None else None) for i in ranking],
            evidence_note='Historical similarity is evidence for review, not a probability or a new resolution.')
