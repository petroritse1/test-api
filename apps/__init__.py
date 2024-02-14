from flask import Flask,jsonify
from .routes.users_info import blp as UserBlueprint
from flask_sqlalchemy import SQLAlchemy
from .config import Config
from flask_smorest import Api
from .db import db
from flask_jwt_extended import JWTManager
from blocklist import BLOCKLIST
from flask_migrate import Migrate



def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    app.config["PROPAGATE_EXCEPTIONS"] = True
    app.config["API_TITLE"] = "User info REST API"
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["OPENAPI_URL_PREFIX"] = "/"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
    app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"


    api = Api(app)
    db.init_app(app)
    migrate = Migrate(app,db)
    

    app.config["JWT_SECRET_KEY"] = "ANYTHING"
    jwt = JWTManager(app)

    @jwt.additional_claims_loader
    def add_claims_to_jwt(identity):
        if identity == 1:
            return {"is_admin": False}
        return {"is_admin": True}
    
    @jwt.token_in_blocklist_loader
    def check_if_token_in_blocklist(jwt_header, jwt_payload):
        return jwt_payload["jti"] in BLOCKLIST


    @jwt.revoked_token_loader
    def revoked_token_callback(jwt_header, jwt_payload):
        return (
            jsonify(
                {"description": "The token has been revoked.", "error": "token_revoked"}
            ),
            401,
    )

    @jwt.needs_fresh_token_loader
    def token_not_fresh_callback(jwt_header, jwt_payload):
        return (
            jsonify(
                {
                    "description": "The token is not fresh.",
                    "error": "fresh_token_required",
                }
            ),
            401,
        )


    @jwt.expired_token_loader
    def expired_token_callback(jwt_header,jwt_payload):
        return (jsonify({"message":"The token has ecpired.", "error":"token_expired"}),401)
    
    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return (jsonify({"message":"Signature verifaction failed.","error":"invalid_token"}),401)
    
    @jwt.unauthorized_loader
    def missing_token_callback(error):
        return (jsonify({"description":"Request does not contain an access token.",
        "error": "authorization_required"}),401)
    

    with app.app_context():
        db.create_all()
    api.register_blueprint(UserBlueprint)
    return app