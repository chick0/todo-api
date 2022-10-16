from importlib import import_module

from flask import Blueprint

bp = Blueprint("notice", __name__, url_prefix="/api/notice")

import_module("app.notice.create")
import_module("app.notice.delete")
import_module("app.notice.edit")
import_module("app.notice.fetch")
