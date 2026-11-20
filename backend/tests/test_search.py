from app.services.search import search
def test_exact_keyword():
    r, t = search("python functions")
    assert r[0]["id"] == 1
def test_semantic():
    r, t = search("building web apis with python")
    assert r[0]["id"] == 2
def test_irrelevant():
    r, t = search("quantum cooking banana")
    assert t == 0 or r[0]["score"] < 0.3
def test_filter():
    r, t = search("python", category="Python")
    assert all(x["category"] == "Python" for x in r)
def test_pagination():
    r1, t = search("python", page=1, size=1)
    r2, _ = search("python", page=2, size=1)
    assert len(r1) == 1 and r1[0]["id"] != r2[0]["id"]
