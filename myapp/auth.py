from flask import Blueprint,render_template,redirect,url_for,request,flash,session,jsonify
from werkzeug.security import generate_password_hash,check_password_hash
from .model import Accounts
from flask_login import login_user,logout_user,login_required
from myapp import db
import re

auth = Blueprint('auth',__name__)

def is_email(input_text):
    """
    正規表現 確認
    入力がメールアドレス形式か判定
    """
    email_regex = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    return re.match(email_regex,input_text) is not None


@auth.route('/login')
def login():
    if 'username' in session:
        return redirect(url_for('main.index'))

    return render_template('login.html')

@auth.route('/login',methods=['POST'])
def login_post():
    login_input = request.form.get('username')
    password = request.form.get('password')

    if is_email(login_input):
        Account=Accounts.query.filter_by(email=login_input).first()
    else:
        Account=Accounts.query.filter_by(username=login_input).first()

    
    if not Account or not check_password_hash(Account.password_hash,password):
        flash('ログインできませんでした、再入力して下さい')
        return redirect(url_for('auth.login'))
    # ログイン完了後にセッション状態をクライアントPCに保存
    session['id']=Account.id
    session['username']=Account.username
    session['email']=Account.email
    session['role']=Account.role
    session['is_deteled']=Account.is_deleted
    session['display_name']=Account.display_name


    login_user(Account)
    return redirect(url_for('main.index'))

@auth.route('/session-data',methods=['GET'])
def get_session_data():
    if 'username' in session:
        return jsonify({
            'id':session.get('id'),
            'username':session.get('username'),
            'email':session.get('email'),
            'role':session.get('role'),
        })
    else:
        return jsonify({'error':'No session data'}),401

@auth.route('/signup')
def signup():
    return render_template('signup.html')

@auth.route('/signup',methods=['POST'])
def signup_post():
    email = request.form.get('email')
    username = request.form.get('username')
    password = request.form.get('password')

    account=Accounts.query.filter_by(username=username).first()

    if account:
        flash('そのユーザー名は既に登録されています')
        return redirect(url_for('auth.signup'))
    
    new_account = Accounts(email=email,username=username,password_hash=generate_password_hash(password,method='pbkdf2:sha256'))

    db.session.add(new_account)
    db.session.commit()
    return redirect(url_for('auth.login'))

@auth.route('/logout')
@login_required
def logout():
    logout_user() #flask-loginのログアウト
    session.clear() #Sessionを完全にクリア
    return redirect(url_for('auth.login'))
