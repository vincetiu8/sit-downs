from typing import Optional
from pydantic import BaseModel
from supabase import Client

from services.date import get_today_by_user, today


class Page(BaseModel):
    id: int
    timestamp: str
    title: str
    url: str
    body: str
    summary: str
    date_id: int
    times_visited: Optional[int]


def create_page(supabase: Client, title, url, body, summary, date_id):
    response = (
        supabase.table("pages")
            .insert({"title": title, "url": url, "body": body, "summary": summary, "date_id": date_id, "times_visited": 1})
            .execute()
    )
    return Page(**response.data[0])


def get_page_by_id(supabase: Client, id: str):
    response = (
        supabase.table("pages")
            .select("*")
            .eq("id", id)
            .execute()
    )
    if response.data:
        return Page(**response.data[0])
    else:
        return None
    

def get_pages_by_date_id(supabase: Client, date_id: str):
    response = (
        supabase.table("pages")
            .select("*")
            .eq("date_id", date_id)
            .execute()
    )
    if response.data:
        return [Page(**page) for page in response.data]
    else:
        return None
    
def get_pages_today_by_user(supabase: Client, uid: str):
    response = (
        supabase.table("pages")
            .select("*")
            .eq("date_id", get_today_by_user(supabase, uid).id)
            .execute()
    )
    if response.data:
        for page in response.data:
            if "times_visited" not in page or not page["times_visited"]:
                page["times_visited"] = 1
        return [Page(**page) for page in response.data]
    else:
        return []
    
def get_top_pages_today_by_user(supabase: Client, uid: str, limit: int):
    response = get_pages_today_by_user(supabase, uid)

    if response:
        return sorted(response, key=lambda x: x.times_visited if x.times_visited else 1, reverse=True)[:limit]
    else:
        return []
    
def get_all_top_pages_today(supabase: Client, limit: int):
    response = (
        supabase.table("pages")
            .select("*")
            .execute()
    )
    for page in response.data:
        if "times_visited" not in page or not page["times_visited"]:
            page["times_visited"] = 1
    pages = [Page(**page) for page in response.data]
    sorted_pages = sorted(pages, key=lambda x: x.times_visited, reverse=True)
    users = {}
    for sorted_page in sorted_pages:
        if sorted_page.date_id not in users:
            users[sorted_page.date_id] = [sorted_page]
        elif len(users[sorted_page.date_id]) < limit:
            users[sorted_page.date_id].append(sorted_page)
    return users
    
def increment_page_times_visited(supabase: Client, uid: str, url: str):
    response = (
        supabase.table("pages")
            .select("*")
            .eq("url", url)
            .eq("date_id", get_today_by_user(supabase, uid).id)
            .execute()
    )

    if response.data:
        page = Page(**response.data[0])
        response = (
            supabase.table("pages")
                .update({"times_visited": page.times_visited + 1 if page.times_visited else 2})
                .eq("id", page.id)
                .execute()
        )

        return page
    
    return None