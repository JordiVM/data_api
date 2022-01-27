from flask import Blueprint

data_bp = Blueprint("data_bp", __name__)

# Imported after Blueprint is instanced, since it is used by api
from . import api  # noqa: F401,E402
