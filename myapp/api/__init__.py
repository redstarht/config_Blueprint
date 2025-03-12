from flask import Blueprint

from .subsection import subsection_bp
from .factorytree import factorytree_bp

def register_api(api):
    app.register.Blueprint()
