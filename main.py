import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional

from database import db, create_document, get_documents

app = FastAPI(title="TechINDIA API", description="Backend for TechINDIA freelance marketplace")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"name": "TechINDIA", "status": "ok"}

@app.get("/test")
def test_database():
    response = {
        "backend": "✅ Running",
        "database": "❌ Not Available",
        "database_url": None,
        "database_name": None,
        "connection_status": "Not Connected",
        "collections": []
    }

    try:
        if db is not None:
            response["database"] = "✅ Available"
            response["database_url"] = "✅ Configured"
            response["database_name"] = db.name if hasattr(db, 'name') else "✅ Connected"
            response["connection_status"] = "Connected"

            try:
                collections = db.list_collection_names()
                response["collections"] = collections[:10]
                response["database"] = "✅ Connected & Working"
            except Exception as e:
                response["database"] = f"⚠️  Connected but Error: {str(e)[:50]}"
        else:
            response["database"] = "⚠️  Available but not initialized"

    except Exception as e:
        response["database"] = f"❌ Error: {str(e)[:50]}"

    import os
    response["database_url"] = "✅ Set" if os.getenv("DATABASE_URL") else "❌ Not Set"
    response["database_name"] = "✅ Set" if os.getenv("DATABASE_NAME") else "❌ Not Set"

    return response

# Schemas endpoint so the integrated DB viewer can read definitions
@app.get("/schema")
def get_schema_definitions():
    try:
        from schemas import User, Gig, Order, Review
        return {
            "user": User.model_json_schema(),
            "gig": Gig.model_json_schema(),
            "order": Order.model_json_schema(),
            "review": Review.model_json_schema(),
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Simple public listings for gigs (no auth for demo)
class GigQuery(BaseModel):
    q: Optional[str] = None
    category: Optional[str] = None
    limit: int = 20

@app.get("/gigs")
def list_gigs(q: Optional[str] = None, category: Optional[str] = None, limit: int = 20):
    filter_dict = {}
    if category:
        filter_dict["category"] = category
    if q:
        # basic contains search on title via regex
        filter_dict["title"] = {"$regex": q, "$options": "i"}

    gigs = get_documents("gig", filter_dict, limit)
    # Convert ObjectId to string safely
    from bson import ObjectId
    for g in gigs:
        if isinstance(g.get("_id"), ObjectId):
            g["id"] = str(g.pop("_id"))
    return gigs

class CreateGig(BaseModel):
    title: str
    description: str
    category: str
    price: float
    seller_id: str
    tags: Optional[List[str]] = []
    cover_image: Optional[str] = None

@app.post("/gigs")
def create_gig(payload: CreateGig):
    from schemas import Gig
    gig = Gig(**payload.model_dump())
    inserted_id = create_document("gig", gig)
    return {"id": inserted_id}

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
