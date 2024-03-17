import os
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from utils.atlas import generate_map

from routes.router import router
from utils.llm import init_llm
from utils.supabase import init_supabase

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.llm = init_llm()
app.supabase = init_supabase()

app.include_router(router)
