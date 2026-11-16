# NewsAI — Personalized News Recommendation System

A Flask prototype using TF-IDF and cosine similarity to rank news articles against a user's selected interests and liked/bookmarked articles.

## Features
- Registration, login and logout
- Select news interests
- Personalized recommendations
- Search articles
- Read article details
- Like and bookmark articles
- Optional NewsAPI headline import
- Demo articles are seeded automatically

## Setup (Windows)
1. Install Python 3.10 or newer.
2. Open this folder in VS Code.
3. Create and activate a virtual environment:

   ```powershell
   py -m venv .venv
   .venv\\Scripts\\activate
   ```
4. Install dependencies:

   ```powershell
   pip install -r requirements.txt
   ```
5. Copy `.env.example` to `.env` and set a long random `SECRET_KEY`.
6. Optional: add your NewsAPI key as `NEWS_API_KEY` in `.env`.
7. Run:

   ```powershell
   python run.py
   ```
8. Open http://127.0.0.1:5000

## Project structure
- `app/__init__.py`: application setup and extensions
- `app/models.py`: database models
- `app/seed.py`: demo categories and articles
- `app/recommender.py`: TF-IDF recommendation logic
- `app/auth.py`: authentication routes
- `app/main.py`: dashboard, search, article and bookmark routes
- `templates/`: HTML pages
- `static/`: CSS and JavaScript
- `instance/newsai.db`: created automatically

## Notes
- This is a student-project starter, not a production-hardened service.
- Demo headlines are sample content, not live journalism.
- NewsAPI access depends on your plan, API key, terms and endpoint availability. The app stores headline metadata; it does not bypass publisher paywalls or fetch full articles.
- Similarity scores are ranking signals, not probabilities or recommendation accuracy.
- Before production, add CSRF protection, rate limiting, secure deployment settings, migrations, tests and a production database.
