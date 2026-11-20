# Semantic Search Engine for Technical Articles
Keyword + Semantic (TF-IDF) hybrid search. Score = 0.4 * keyword + 0.6 * semantic (cosine).
## Run Backend (Terminal 1)
cd backend; uvicorn app.main:app --port 8002 --reload
## Run Frontend (Terminal 2)
cd frontend; npm run dev
# http://localhost:5174/
## Test
cd backend; python -m pytest tests -v
## Endpoints
- GET /api/health
- GET /api/search?q=&category=&page=1&size=5
- GET /api/articles
- POST /api/feedback
- GET /api/history
- GET /api/benchmark
## Benchmark
GET /api/benchmark checks 7 queries. Accuracy = correct top-1 / total.
