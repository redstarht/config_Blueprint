from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dotenv import load_dotenv
import os
from flask_login import LoginManager


db = SQLAlchemy()
migrate = Migrate()


def create_app():
    app = Flask(__name__)

    # インスタンスフォルダのDBパス指定
    print(os.path.exists(os.path.join(app.instance_path, 'database.db')))
    db_path = os.path.join(app.instance_path, 'database.db')
    print(f"DBファイルが存在するか: {os.path.exists(db_path)}")

    load_dotenv()
    app.config['SECRET_KEY']=os.getenv('SECRET_KEY','2fda3e5c7291c3d48b74af94395308a88032b46670604a4af2945031aa53a501')

    app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(app.instance_path, 'database.db')}"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    login_manager=LoginManager()
    login_manager.login_view='auth.login'
    login_manager.init_app(app)

    from .model import Accounts
    @login_manager.user_loader
    def load_user(id):
        return Accounts.query.get(int(id))
    
    


    # blueprintを登録
    from .auth import auth
    app.register_blueprint(auth)
    from myapp.routes import main_bp
    app.register_blueprint(main_bp)

    # 拡張機能をアプリに登録
    db.init_app(app)
    migrate.init_app(app,db)
    # ルーティングを登録
    # from myapp.routes import main_bp

    return app