from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1.brief import router as brief_router
from app.api.v1.articles import router as articles_router
from app.api.v1.feedback import router as feedback_router
from app.api.v1.history import router as history_router

app = FastAPI(title="Nifty Brief API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(brief_router, prefix="/api/v1")
app.include_router(articles_router, prefix="/api/v1")
app.include_router(feedback_router, prefix="/api/v1")
app.include_router(history_router, prefix="/api/v1")


@app.get("/health")
def health():
    return {"status": "ok", "version": "1.0.0"}
