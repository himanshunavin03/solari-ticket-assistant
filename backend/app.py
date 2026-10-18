import json
import os
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from backend.retrieval import DATA, MODEL_ID, MODEL_REVISION, Retriever, SearchRequest, SearchResponse


class Health(BaseModel):
    status: str
    capabilities: list[str]
    ticket_count: int
    model_id: str
    model_revision: str
    message: str | None


def create_app(retriever=None):
    @asynccontextmanager
    async def lifespan(app):
        app.state.retriever = retriever or Retriever(semantic=os.getenv('SOLARI_KEYWORD_ONLY') != '1')
        yield

    app = FastAPI(title='Solari Ticket Assistant', lifespan=lifespan)
    app.add_middleware(CORSMiddleware, allow_origins=['http://localhost:4200', 'http://127.0.0.1:4200'],
        allow_methods=['GET', 'POST'], allow_headers=['Content-Type'])

    @app.exception_handler(RequestValidationError)
    async def validation_error(request, exc):
        return JSONResponse(status_code=422, content={'error': {'code': 'invalid_input',
            'message': 'Check subject, description, mode and top_k (1–10).',
            'fields': sorted({str(e['loc'][-1]) for e in exc.errors()})}})

    @app.exception_handler(Exception)
    async def unexpected_error(request, exc):
        return JSONResponse(status_code=503, content={'error': {'code': 'service_unavailable',
            'message': 'Search service unavailable. Retry or check readiness.'}})

    @app.get('/api/health', response_model=Health)
    def health(request: Request):
        r = request.app.state.retriever
        return Health(status='ready' if r.model is not None else 'degraded', capabilities=r.capabilities,
            ticket_count=len(r.tickets), model_id=MODEL_ID, model_revision=MODEL_REVISION,
            message=r.semantic_failure)

    @app.get('/api/examples')
    def examples():
        return json.loads((DATA / 'new_tickets_example.json').read_text(encoding='utf-8'))

    @app.post('/api/search', response_model=SearchResponse)
    def search(body: SearchRequest, request: Request):
        r = request.app.state.retriever
        if body.mode not in r.capabilities:
            return JSONResponse(status_code=503, content={'error': {'code': 'capability_unavailable',
                'message': 'Semantic retrieval unavailable. Select Keyword explicitly or restart after model download.'}})
        return r.search(body)

    return app


app = create_app()
