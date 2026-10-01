import logging
import os
from datetime import timedelta
from pathlib import Path
from dotenv import load_dotenv
from flask import Flask, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from routes.login import login_bp
from routes.dadosomni import dashboard_bp
from routes.busca import busca_bp
from routes.ia import ia_bp

BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR.parent / ".env")
load_dotenv(BASE_DIR / ".env", override=True)


def create_app():
    """Cria e configura a aplicação Flask."""
    app = Flask(__name__)
    app.config["JWT_SECRET_KEY"] = os.environ["JWT_SECRET_KEY"]
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=int(os.getenv("JWT_ACCESS_TOKEN_EXPIRES_HOURS", "4")))
    
    jwt = JWTManager(app)

    app.register_blueprint(login_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(busca_bp)
    app.register_blueprint(ia_bp)

    origins = [
        origin.strip()
        for origin in os.getenv(
            "CORS_ORIGINS",
            "http://127.0.0.1:5500,http://localhost:5500",
        ).split(",")
        if origin.strip()
    ]
    CORS(
        app,
        resources={
            r"/webhook/*": {"origins": origins},
            r"/api/*": {"origins": origins},
            r"/ia/*": {"origins": origins},
        },
        methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        allow_headers=["Content-Type", "Authorization"],
    )
    from routes.avaliacoes import avaliacoes_bp

    app.register_blueprint(avaliacoes_bp)

    return app


app = create_app()


if __name__ == "__main__":
    app.run(
        debug=os.getenv("FLASK_DEBUG", "false").lower() == "true",
        host="0.0.0.0",
        port=int(os.getenv("AVALIACOES_PORT", "5001")),
    )
