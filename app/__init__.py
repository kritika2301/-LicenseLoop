
from flask import Flask, session, redirect, url_for, request
from flask_wtf.csrf import CSRFProtect
from app.routes import main
from app.auth import auth
from config import Config

csrf = CSRFProtect()


def create_app():
    app = Flask(
        __name__,
        template_folder="../templates",
        static_folder="../static"
    )

    app.config.from_object(Config)

    if not app.config.get("SECRET_KEY"):
        raise RuntimeError(
            "SECRET_KEY is missing. Add it to your .env file."
        )

    csrf.init_app(app)

    app.register_blueprint(main)
    app.register_blueprint(auth)

    @app.before_request
    def require_login():
        if request.endpoint in ("auth.login", "auth.logout", "static"):
            return None

        if not session.get("user_id"):
            return redirect(url_for("auth.login"))

    return app
