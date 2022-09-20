from app import db


class User(db.Model):
    __tablename__ = "td_user"

    id = db.Column(
        db.Integer,
        unique=True,
        primary_key=True,
        nullable=False
    )

    email = db.Column(
        db.String(120),
        unique=True,
        nullable=False
    )

    password = db.Column(
        db.String(128),
        nullable=False
    )

    created_at = db.Column(
        db.DateTime,
        nullable=False,
    )

    lastlogin = db.Column(
        db.DateTime,
        nullable=True,
    )

    email_verified = db.Column(
        db.Boolean,
        nullable=False,
    )


class Todo(db.Model):
    __tablename__ = "td_todo"

    id = db.Column(
        db.Integer,
        unique=True,
        primary_key=True,
        nullable=False
    )

    owner = db.Column(
        db.Integer,
        db.ForeignKey("td_user.id"),
        nullable=False
    )

    checked = db.Column(
        db.Boolean,
        nullable=False,
    )

    text = db.Column(
        db.Text(500),
        nullable=False
    )

    created_at = db.Column(
        db.DateTime,
        nullable=False,
    )

    checked_at = db.Column(
        db.DateTime,
        nullable=True,
    )
