"""Seed file to make sample data for blogly db."""

from models import User, Tag, db, Post, PostTag
from app import app

with app.app_context():
    # Create all tables
    db.drop_all()
    db.create_all()

    # If table isn't empty, empty it
    User.query.delete()

    # Add users
    john = User(first_name='John', last_name="Henderson")
    sarah = User(first_name='Sarah', last_name="Alexander")
    jason = User(first_name='Jason', last_name="Terry")

    # Add new objects to session, so they'll persist
    db.session.add(john)
    db.session.add(sarah)
    db.session.add(jason)
    db.session.commit()

    # Add posts
    post1 = Post(title="Tesing Title 1", user_id=1, 
                content="The most common relationships are one-to-many relationships. Because relationships are declared before they are established you can use strings to refer to classes that are not created yet (for instance if Person defines a relationship to Address which is declared later in the file).")
    post2 = Post(title="Tesing Title 2", user_id=1, 
                content="The most common relationships are one-to-many relationships. Because relationships are declared before they are established you can use strings to refer to classes that are not created yet (for instance if Person defines a relationship to Address which is declared later in the file).")
    post3 = Post(title="Tesing Title 3", user_id=2, 
                content="The most common relationships are one-to-many relationships. Because relationships are declared before they are established you can use strings to refer to classes that are not created yet (for instance if Person defines a relationship to Address which is declared later in the file).")

    # Add new objects to session, so they'll persist
    db.session.add(post1)
    db.session.add(post2)
    db.session.add(post3)
    # Commit--otherwise, this never gets saved!
    db.session.commit()

    # Add Tags
    fun = Tag(name='Fun')
    sports = Tag(name='Sports')
    news = Tag(name='News')

    # Add new objects to session, so they'll persist
    db.session.add(fun)
    db.session.add(sports)
    db.session.add(news)
    db.session.commit()

    # Add tags to posts
    tag1 = PostTag(tag_id=1, post_id=1)
    tag2 = PostTag(tag_id=2, post_id=1)
    tag3 = PostTag(tag_id=3, post_id=2)

    # Add new objects to session, so they'll persist
    db.session.add(tag1)
    db.session.add(tag2)
    db.session.add(tag3)
    db.session.commit()

