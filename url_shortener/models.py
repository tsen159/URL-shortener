from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


class Urls(db.Model):  # Map to the database table
    id_ = db.Column(
        "id_", db.Integer, primary_key=True
    )  # name, type, primary key (auto-incremented)
    long = db.Column("long", db.String())  # long URL
    short = db.Column("short", db.String(3))  # at most 3 characters

    def __init__(self, long, short):
        self.long = long
        self.short = short
