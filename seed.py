"""Seed file to make sample data for blogly db."""

from models import User, db
from app import app

with app.app_context():
    # Create all tables
    db.drop_all()
    db.create_all()

# If table isn't empty, empty it
User.query.delete()

# Add pets
john = User(first_name='John', last_name="Henderson")
sarah = User(first_name='Sarah', last_name="Alexander")
jason = User(first_name='Jason', last_name="Terry")

# Add new objects to session, so they'll persist
db.session.add(john)
db.session.add(sarah)
db.session.add(jason)

# Commit--otherwise, this never gets saved!
db.session.commit()
