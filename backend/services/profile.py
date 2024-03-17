from typing import Optional
from pydantic import BaseModel
from supabase import Client

from services.date import today


class Profile(BaseModel):
    id: str
    updated_at: str
    name: str
    avatar_url: Optional[str]


def create_profile(supabase: Client, id, name, avatar_url):
    response = (
        supabase.table("profiles")
            .insert({"id": id, "name": name, "avatar_url": avatar_url})
            .execute()
    )
    return response


def get_profile_by_id(supabase: Client, id: str):
    response = (
        supabase.table("profiles")
            .select("*")
            .eq("id", id)
            .execute()
    )
    if response.data:
        return Profile(**response.data[0])
    else:
        return None


def get_all_profiles(supabase: Client):
    response = (
        supabase.table("profiles")
            .select("*")
            .execute()
    )
    profiles = {}
    for profile in response.data:
        profiles[profile["id"]] = Profile(**profile)
    return profiles