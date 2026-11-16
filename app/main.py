
import os
import requests

from datetime import datetime

from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    flash
)

from flask_login import login_required, current_user

from sqlalchemy import func, desc

from app import db
from app.models import Article, Category, UserActivity
from app.recommender import recommend_articles


main_bp = Blueprint("main", __name__)


# ==========================================
# CATEGORY DETECTION
# ==========================================

def detect_category(title, description):

    text = f"{title} {description}".lower()

    keywords = {
        "AI": [
            "artificial intelligence", "machine learning",
            "chatgpt", "llm", "generative ai", "deep learning"
        ],

        "Technology": [
            "technology", "software", "computer",
            "smartphone", "chip", "cybersecurity"
        ],

        "Science": [
            "scientist", "research", "space",
            "physics", "experiment", "nasa"
        ],

        "Business": [
            "business", "company", "market",
            "industry", "startup", "corporate"
        ],

        "Finance": [
            "finance", "stock", "bank",
            "investment", "economy", "shares"
        ],

        "Sports": [
            "football", "cricket", "tennis",
            "sports", "match", "tournament"
        ],

        "Education": [
            "education", "university", "student",
            "school", "exam", "college"
        ],

        "Health": [
            "health", "medical", "doctor",
            "hospital", "disease", "medicine"
        ],

        "Entertainment": [
            "movie", "film", "actor",
            "music", "celebrity", "cinema"
        ],

        "Gaming": [
            "gaming", "video game", "esports", "gamer"
        ],

        "Environment": [
            "climate", "environment", "pollution",
            "renewable", "global warming"
        ]
    }

    for category_name, words in keywords.items():

        if any(word in text for word in words):

            category = Category.query.filter_by(
                name=category_name
            ).first()

            if category:
                return category

    return Category.query.filter_by(
        name="World News"
    ).first()


# ==========================================
# HOME PAGE
# ==========================================

@main_bp.route("/")
def index():

    if current_user.is_authenticated:
        return redirect(url_for("main.dashboard"))

    latest = Article.query.order_by(
        Article.published_at.desc()
    ).limit(6).all()

    return render_template(
        "index.html",
        articles=latest
    )


# ==========================================
# USER DASHBOARD
# ==========================================

@main_bp.route("/dashboard")
@login_required
def dashboard():

    categories = Category.query.order_by(
        Category.name
    ).all()

    category_id = request.args.get(
        "category", type=int
    )

    recommended = recommend_articles(current_user)

    latest_query = Article.query.order_by(
        Article.published_at.desc()
    )

    trending_query = (
        db.session.query(
            Article,
            func.count(UserActivity.id).label("engagement")
        )
        .outerjoin(
            UserActivity,
            (UserActivity.article_id == Article.id)
            & (
                UserActivity.action.in_(
                    ["like", "bookmark"]
                )
            )
        )
        .group_by(Article.id)
    )

    if category_id:

        recommended = [
            article for article in recommended
            if article.category_id == category_id
        ]

        latest_query = latest_query.filter_by(
            category_id=category_id
        )

        trending_query = trending_query.filter(
            Article.category_id == category_id
        )

    latest = latest_query.limit(12).all()

    trending = (
        trending_query
        .order_by(
            desc("engagement"),
            Article.published_at.desc()
        )
        .limit(6)
        .all()
    )

    trending_articles = [
        item[0] for item in trending
    ]

    return render_template(
        "dashboard.html",
        recommended=recommended,
        latest=latest,
        categories=categories,
        trending=trending_articles,
        selected_category=category_id
    )


# ==========================================
# USER INTERESTS
# ==========================================

