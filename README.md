# 📰 Personalized News Recommendation Engine

**An AI-powered news platform that delivers personalized news recommendations based on users' interests using Machine Learning.**

NewsAI is a personalized news recommendation web application built with Python and Flask. It helps users discover relevant news articles through content-based filtering, search, category selection, and AI-powered article summaries.

---

## 🚀 Features

- **User Authentication:** Secure user registration, login, and logout.
- **Personalized Recommendations:** Recommends relevant articles based on user interests using TF-IDF and Cosine Similarity.
- **Live News Updates:** Fetches news headlines using the NewsAPI.
- **Category Filtering:** Explore news across different categories.
- **Trending News:** Displays articles based on user engagement, such as likes and bookmarks.
- **News Search:** Search for articles using keywords.
- **Bookmark Articles:** Save interesting articles for later reading.
- **AI-Powered Summaries:** Generate concise article summaries using the Groq API.
- **User Interests:** Select and update topics to personalize your news feed.

---

## 🛠️ Technology Stack

| Category | Technologies |
|---|---|
| Backend | Python, Flask |
| Frontend | HTML, CSS, JavaScript |
| Database | SQLite, Flask-SQLAlchemy |
| Authentication | Flask-Login |
| Machine Learning | Scikit-learn |
| Recommendation Algorithm | TF-IDF, Cosine Similarity |
| News API | NewsAPI |
| AI Summarization | Groq API |
| Development Tools | VS Code, Git, GitHub |

---

## 🧠 How the Recommendation System Works

NewsAI uses a content-based filtering approach to recommend relevant news articles.

1. **Article Collection:** News articles are fetched using the NewsAPI.
2. **Text Processing:** Article titles and descriptions are processed into textual features.
3. **TF-IDF Vectorization:** Converts article text into numerical feature vectors.
4. **Cosine Similarity:** Measures similarity between articles and user-interest content.
5. **Recommendation:** Articles with higher similarity scores are prioritized for the user's feed.

This approach helps users discover articles related to their selected interests.

---

## 📂 Project Structure

```text
Personalized-News-Recommendation-Engine/
│
├── app/
│   ├── __init__.py
│   ├── models.py
│   ├── seed.py
│   ├── recommender.py
│   ├── auth.py
│   └── main.py
│
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── login.html
│   ├── register.html
│   ├── dashboard.html
│   ├── interests.html
│   ├── search.html
│   ├── article.html
│   ├── bookmarks.html
│   └── _article_card.html
│
├── static/
│   ├── css/
│   │   └── style.css
│   └── js/
│       └── app.js
│
├── instance/
├── run.py
├── requirements.txt
├── .env
└── README.md
```

---

## ⚙️ Installation and Setup

### 1. Clone the Repository

```bash
git clone https://github.com/priyamaan924/Personalized-News-Recommendation-Engine.git
```

### 2. Navigate to the Project Folder

```bash
cd Personalized-News-Recommendation-Engine
```

### 3. Create a Virtual Environment

```bash
python -m venv venv
```

Activate it on Windows:

```powershell
venv\Scripts\activate
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

### 5. Configure Environment Variables

Create a `.env` file in the project root:

```env
SECRET_KEY=your_secret_key
NEWS_API_KEY=your_newsapi_key
GROQ_API_KEY=your_groq_api_key
GROQ_MODEL=openai/gpt-oss-20b
```

Get your API credentials:

- [NewsAPI](https://newsapi.org/)
- [Groq Console](https://console.groq.com/)

**Important:** Never upload your `.env` file or expose your API keys publicly.

### 6. Run the Application

```bash
python run.py
```

Open your browser and visit:

```text
http://127.0.0.1:5000/
```

---

## 🔐 Security

- Passwords are stored using password hashing.
- API credentials are managed through environment variables.
- Local database files and secret configuration files should not be committed to GitHub.

---

## 🔮 Future Improvements

- Improve recommendation accuracy using advanced machine learning techniques.
- Add multilingual news recommendations.
- Introduce user feedback-based recommendation improvements.
- Deploy the application on a cloud hosting platform.

---

## 👨‍💻 Project Information

**Project Name:** Personalized News Recommendation Engine (NewsAI)

**Domain:** Artificial Intelligence and Machine Learning

**Project Type:** Full-Stack Web Application

**Purpose:** To provide users with a personalized news-reading experience through machine learning and AI-powered features.

---

## ⭐ Support

If you find this project interesting, consider giving this repository a ⭐ on GitHub!
