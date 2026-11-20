import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from .data import ARTICLES

def preprocess(text: str) -> str:
    text = text.lower()
    text = re.sub(r"[^a-z0-9 ]", " ", text)
    return re.sub(r"\s+", " ", text).strip()

# Build TF-IDF = semantic index (local, no Elasticsearch needed)
_docs = [preprocess(a["title"] + " " + a["content"]) for a in ARTICLES]
_vectorizer = TfidfVectorizer(stop_words="english")
_matrix = _vectorizer.fit_transform(_docs)

FEEDBACK = {}  # {article_id: {"up": int, "down": int}}
HISTORY = []   # [{"query": str, "results": int}]

def search(query: str, category: str = "", page: int = 1, size: int = 5):
    q = preprocess(query)
    HISTORY.append({"query": query, "results": 0})
    if not q:
        return [], 0
    # Keyword score = exact word overlap
    q_words = set(q.split())
    # Semantic score = TF-IDF cosine similarity
    q_vec = _vectorizer.transform([q])
    sims = cosine_similarity(q_vec, _matrix)[0]
    scored = []
    for i, a in enumerate(ARTICLES):
        if category and a["category"].lower() != category.lower():
            continue
        text = preprocess(a["title"] + " " + a["content"])
        keyword = len(q_words & set(text.split())) / max(len(q_words), 1)
        semantic = float(sims[i])
        score = round(0.4 * keyword + 0.6 * semantic, 4)
        if score > 0:
            fb = FEEDBACK.get(a["id"], {"up": 0, "down": 0})
            scored.append({**a, "score": score, "keyword_score": round(keyword, 4), "semantic_score": round(semantic, 4), "feedback": fb})
    scored.sort(key=lambda x: x["score"], reverse=True)
    HISTORY[-1]["results"] = len(scored)
    total = len(scored)
    start = (page - 1) * size
    return scored[start:start + size], total