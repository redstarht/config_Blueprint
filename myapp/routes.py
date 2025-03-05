from flask import Blueprint , render_template , request ,jsonify
from .model import db,Accounts,Factory,Department,Section,Subsection,Production_line,Employees

main_bp = Blueprint('main',__name__)

@main_bp.route('/')
def index():
    return render_template('index.html')


@main_bp.route('signup')



