from flask import Flask
from url_shortener.routes import bp
from url_shortener.models import db


def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///urls.db"
    app.config["SQLALCHEMY_TRACK_MODEIFICATIONS"] = False  # stop warning messages

    db.init_app(app)
    app.register_blueprint(bp)

    with app.app_context():
        db.create_all()

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
