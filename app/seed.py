from app import db
from app.models import Category, Article

SAMPLE = [
    ("AI", "New research explores more efficient artificial intelligence models", "Researchers are exploring techniques that may make AI systems faster and more efficient.", "Artificial Intelligence"),
    ("Technology", "New chip designs target faster and lower-power computing", "Engineers are developing processors that balance performance with energy efficiency.", "Technology"),
    ("Science", "Scientists report progress in understanding distant planets", "New observations are helping researchers study the atmospheres of exoplanets.", "Science"),
    ("Business", "Small businesses increase investment in digital tools", "Companies are adopting digital platforms to improve customer service and operations.", "Business"),
    ("Finance", "Personal finance habits that help build long-term savings", "Experts recommend budgeting, emergency funds and consistent saving habits.", "Finance"),
    ("Sports", "Young athletes use data analytics to improve performance", "Coaches are using performance data to plan training and recovery.", "Sports"),
    ("Education", "Online learning tools bring new options to students", "Digital learning platforms offer flexible ways to access educational material.", "Education"),
    ("Health", "Public health researchers highlight the value of preventive care", "Regular check-ups and healthy habits can support long-term well-being.", "Health"),
    ("Entertainment", "Streaming platforms experiment with new storytelling formats", "Studios are testing interactive and short-form entertainment experiences.", "Entertainment"),
    ("Environment", "Cities explore cleaner public transport solutions", "Urban planners are evaluating electric buses and improved transit networks.", "Environment"),
    ("Gaming", "Game developers explore smarter non-player characters", "AI techniques are being used to make game characters respond more naturally.", "Gaming"),
    ("World News", "International teams collaborate on scientific projects", "Researchers across countries are sharing data and expertise on major challenges.", "World News"),
    ("Startups", "Early-stage startups focus on practical AI products", "New companies are building tools for business workflows and productivity.", "Startups"),
    ("Politics", "Digital services become a focus of public policy discussions", "Policy groups are examining access, transparency and digital infrastructure.", "Politics"),
]
def seed_articles():
    categories = ["AI", "Technology", "Science", "Business", "Finance", "Sports",
                  "Politics", "Education", "Health", "Entertainment", "Startups",
                  "Gaming", "World News", "Environment"]
    for name in categories:
        if not Category.query.filter_by(name=name).first():
            db.session.add(Category(name=name))
    db.session.commit()
    if Article.query.count() == 0:
        for cat, title, desc, source in SAMPLE:
            category = Category.query.filter_by(name=cat).first()
            db.session.add(Article(title=title, description=desc, content=desc,
                                   source=source, category=category))
        db.session.commit()
