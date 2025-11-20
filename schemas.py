"""
Database Schemas for TechINDIA (Freelance Marketplace)

Each Pydantic model corresponds to a MongoDB collection with the
collection name equal to the lowercase of the class name.

Examples:
- User -> "user"
- Gig -> "gig"
- Order -> "order"
- Review -> "review"
"""

from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List

class User(BaseModel):
    name: str = Field(..., description="Full name")
    email: EmailStr = Field(..., description="Email address")
    role: str = Field(..., description="buyer or seller")
    bio: Optional[str] = Field(None, description="Short bio")
    skills: List[str] = Field(default_factory=list, description="Skills list")
    rating: float = Field(default=0, ge=0, le=5, description="Average rating")
    avatar_url: Optional[str] = Field(None, description="Profile image URL")

class Gig(BaseModel):
    title: str = Field(..., description="Gig title")
    description: str = Field(..., description="Detailed description of the service")
    category: str = Field(..., description="Category of the service, e.g., Design, Web, AI")
    price: float = Field(..., ge=0, description="Base price")
    seller_id: str = Field(..., description="User id of the seller")
    tags: List[str] = Field(default_factory=list, description="Tags for search")
    cover_image: Optional[str] = Field(None, description="Cover image URL")
    rating: float = Field(default=0, ge=0, le=5, description="Average rating")
    reviews_count: int = Field(default=0, ge=0, description="Number of reviews")

class Order(BaseModel):
    gig_id: str = Field(..., description="Gig id")
    buyer_id: str = Field(..., description="User id of the buyer")
    seller_id: str = Field(..., description="User id of the seller")
    status: str = Field("pending", description="pending, in_progress, delivered, completed, cancelled")
    requirements: Optional[str] = Field(None, description="Buyer requirements")

class Review(BaseModel):
    gig_id: str = Field(..., description="Gig id")
    user_id: str = Field(..., description="Reviewer user id")
    rating: int = Field(..., ge=1, le=5, description="Rating 1-5")
    comment: Optional[str] = Field(None, description="Optional feedback")
