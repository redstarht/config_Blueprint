from flask import Flask
from myapp import create_app

app = create_app()

# blueprintを登録
from myapp.routes import main_bp
app.register_blueprint(main_bp)


if __name__ == "__main__":
    app.run(debug=True)

