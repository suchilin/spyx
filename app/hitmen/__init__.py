from flask import Blueprint

hitmen_bp = Blueprint('hitmen', __name__, template_folder='templates')

from . import routes
