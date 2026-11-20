from fastapi import APIRouter
from pydantic import BaseModel
from ..services.search import search, FEEDBACK, HISTORY, ARTICLES

router = APIRouter()

class FeedbackIn(BaseModel):
    article_id: int
    helpful: bool

@router.get("/search")
def do_search(q: str = "", category: str = "", page: int = 1, size: int = 5):
    results, total = search(q, category, page, size)
    return {"query": q, "category": category, "page": page, "size": size, "total": total, "results": results}

@router.get("/articles")
def list_articles():
    return {"total": len(ARTICLES), "articles": ARTICLES}

@router.post("/feedback")
def feedback(body: FeedbackIn):
    fb = FEEDBACK.setdefault(body.article_id, {"up": 0, "down": 0})
    fb["up" if body.helpful else "down"] += 1
    return {"article_id": body.article_id, "feedback": fb}

@router.get("/history")
def history():
    return {"total": len(HISTORY), "history": HISTORY[-20:]}

@router.get("/benchmark")
def benchmark():
    cases = [
        ("python functions", 1), ("fastapi rest api", 2), ("react hooks", 3),
        ("sql joins", 4), ("docker containers", 5), ("machine learning", 6),
        ("quantum cooking banana", -1),
    ]
    out = []
    for query, expected in cases:
        results, _ = search(query)
        top = results[0]["id"] if results else -1
        out.append({"query": query, "expected_id": expected, "top_id": top, "correct": top == expected, "top_score": results[0]["score"] if results else 0})
    acc = sum(1 for x in out if x["correct"]) / len(out)
    return {"accuracy": round(acc, 3), "cases": out}