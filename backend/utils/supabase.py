import os
from dotenv import load_dotenv
from supabase import create_client

load_dotenv()

def init_supabase():
    return create_client(
        os.environ.get("SUPABASE_URL"), os.environ.get("SUPABASE_KEY")
    )