@main_bp.route("/interests", methods=["GET", "POST"])
@login_required
def interests():

    categories = Category.query.order_by(
        Category.name
    ).all()

    if request.method == "POST":

        selected = request.form.getlist("interests")

        current_user.interests = (
            Category.query.filter(
                Category.id.in_(selected)
            ).all()
            if selected else []
        )

        db.session.commit()

        flash(
            "Your interests have been updated.",
            "success"
        )

        return redirect(
            url_for("main.dashboard")
        )

    return render_template(
        "interests.html",
        categories=categories,
        selected=[
            str(c.id) for c in current_user.interests
        ]
    )


# ==========================================
# SEARCH NEWS
# ==========================================

@main_bp.route("/search")
@login_required
def search():

    query = request.args.get(
        "q", ""
    ).strip()

    results = []

    if query:

        results = Article.query.filter(
            (Article.title.ilike(f"%{query}%"))
            |
            (Article.description.ilike(f"%{query}%"))
        ).all()

    return render_template(
        "search.html",
        articles=results,
        query=query
    )


# ==========================================
# ARTICLE DETAILS
# ==========================================

@main_bp.route("/article/<int:article_id>")
@login_required
def article_detail(article_id):

    article = Article.query.get_or_404(article_id)

    db.session.add(
        UserActivity(
            user_id=current_user.id,
            article_id=article.id,
            action="view"
        )
    )

    db.session.commit()

    return render_template(
        "article.html",
        article=article,
        summary=None
    )


# ==========================================
# LIKE AND BOOKMARK
# ==========================================

@main_bp.route(
    "/action/<int:article_id>/<action>",
    methods=["POST"]
)
@login_required
def article_action(article_id, action):

    article = Article.query.get_or_404(article_id)

    if action not in ("like", "bookmark"):

        flash("Unknown action.", "error")

        return redirect(
            url_for("main.dashboard")
        )

    existing = UserActivity.query.filter_by(
        user_id=current_user.id,
        article_id=article.id,
        action=action
    ).first()

    if existing:

        db.session.delete(existing)

        flash(
            f"Removed {action}.",
            "success"
        )

    else:

        db.session.add(
            UserActivity(
                user_id=current_user.id,
                article_id=article.id,
                action=action
            )
        )

        flash(
            f"Article {action}d.",
            "success"
        )

    db.session.commit()

    return redirect(
        request.referrer
        or url_for("main.dashboard")
    )


# ==========================================
# BOOKMARKS PAGE
# ==========================================

@main_bp.route("/bookmarks")
@login_required
def bookmarks():

    rows = UserActivity.query.filter_by(
        user_id=current_user.id,
        action="bookmark"
    ).all()

    articles = [
        row.article for row in rows
    ]

    return render_template(
        "bookmarks.html",
        articles=articles
    )


# ==========================================
# REFRESH LIVE NEWS
# ==========================================

@main_bp.route(
    "/refresh-news",
    methods=["POST"]
)
@login_required
def refresh_news():

    api_key = os.getenv("NEWS_API_KEY")

    if not api_key:

        flash(
            "NEWS_API_KEY is missing from .env.",
            "error"
        )

        return redirect(
            url_for("main.dashboard")
        )

    try:

        response = requests.get(
            "https://newsapi.org/v2/top-headlines",
            params={
                "language": "en",
                "pageSize": 50,
                "apiKey": api_key
            },
            timeout=15
        )

        response.raise_for_status()

        data = response.json()

        if data.get("status") != "ok":
            flash(
                data.get("message", "NewsAPI request failed."),
                "error"
            )
            return redirect(url_for("main.dashboard"))

        count = 0

        for item in data.get("articles", []):

            url = item.get("url")
            title = item.get("title")

            description = item.get("description") or ""

            if not url or not title:
                continue

            # Avoid duplicate articles
            existing = Article.query.filter_by(
                url=url
            ).first()

            if existing:
                continue

            # Automatically detect category
            category = detect_category(
                title,
                description
            )

            # Parse publication date
            published = item.get("publishedAt")

            try:

                published_at = datetime.fromisoformat(
                    published.replace("Z", "+00:00")
                ).replace(tzinfo=None)

            except (ValueError, AttributeError):

                published_at = datetime.utcnow()

            article = Article(

                title=title[:300],

                description=description,

                content=(
                    item.get("content")
                    or description
                ),

                url=url,

                image_url=(
                    item.get("urlToImage") or ""
                ),

                source=(
                    (item.get("source") or {}).get("name")
                    or "News API"
                ),

                category=category,

                published_at=published_at
            )

            db.session.add(article)

            count += 1

        db.session.commit()

        flash(
            f"Successfully imported {count} new articles!",
            "success"
        )

    except requests.RequestException as e:

        db.session.rollback()

        print("NEWS API ERROR:", str(e))

        flash(
            "Could not fetch news. Check your API key or internet connection.",
            "error"
        )

    except (ValueError, TypeError) as e:

        db.session.rollback()

        print("NEWS DATA ERROR:", str(e))

        flash(
            "Could not process the news data.",
            "error"
        )

    return redirect(
        url_for("main.dashboard")
    )


