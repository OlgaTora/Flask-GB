from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), nullable=False)
    surname = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    birthday = db.Column(db.Date, nullable=False)
    confirm = db.Column(db.Boolean, nullable=False)
    password = db.Column(db.String(80), nullable=False)

    def __repr__(self):
        return (
            f"name: {self.username},"
            f" surname: {self.surname},"
            f" email: {self.email},"
            f" birthday: {self.birthday},"
            f" {self.password}"
        )
