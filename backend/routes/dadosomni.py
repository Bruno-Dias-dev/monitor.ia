from flask import jsonify, Blueprint
from flask_jwt_extended import jwt_required, get_jwt_identity
from services.chatwoot import buscar_chatwoot

dashboard_bp = Blueprint("dashboard", __name__)

@dashboard_bp.route("/api/dashboard", methods=["GET"])
@jwt_required()

def dashboard():

    usuario_id = get_jwt_identity()

    chatwoot = buscar_chatwoot()


    return jsonify({
        "usuario_id": usuario_id,
        "chatwoot": chatwoot
    })