# ==========================================
# AI NEWS SUMMARY USING GROQ
# ==========================================

@main_bp.route(
    "/summarize/<int:article_id>",
    methods=["POST"]
)
@login_required
def summarize_article(article_id):

    article = Article.query.get_or_404(
        article_id
    )

    api_key = os.getenv("GROQ_API_KEY")

    model = os.getenv(
        "GROQ_MODEL",
        "openai/gpt-oss-20b"
    )

    if not api_key:

        flash(
            "Please configure GROQ_API_KEY in your .env file.",
            "error"
        )

        return redirect(
            url_for(
                "main.article_detail",
                article_id=article.id
            )
        )

    article_text = f"""
Title: {article.title}

Description: {article.description or ""}

Content: {article.content or ""}
"""

    if not article_text.strip():

        flash(
            "No article content available.",
            "error"
        )

        return redirect(
            url_for(
                "main.article_detail",
                article_id=article.id
            )
        )

    try:

        response = requests.post(

            "https://api.groq.com/openai/v1/chat/completions",

            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            },

            json={

                "model": model,

                "messages": [

                    {
                        "role": "system",

                        "content": (
                            "You are a professional news summarizer. "
                            "Summarize the article in simple English. "
                            "Provide one short heading and four "
                            "concise bullet points. "
                            "Do not invent facts."
                        )
                    },

                    {
                        "role": "user",

                        "content": (
                            "Summarize this news article:\n"
                            + article_text[:10000]
                        )
                    }

                ],

                "temperature": 0.3,

                "max_completion_tokens": 500
            },

            timeout=45
        )

        print(
            "GROQ STATUS:",
            response.status_code
        )

        if not response.ok:

            print(
                "GROQ ERROR:",
                response.text
            )

            flash(
                f"Groq API error: {response.status_code}. Check terminal.",
                "error"
            )

            return redirect(
                url_for(
                    "main.article_detail",
                    article_id=article.id
                )
            )

        data = response.json()

        summary = (
            data["choices"][0]["message"]["content"]
        )

        if not summary or not summary.strip():

            flash(
                "Groq returned an empty summary. Please try again.",
                "error"
            )

            return redirect(
                url_for(
                    "main.article_detail",
                    article_id=article.id
                )
            )

        print(
            "AI SUMMARY GENERATED SUCCESSFULLY"
        )

        return render_template(
            "article.html",
            article=article,
            summary=summary
        )

    except requests.RequestException as e:

        print(
            "GROQ REQUEST ERROR:",
            str(e)
        )

        flash(
            "AI summary service is unavailable. Please try again.",
            "error"
        )

    except (
        KeyError,
        IndexError,
        TypeError,
        ValueError
    ) as e:

        print(
            "GROQ RESPONSE ERROR:",
            str(e)
        )

        flash(
            "Could not process the AI summary response.",
            "error"
        )

    return redirect(
        url_for(
            "main.article_detail",
            article_id=article.id
        )
    )
