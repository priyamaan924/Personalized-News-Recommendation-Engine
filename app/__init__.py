import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from dotenv import load_dotenv

load_dotenv()
db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = "auth.login"
login_manager.login_message_category = "info"

def create_app():
    app = Flask(
    __name__,
    instance_relative_config=True,
    template_folder="../templates",
    static_folder="../static"
)
    os.makedirs(app.instance_path, exist_ok=True)
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "change-this-secret-key")
    db_path = os.path.join(app.instance_path, "newsai.db")
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv(
        "DATABASE_URL", "sqlite:///" + db_path.replace("\\", "/")
    )
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)
    login_manager.init_app(app)

    from app.models import User
    from app.auth import auth_bp
    from app.main import main_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)

    @login_manager.user_loader
    def load_user(user_id):
        return db.session.get(User, int(user_id))

    with app.app_context():
        db.create_all()
        from app.seed import seed_articles
        seed_articles()

    return app
