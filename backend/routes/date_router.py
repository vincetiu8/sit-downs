from fastapi import APIRouter, Request
from utils.atlas import get_k_neighbors
from services.page import get_all_top_pages_today, get_top_pages_today_by_user
from services.profile import get_all_profiles, get_profile_by_id

from services.date import create_today_by_user, get_all_today, get_today_by_user
from services.page import get_pages_by_date_id


date_router = APIRouter(
    prefix="/date",
    tags=["date"],
)


@date_router.get("/today/{uid}")
async def get_today_handler(request: Request, uid: str):
    """
    Gets all tasks for a given user today.
    """

    result = get_today_by_user(request.app.supabase, uid)
    if not result:
        profile = get_profile_by_id(request.app.supabase, uid)
        result = create_today_by_user(request.app.supabase, uid, "No activity so far.", f"{profile.name} has not done anything so far.", "You have not done anything so far. Get to work!")
    
    return {
        "name": get_profile_by_id(request.app.supabase, uid).name,
        "date": result.date,
        "summary": result.summary,
        "one_sentence_summary": result.one_sentence_summary,
        "one_sentence_summary_second_person": result.one_sentence_summary_second_person,
        "links": [[page.title, page.url, page.times_visited, page.summary] for page in get_top_pages_today_by_user(request.app.supabase, uid, 5)],
    }


@date_router.get("/today/relevant/{uid}")
async def get_relevant_coworkers_today_handler(request: Request, uid: str):
    """
    Gets top coworkers working on the most relevant tasks for a given user today.
    """

    # for now, we just return the first 3 coworkers

    results = get_all_today(request.app.supabase)
    my_summary = [result.summary for result in filter(lambda result: result.uid == uid, results)]

    pages = get_all_top_pages_today(request.app.supabase, 5)
    profiles = get_all_profiles(request.app.supabase)

    if len(my_summary) == 0:
        ordered_results = results

        return [{
            "name": profiles[result.uid].name,
            "date": result.date,
            "summary": result.summary,
            "one_sentence_summary": result.one_sentence_summary,
            "one_sentence_summary_second_person": result.one_sentence_summary_second_person,
            "links": [[page.title, page.url, page.times_visited, page.summary] for page in (pages[result.id] if result.id in pages else [])],
        } for result in ordered_results]
    my_summary = my_summary[0]


    other_results = list(filter(lambda result: result.uid != uid, results))
    other_summaries = [result.summary for result in other_results]
    order = get_k_neighbors(my_summary, other_summaries)
    ordered_results = [other_results[i] for i in order]

    return [{
        "name": profiles[result.uid].name,
        "date": result.date,
        "summary": result.summary,
        "one_sentence_summary": result.one_sentence_summary,
        "one_sentence_summary_second_person": result.one_sentence_summary_second_person,
        "links": [[page.title, page.url, page.times_visited, page.summary] for page in (pages[result.id] if result.id in pages else [])],
    } for result in ordered_results]


@date_router.get("/profile/{id}")
async def get_profile(request: Request, id:str):
    return get_pages_by_date_id(request.app.supabase, id)
