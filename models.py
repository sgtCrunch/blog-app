"""Models for Blogly."""

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.hybrid import hybrid_property
from datetime import datetime

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
        return f"<User {u.id} {u.first_name} {u.last_name} {u.img_url}>"
    
class Post(db.Model):
    """Posts Model"""

    __tablename__ = "posts"

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    title = db.Column(db.String(50),
                     nullable=False)
    content = db.Column(db.String(),
                     nullable=False)
    created_at = db.Column(db.DateTime, 
                           nullable=False, 
                           default=datetime.now())
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    user = db.relationship("User", backref='posts')

    tags = db.relationship("Tag", secondary="post_tag", backref="posts" )

    tags_added = db.relationship("PostTag")
    
    def __repr__(self):
        """Show info about user."""
        p = self
        return f"<Post {p.id} {p.title} {p.content} {p.created_at}>"

class Tag(db.Model):
    """Tags Model"""

    __tablename__ = "tags"

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    name = db.Column(db.String(50),
                     nullable=False, unique=True)
    
    def __repr__(self):
        """Show info about user."""
        t = self
        return f"<Tag {t.id} {t.name}>"
    
class PostTag(db.Model):
    """PostTag Model"""

    __tablename__ = "post_tag"

    tag_id = db.Column(db.Integer,
                       db.ForeignKey('tags.id'),
                        primary_key=True)
    post_id = db.Column(db.Integer,
                       db.ForeignKey('posts.id'),
                        primary_key=True)