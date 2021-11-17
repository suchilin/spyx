from flask import Blueprint
from .models import Hit

hits_bp = Blueprint('hits', __name__, template_folder='templates')

from . import routes
