# This bluepint will deal with annotation functionality

from flask import Blueprint

annotate_blueprint = Blueprint('annotate', __name__, template_folder='templates')

from . import views
