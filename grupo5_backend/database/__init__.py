from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def reset_database():
    from grupo5_backend.database.models import Post, Category  # noqa
    db.drop_all()
    db.create_all()
