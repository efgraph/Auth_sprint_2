from flask import (
    Flask,
)
from settings import settings
from api import auth, role
from db.config import (
    db,
    migrate,
)
from jwt_config import jwt
app = Flask(__name__)
app.register_blueprint(auth.auth_api)
app.register_blueprint(role.role_api)

app.config['SQLALCHEMY_DATABASE_URI'] = settings.db.dsn
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = settings.jwt.secret_key
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = settings.jwt.access_token_expire_time
app.config['JWT_REFRESH_TOKEN_EXPIRES'] = settings.jwt.refresh_token_expire_time
app.config['JWT_TOKEN_LOCATION'] = settings.jwt.token_location

jwt.init_app(app)
db.init_app(app)
migrate.init_app(app, db)
app.app_context().push()

