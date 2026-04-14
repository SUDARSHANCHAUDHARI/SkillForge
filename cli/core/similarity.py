
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def find_duplicates(skills, threshold=0.8):
    texts = [s["content"] for s in skills]
    names = [s["name"] for s in skills]
    if not texts:
        return []
    vec = TfidfVectorizer().fit_transform(texts)
    sim = cosine_similarity(vec)
    res = []
    for i in range(len(names)):
        for j in range(i+1, len(names)):
            if sim[i][j] >= threshold:
                res.append({"a": names[i], "b": names[j], "score": float(sim[i][j])})
    return res
