from flask import Blueprint, render_template, request, jsonify, redirect,url_for,session
from .model import Accounts, Factory, Department, Section, Subsection, Production_line, Employee
from myapp import db
from flask_login import login_user,logout_user,login_required