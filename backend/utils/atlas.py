from nomic.atlas import AtlasDataset
from nomic import embed
import numpy as np
from pydantic import BaseModel
from utils.supabase import init_supabase

dataset = AtlasDataset(
    "sit-downs-pages",
    unique_id_field="id",
)

class DatasetPage(BaseModel):
    id: int
    title: str
    url: str
    body: str
    summary: str
    date: str
    user_name: str


def add_page(page: DatasetPage):
    page_json = {
        "id": page.id,
        "title": page.title,
        "url": page.url,
        "body": page.body,
        "summary": page.summary,
        "date": page.date,
        "user_name": page.user_name
    }
    dataset.add_data(
        data=[page_json]
    )


def generate_map():
    map = dataset.create_index(
        indexed_field="summary",
        topic_model=True,
        duplicate_detection=True,
        projection=None,
        embedding_model="NomicEmbed"
    )
    return map


def get_k_neighbors(summary: str, other_summaries: list[str]):
    embeddings = embed.text(
        texts=[summary] + other_summaries,
        model="nomic-embed-text-v1.5",
        task_type="search_document",
    )["embeddings"]

    return np.argsort(np.dot(embeddings[1:], embeddings[0]))[::-1]


def get_all_supabase():
    s = init_supabase()
    response = s.table('pages').select("*").execute()
    for i, r in enumerate(response.data):
        add_page(DatasetPage(
            id = i,
            title = r['title'],
            url = r["url"],
            body = r['body'],
            summary = r['summary'],
            date = r['timestamp'],
            user_name = str(r['id'])
        ))
