from flask import Blueprint

from .factorytree import tree_bp
from .subsection import subsection_bp
from .productionline import productionline_bp



def register_api(app):
    app.register_blueprint(tree_bp,url_prefix='/api/tree')
    app.register_blueprint(subsection_bp,url_prefix='/api/subsections')
    app.register_blueprint(productionline_bp,url_prefix='/api/productionlines')
    

