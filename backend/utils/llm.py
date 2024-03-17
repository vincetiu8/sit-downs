from openai import OpenAI
import os
from dotenv import load_dotenv
from transformers import AutoTokenizer
from utils.prompts import find_others_system_prompt, find_others_user_prompt

load_dotenv()


def init_llm():
    model_id = os.environ["BASE_TEN_MODEL_ID"]
    return OpenAI(
        api_key=os.environ["BASE_TEN_API_KEY"],
        base_url=f"https://bridge.baseten.co/{model_id}/v1",
    )


def cut(webSequence):
    tokenizer = AutoTokenizer.from_pretrained("mistralai/Mixtral-8x7B-v0.1")
    tokenized = tokenizer(webSequence, return_tensors="pt")
    if len(tokenized.input_ids[0]) < 4000:
        return webSequence
    return tokenizer.decode(tokenized.input_ids[0][:4000])


def summarize_webpage(llm: OpenAI, title, url, body):
    webSequence = f"TITLE:{title},URL:{url},BODY:{body}"
    webSequence = cut(webSequence)
    res = llm.chat.completions.create(
        model="mistral-7b",
        messages=[
            {
                "role": "system",
                "content": "Summarize what the following web page created by this title, URL and DOM does in a short, concise paragraph of LESS THAN 100 WORDS. DO NOT embed URLs or links into the paragraph.",
            },
            {"role": "user", "content": webSequence},
        ],
        temperature=0.6,
        max_tokens=512,
    )
    arr = res.choices[0].message.content.split("[/INST]")
    if len(arr) < 1:
        raise ValueError("No output")
    return arr[1]


def summarize_date(llm: OpenAI, name: str, summaries: list[str]):
    allSummaries = cut("`".join(summaries))
    res = llm.chat.completions.create(
        model="mistral-7b",
        messages=[
            {
                "role": "system",
                "content": f"From the following summaries of web pages a user '{name}' has been browsing, infer what they have been working on. This paragraph should be LESS THAN 150 words. DO NOT embed URLs or links into the paragraph. Do not give an introduction. Do not use pronouns or an explicit subject. Be in present-continuous tense. Start Each summary is separated by a `",
            },
            {"role": "user", "content": allSummaries},
        ],
        temperature=0.6,
        max_tokens=512,
    )
    arr = res.choices[0].message.content.split("[/INST]")
    if len(arr) < 1:
        raise ValueError("No output")
    return arr[1]


def summarize_summary(llm: OpenAI, name: str, summary: str):
    res = llm.chat.completions.create(
        model="mistral-7b",
        messages=[
            {
                "role": "system",
                "content": f"Summarize the following paragraph into one concise sentence with less than 10 words in third-person present-continuous tense with active voice using the given name f{name} in the original paragraph. Example: {name} is working on a project.",
            },
            {"role": "user", "content": summary},
        ],
        temperature=0.6,
        max_tokens=512,
    )
    arr = res.choices[0].message.content.split("[/INST]")
    if len(arr) < 1:
        raise ValueError("No output")
    clean_string = arr[1].replace("\n", "").replace("\t", "").replace("  ", " ").strip()

    res = llm.chat.completions.create(
        model="mistral-7b",
        messages=[
            {
                "role": "system",
                "content": f"Summarize the following paragraph into one concise sentence with less than 10 words in second-person present-continuous tense with active voice. Example: You are working on a project.",
            },
            {"role": "user", "content": summary},
        ],
        temperature=0.6,
        max_tokens=512,
    )
    arr = res.choices[0].message.content.split("[/INST]")
    if len(arr) < 1:
        raise ValueError("No output")
    clean_string_2 = arr[1].replace("\n", "").replace("\t", "").replace("  ", " ").strip()

    return [clean_string, clean_string_2]


def other_k_people(llm: OpenAI, target, neighbors):
    res = llm.chat.completions.create(
        model="mistral-7b",
        messages=[
            {"role": "system", "content": find_others_system_prompt()},
            {
                "role": "user",
                "content": find_others_user_prompt(target, cut(neighbors)),
            },
        ],
        temperature=0.6,
        max_tokens=512,
    )
    arr = res.choices[0].message.content.split("[/INST]")
    if len(arr) < 1:
        raise ValueError("No output")

    return arr[1]


# llm = init_llm()
# target = """{uid: fb67383f-12de-4c07-a423-ed7faad8b7a3, summary:  The user has been working on projects related to
#             artificial intelligence (AI) and data analysis, primarily using tools and platforms provided by Nomic.ai.
#             They have explored Nomic's AI tools, Atlas and GPT4All, which focus on data exploration, model quality enhancement,
#             and accessible AI. The user has also utilized Nomic Atlas for structuring and gaining insights from unstructured data,
#               and has recently learned about the release of Nomic Embed, an open-source text embedding model. Additionally, the user
#               has been looking into the deepscatter project by nomic-ai, which is a library for creating zoomable, animated scatterplots
#               in the browser that can handle over a billion data points. They have accessed the GitHub repositories for both the deepscatter
#               project and Nomic AI's organization page, suggesting an interest in contributing to these projects or understanding their functionality in greater depth.}"""


# neighbors = """{uid: fb67383f-12de-4c07-a423-ed7faad8b7a3, summary:   Based on the summaries, the user has been working on researching the Wharton MBA program at the University of Pennsylvania. They have looked up general information about the program through Google search, as well as specific details about the 2-year MBA program and the admissions process from the Wharton School's website. It appears they are considering applying to the program and gathering information to support their application.},
#                 {uid:179a69ab-5715-457e-8fc0-86533ea165bd, summary:  Based on the summaries, 'Prince' has been working on a project related to Goldman Sachs' Menlo Park location. They have been searching for information about the company's offices, people, and job opportunities in that location. They have visited Google's homepage and used it to search for relevant terms such as "Goldman Sachs Menlo Park" and "how to get in to Goldman Menlo Park." They have also browsed job listings on Indeed.com for positions at Goldman Sachs in Menlo Park, CA. It appears they are considering a career move to Goldman Sachs or are conducting research for another purpose related to the company's Menlo Park location. }"""
# print(other_k_people(llm, target, neighbors))
