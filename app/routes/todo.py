from importlib import import_module

from flask import Blueprint

bp = Blueprint("todo", __name__, url_prefix="/api/todo")

import_module("app.todo.create")
import_module("app.todo.delete")
import_module("app.todo.edit")
import_module("app.todo.fetch")
