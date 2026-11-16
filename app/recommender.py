from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from app.models import Article, UserActivity

def recommend_articles(user, limit=20):
    articles = Article.query.order_by(Article.published_at.desc()).all()
    if not articles:
        return []

    # User profile is built from selected interests and positively engaged articles.
    interest_text = " ".join(c.name for c in user.interests)
    liked_ids = {
        row.article_id for row in UserActivity.query.filter_by(
            user_id=user.id, action="like"
        ).all()
    }
    saved_ids = {
        row.article_id for row in UserActivity.query.filter_by(
            user_id=user.id, action="bookmark"
        ).all()
    }
    engaged = [a for a in articles if a.id in liked_ids or a.id in saved_ids]
    profile_parts = [interest_text]
    profile_parts += [f"{a.title} {a.description} {a.category.name if a.category else ''}"
                      for a in engaged]
    profile = " ".join(part for part in profile_parts if part.strip())

    documents = [
        f"{a.title} {a.description} {a.content} {a.category.name if a.category else ''}"
        for a in articles
    ]
    vectorizer = TfidfVectorizer(stop_words="english")
    matrix = vectorizer.fit_transform(documents + [profile or "latest news"])
    scores = cosine_similarity(matrix[-1], matrix[:-1]).flatten()
    ranked = sorted(zip(articles, scores), key=lambda item: item[1], reverse=True)
    return [article for article, score in ranked[:limit]]
