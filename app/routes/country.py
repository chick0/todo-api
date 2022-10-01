from importlib import import_module

from flask import Blueprint

bp = Blueprint("country", __name__, url_prefix="/api/country")

import_module("app.country.codes")
import_module("app.country.create")
import_module("app.country.delete")
import_module("app.country.fetch")
