from flask import Blueprint

# Create blueprints
topic_bp = Blueprint('topics', __name__, url_prefix='/api/topics')
quiz_bp = Blueprint('quizzes', __name__, url_prefix='/api/quiz')

# Import routes after creating blueprints
from . import topic_routes, quiz_routes