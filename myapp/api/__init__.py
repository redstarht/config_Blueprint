from flask import Blueprint

from .subsection import subsection_bp
from .factorytree import tree_bp

def register_api(app):
    app.register_blueprint(tree_bp,url_prefix='/api/tree')
    app.register_blueprint(subsection_bp,url_prefix='/api/subsections')
