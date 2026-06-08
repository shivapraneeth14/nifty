from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1.brief import router as brief_router
from app.api.v1.articles import router as articles_router
from app.api.v1.feedback import router as feedback_router
from app.api.v1.history import router as history_router
from app.api.v1.accuracy import router as accuracy_router
from app.api.v1.global_market import router as global_market_router
from app.api.v1.meter import router as meter_router
from app.api.v1.option_chain import router as option_chain_router
from app.api.v1.debrief import router as debrief_router
from app.api.v1.fii import router as fii_router
from app.api.v1.notifications import router as notifications_router

app = FastAPI(
    title="Nifty Brief API",
    version="2.0.0",
    description="Pre-market trading brief for Nifty 50 / Bank Nifty options traders",
    docs_url="/docs",
)

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
app.include_router(accuracy_router, prefix="/api/v1")
app.include_router(global_market_router, prefix="/api/v1")
app.include_router(meter_router, prefix="/api/v1")
app.include_router(option_chain_router, prefix="/api/v1")
app.include_router(debrief_router, prefix="/api/v1")
app.include_router(fii_router, prefix="/api/v1")
app.include_router(notifications_router, prefix="/api/v1")


@app.get("/health")
def health():
    return {"status": "ok", "version": "2.0.0"}
