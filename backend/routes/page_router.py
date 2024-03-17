from fastapi import APIRouter, Request
from pydantic import BaseModel
from utils.atlas import DatasetPage
from services.date import create_today_by_user, get_today_by_user, update_date_summary

from services.page import create_page, get_pages_by_date_id, get_pages_today_by_user, increment_page_times_visited
from utils.llm import summarize_date, summarize_webpage, summarize_summary
from utils.atlas import add_page, generate_map
from services.profile import get_profile_by_id


page_router = APIRouter(
    prefix="/page",
    tags=["page"],
)

@page_router.get("/today/{uid}")
async def get_today_page_handler(request: Request, uid: int):
    get_pages_today_by_user(request.app.supabase, uid)


def update_date_summary_wrapper(request: Request, id: str, name: str):
    pages = get_pages_by_date_id(request.app.supabase, id)
    date_summary = summarize_date(request.app.llm, name, [page.summary for page in pages])
    [one_sentence_summary, one_sentence_summary_second_person] = summarize_summary(request.app.llm, name, date_summary)
    update_date_summary(request.app.supabase, id, date_summary, one_sentence_summary, one_sentence_summary_second_person)

class ProcessPageRequest(BaseModel):
    title: str
    url: str
    body: str


@page_router.post("/{uid}")
async def process_page_handler(request: Request, uid: str, input: ProcessPageRequest):
    today = get_today_by_user(request.app.supabase, uid)
    profile = get_profile_by_id(request.app.supabase, uid)

    if not today:
        create_today_by_user(request.app.supabase, uid, "No activity so far.", f"{profile.name} has no activity so far.", "You have no activity so far.")
        today = get_today_by_user(request.app.supabase, uid)

    result = increment_page_times_visited(request.app.supabase, uid, input.url)
    if result:
        return result

    page_summary = summarize_webpage(request.app.llm, input.title, input.url, input.body)

    page = create_page(request.app.supabase, input.title, input.url, input.body, page_summary, today.id)

    profile = get_profile_by_id(request.app.supabase, uid)

    update_date_summary_wrapper(request, today.id, profile.name) 

    user = get_profile_by_id(request.app.supabase, uid)

    datasetPage = DatasetPage(
        id = page.id,
        title = page.title,
        url = page.url,
        body = page.body,
        summary = page.summary,
        date = today.date,
        user_name = user.name
    )

    add_page(datasetPage)

    return page


@page_router.get("/generate")
async def generate_nomic(request: Request):
    return generate_map()
