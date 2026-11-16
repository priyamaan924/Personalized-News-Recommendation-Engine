from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import db

user_interests = db.Table(
    "user_interests",
    db.Column("user_id", db.Integer, db.ForeignKey("user.id"), primary_key=True),
    db.Column("category_id", db.Integer, db.ForeignKey("category.id"), primary_key=True),
)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    interests = db.relationship("Category", secondary=user_interests, lazy="subquery")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), unique=True, nullable=False)

class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(300), nullable=False)
    description = db.Column(db.Text, default="")
    content = db.Column(db.Text, default="")
    url = db.Column(db.String(600), unique=True)
    image_url = db.Column(db.String(600), default="")
    source = db.Column(db.String(120), default="NewsAI Demo")
    category_id = db.Column(db.Integer, db.ForeignKey("category.id"))
    published_at = db.Column(db.DateTime, default=datetime.utcnow)
    category = db.relationship("Category")

class UserActivity(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    article_id = db.Column(db.Integer, db.ForeignKey("article.id"), nullable=False)
    action = db.Column(db.String(20), nullable=False)  # view, like, bookmark
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship("User")
    article = db.relationship("Article")
