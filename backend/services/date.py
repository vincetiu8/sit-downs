from datetime import datetime
from typing import Optional
from pydantic import BaseModel
from supabase import Client

class Date(BaseModel):
    id: int
    date: str
    uid: str
    summary: str
    one_sentence_summary: str
    one_sentence_summary_second_person: Optional[str]

def today():
    return datetime.now().strftime("%Y-%m-%d")

def create_date(supabase: Client, date: str, uid: str, summary: str, one_sentence_summary: str, one_sentence_summary_second_person: str):
    response = (
        supabase.table("dates")
            .insert({"date": date, "uid": uid, "summary": summary, "one_sentence_summary": one_sentence_summary, "one_sentence_summary_second_person": one_sentence_summary_second_person})
            .execute()
    )
    return Date(**response.data[0])

def create_today_by_user(supabase: Client, uid: str, summary: str, one_sentence_summary: str, one_sentence_summary_second_person: str):
    return create_date(supabase, today(), uid, summary, one_sentence_summary, one_sentence_summary_second_person)

def get_date_by_id(supabase: Client, id: str):
    response = (
        supabase.table("dates")
            .select("*")
            .eq("id", id)
            .execute()
    )
    if response.data:
        return Date(**response.data[0])
    else:
        return None
    
def get_today_by_user(supabase: Client, uid: str):
    response = (
        supabase.table("dates")
            .select("*")
            .eq("date", today())
            .eq("uid", uid)
            .execute()
    )
    if response.data:
        return Date(**response.data[0])
    else:
        return None
    
def get_all_today(supabase: Client):
    response = (
        supabase.table("dates")
            .select("*")
            .eq("date", today())
            .execute()
    )
    return [Date(**date) for date in response.data]
    
def update_date_summary(supabase: Client, id: str, summary: str, one_sentence_summary: str, one_sentence_summary_second_person: str):
    response = (
        supabase.table("dates")
            .update({"summary": summary, "one_sentence_summary": one_sentence_summary, "one_sentence_summary_second_person": one_sentence_summary_second_person})
            .eq("id", id)
            .execute()
    )
    return response

def delete_date(supabase: Client, id: str):
    response = (
        supabase.table("dates")
            .delete()
            .eq("id", id)
            .execute()
    )
    return response
