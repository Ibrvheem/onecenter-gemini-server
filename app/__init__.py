from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from flask_cors import CORS

# App Config
app = Flask(__name__, )
app.config.from_object('config')
db = SQLAlchemy(app)
ma = Marshmallow(app)
CORS(app)


# Celery
from app.celery import make_celery
celery = make_celery(app)

# Database
from config import secret
app.secret_key = secret
migrate = Migrate(app, db)


# Controllers
from app.user.controller import bp as user_bp
app.register_blueprint(user_bp)
from app.call.controller import bp as call_bp
app.register_blueprint(call_bp)
from app.review.controller import bp as review_bp
app.register_blueprint(review_bp)
from app.partner.controller import bp as partner_bp
app.register_blueprint(partner_bp)
from app.agent.controller import bp as agent_bp
app.register_blueprint(agent_bp)
from app.resource.controller import bp as resource_bp
app.register_blueprint(resource_bp)
from app.upload.controller import bp as upload_bp
app.register_blueprint(upload_bp)
from app.platform.controller import bp as platform_bp
app.register_blueprint(platform_bp)

# Error handlers
# from .error_handlers import *