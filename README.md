# Sit Downs

No more standups.

### Overview

We don't like useless meetings, and wanted to design a tool that streamlined the process of communication between team members while retaining and improving our ability to identify areas of potential collaboration. For this, we built Sit-Downs, a Chrome Extension that tracks your browsing history, infers what you are working on and identifies other co-workers working in similar areas.

Through Sit-Downs, you can:
- Get automatic summaries for your day’s work
- See most visited websites
- See your teammates’ work
- Smart search for related updates to streamline collaboration
- Visualize team-wide progress

Sit-Downs is a universal and effortless communication tool for all companies, teams and groups.

### Tech Stack

Frontend: React, Plasmo, Tailwind CSS
Backend: Nomic, Baseten, FastAPI, Supabase
Models: Mixtral 8x7B (on Baseten A100s), Nomic Embeddings

##### Tech Pipeline

1. Chrome extension scrapes DOM + metadata from browsed websites
2. Mistral DOM Analyzer Agent processes website data into english description
3. Mistral Summarizer Agent infers tasks and acomplishments through analyzing website descriptions
4. Nomic Embeddings Model creates vector embeddings of each summary
5. Vector Similarity Search used on vector embeddings to find teammates working on similar tasks
6. Supabase hosts all data
7. Frontend displays results to end-user and team

### Execution

1. Run backend server
    1. `cd backend`
    2. `uvicorn main:app --reload`
2. Run chrome extension
    1. `cd extension`
    2. `pnpm dev`
    3. Go to chrome extensions, enable dev tools
    4. Load unpacked extension, select build folder in extensions
