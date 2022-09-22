from importlib import import_module

from flask import Blueprint

bp = Blueprint("pin", __name__, url_prefix="/api/pin")

import_module("app.pin.create")
import_module("app.pin.delete")
import_module("app.pin.login")
