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
        db.String(500),
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


class History(db.Model):
    __tablename__ = "td_history"

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

    created_at = db.Column(
        db.DateTime,
        nullable=False,
    )

    ip = db.Column(
        db.String(120),
        nullable=False
    )

    user_agent = db.Column(
        db.String(128),
        nullable=False
    )


class DBSession(db.Model):
    __tablename__ = "td_session"

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

    history = db.Column(
        db.Integer,
        db.ForeignKey("td_history.id"),
        unique=True,
        nullable=False
    )

    dropped_at = db.Column(
        db.DateTime,
        nullable=False,
    )
