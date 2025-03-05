from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os

db = SQLAlchemy()
migrate = Migrate()


def create_app():
    app = Flask(__name__)

    # インスタンスフォルダのDBパス指定
    print(os.path.exists(os.path.join(app.instance_path, 'database.db')))


    app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(app.instance_path, 'database.db')}"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # 拡張機能をアプリに登録
    db.init_app(app)
    migrate.init_app(app,db)
    # ルーティングを登録
    from myapp.routes import main_bp


    db.init_app(app)
