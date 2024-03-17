from typing import Optional
from fastapi import APIRouter, Request
from pydantic import BaseModel
from services.profile import create_profile, get_profile_by_id


profile_router = APIRouter(
    prefix="/profile",
    tags=["profile"],
)

class CreateProfileRequest(BaseModel):
    name: str
    avatar_url: Optional[str]

@profile_router.post("/{uid}")
async def create_profile_handler(request: Request, uid: str, create_profile_request: CreateProfileRequest):
    response = create_profile(request.app.supabase, uid, create_profile_request.name, create_profile_request.avatar_url)
    return response

@profile_router.get("/{uid}")
async def get_profile_handler(request: Request, uid: str):
    response = get_profile_by_id(request.app.supabase, uid)
    return response