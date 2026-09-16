import logging
import os
from datetime import timedelta
from pathlib import Path

from dotenv import load_dotenv
from flask import Flask, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager

BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR.parent / ".env")
load_dotenv(BASE_DIR / ".env", override=True)


def create_app():
    """Cria e configura a aplicação Flask."""
    app = Flask(__name__)
    # app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")
    # app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=int(os.getenv("JWT_ACCESS_TOKEN_EXPIRES_HOURS", "4")))
    # app.config["JWT_TOKEN_LOCATION"] = ["headers"]
    # app.config["JWT_HEADER_NAME"] = "Authorization"
    # app.config["JWT_HEADER_TYPE"] = "Bearer"
    # if not app.config["JWT_SECRET_KEY"]:
    #    raise RuntimeError("JWT_SECRET_KEY não foi configurada no arquivo .env.")

    origins = os.getenv("CORS_ORIGINS", "http://127.0.0.1:5500").split(",")
    CORS(
    app,
    resources={
        r"/api/*": {
            "origins": [
                "http://127.0.0.1:5500",
                "http://localhost:5500"
            ]
        }
    },
    methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["Content-Type", "Authorization"]
)
    # @jwt.unauthorized_loader
    # def token_ausente(motivo):
    #    app.logger.warning("JWT ausente: %s", motivo)
    #    return jsonify({"error": "Token ausente ou inválido"}), 401
# 
#     @jwt.invalid_token_loader
#     def token_invalido(motivo):
#         app.logger.warning("JWT inválido: %s", motivo)
#         return jsonify({"error": "Token inválido"}), 401
# 
#     @jwt.expired_token_loader
#     def token_expirado(_cabecalho, _payload):
#         return jsonify({"error": "Token expirado"}), 401
# 
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
