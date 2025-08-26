import os
import asyncio
from typing import Optional

from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware

from database.db import jobs_collection
from database.insert import store_jobs
from database.debug import find_url_duplicates, delete_url_duplicates

# --- Config ---
REFRESH_SECONDS = int(os.getenv("CF_REFRESH_SECONDS", "60"))  # set CF_REFRESH_SECONDS=300 in prod
ALLOWED_ORIGINS = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

app = FastAPI(title="CareerForge API", version="0.2.1")

# CORS (dev-safe)
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "CareerForge Backend is running 🚀", "docs": "/docs"}

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/jobs")
def get_jobs(
    title: Optional[str] = Query(None),
    location: Optional[str] = Query(None),
    source: Optional[str] = Query(None),
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
):
    query = {}
    if title:
        query["title"] = {"$regex": title, "$options": "i"}
    if location:
        query["location"] = {"$regex": location, "$options": "i"}
    if source:
        query["source"] = source

    cursor = (
        jobs_collection.find(query, {"_id": 0})
        .sort("date_posted", -1)
        .skip(offset)
        .limit(limit)
    )
    items = list(cursor)
    total = jobs_collection.count_documents(query)
    return {"total": total, "limit": limit, "offset": offset, "items": items}

@app.post("/refresh")
async def refresh_jobs():
    """Manual refresh on demand."""
    await asyncio.to_thread(store_jobs)
    groups = await asyncio.to_thread(find_url_duplicates)
    if groups:
        await asyncio.to_thread(delete_url_duplicates, groups)
    return {"status": "refreshed", "deleted_duplicate_groups": len(groups) if groups else 0}

# ------------- Background auto-refresh loop -------------

async def auto_refresh_loop():
    while True:
        try:
            print("🔄 Auto-refresh: fetching jobs...")
            await asyncio.to_thread(store_jobs)
            groups = await asyncio.to_thread(find_url_duplicates)
            if groups:
                await asyncio.to_thread(delete_url_duplicates, groups)
        except Exception as e:
            print("⚠️ Auto-refresh failed:", e)
        await asyncio.sleep(REFRESH_SECONDS)

@app.on_event("startup")
async def startup_event():
    # Kick off the background loop (non-blocking)
    asyncio.create_task(auto_refresh_loop())
