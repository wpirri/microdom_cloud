from fastapi import FastAPI
import asyncio
from .worker import worker_loop

app = FastAPI(title="microdom_cloud")

@app.get("/health")
async def health():
    return {"status": "ok", "service": "microdom_cloud"}

@app.on_event("startup")
async def startup_event():
    asyncio.create_task(worker_loop())
    