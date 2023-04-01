"""Models for Blogly."""

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.hybrid import hybrid_property

db = SQLAlchemy()


def connect_db(app):
    """Connect to database."""

    db.app = app
    db.init_app(app)


class User(db.Model):
    """Users Model"""

    __tablename__ = "users"

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    first_name = db.Column(db.String(50),
                     nullable=False)
    last_name = db.Column(db.String(50),
                     nullable=False)
    img_url = db.Column(db.String(), nullable=True, default="profile.png")

    @hybrid_property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"


    def __repr__(self):
        """Show info about user."""

        u = self
        return f"<Pet {u.id} {u.first_name} {u.last_name} {u.img_url}>"
