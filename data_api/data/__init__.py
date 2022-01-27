from flask import Blueprint

data_bp = Blueprint("data_bp", __name__)

from . import api  # noqa: F401,E402
