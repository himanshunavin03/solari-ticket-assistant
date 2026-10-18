"""Pre-download and verify the exact pinned model; errors fail this command."""
from backend.retrieval import MODEL_ID, MODEL_REVISION, ROOT
from sentence_transformers import SentenceTransformer
import os
import torch

torch.set_num_threads(4)
model = SentenceTransformer(MODEL_ID, revision=MODEL_REVISION, device='cpu',
    cache_folder=str(ROOT / '.cache/models'), trust_remote_code=False,
    local_files_only=os.getenv('SOLARI_OFFLINE') == '1')
embedding = model.encode(['Model download verification'], normalize_embeddings=True)
print(f'{MODEL_ID}@{MODEL_REVISION}: verified {embedding.shape}')
