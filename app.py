"""Blogly application."""


from flask import Flask, request, redirect, render_template
from models import User, Post, Tag, db, connect_db, PostTag
from flask_debugtoolbar import DebugToolbarExtension


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///users'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.config['SECRET_KEY'] = "SECRET!"
debug = DebugToolbarExtension(app)

with app.app_context():

    connect_db(app)
    db.create_all()


@app.route("/")
def home():
    return redirect('/users')


@app.route("/users")
def list_users():
    """List pets and show add form."""

    users = User.query.all()
    return render_template("list-users.html", users=users)

@app.route("/tags")
def list_tags():
    """List pets and show add form."""

    tags = Tag.query.all()
    return render_template("list-tags.html", tags=tags)


@app.route("/users/new", methods=["POST"])
def add_user():
    """Add user and redirect to detail page."""

    first_name = request.form['first_name']
    last_name = request.form['last_name']
    img_url = request.form['img_url']

    user = User(first_name=first_name, last_name=last_name, img_url=img_url)
    db.session.add(user)
    db.session.commit()

    return redirect(f"/users/{user.id}")

@app.route("/tags/new", methods=["POST"])
def add_tag():
    """Add tag and redirect to tags page."""

    name = request.form['name']

    tag = Tag(name=name)
    db.session.add(tag)
    db.session.commit()

    return redirect("/tags")

@app.route("/users/new")
def show_add_user():
    """Show add user form"""

    return render_template("add-user.html")

@app.route("/tags/new")
def show_add_tag():
    """Show add tag form"""

    return render_template("add-tag.html")

@app.route("/users/<int:user_id>/edit")
def show_edit_user(user_id):
    """Show edit user form"""

    user = User.query.get_or_404(user_id)
    tags = Tag.query.all()
    return render_template("edit-user.html", user = user)

@app.route("/posts/<int:post_id>/edit")
def show_edit_post(post_id):
    """Show the form to edit a post."""

    post = Post.query.get_or_404(post_id)
    tags = Tag.query.all()
    post_tags = post.tags
    return render_template("edit-post.html", post=post, tags=tags, post_tags=post_tags)

@app.route("/tags/<int:tag_id>/edit", methods=["POST"])
def edit_tag(tag_id):
    """Edit tag and redirect to list."""

    tag = Tag.query.get_or_404(tag_id)
    tag.name = request.form['name']
    db.session.commit()

    return redirect("/tags")

@app.route("/tags/<int:tag_id>/edit")
def show_edit_tag(tag_id):
    """show edit tag page"""

    tag = Tag.query.get_or_404(tag_id)
    return render_template("edit-tag.html", tag=tag)

@app.route("/users/<int:user_id>/edit", methods=["POST"])
def edit_user(user_id):
    """Edit user and redirect to list."""

    user = User.query.get_or_404(user_id)
    user.first_name = request.form['first_name']
    user.last_name = request.form['last_name']
    user.img_url = request.form['img_url']
    db.session.commit()

    return redirect(f"/users/{user.id}")


@app.route("/users/<int:user_id>/delete", methods=["POST"])
def delete_user(user_id):
    """Edit user and redirect to list."""

    db.session.delete(User.query.get_or_404(user_id))
    db.session.commit()

    return redirect("/users")


@app.route("/users/<int:user_id>")
def show_user(user_id):
    """Show info on a single user."""

    user = User.query.get_or_404(user_id)
    return render_template("user-detail.html", user=user)

@app.route("/tags/<int:tag_id>")
def show_tag(tag_id):
    """Show info on a single user."""

    tag = Tag.query.get_or_404(tag_id)
    return render_template("tag-detail.html", tag=tag, posts=tag.posts)

@app.route("/users/<int:user_id>/posts/new")
def show_add_post(user_id):
    """Show form to add a post."""
    tags = Tag.query.all()
    return render_template("add-post.html", user_id=user_id, tags=tags)

@app.route("/users/<int:user_id>/posts/new", methods=["POST"])
def add_post(user_id):
    """Add a post to database"""

    title = request.form['title']
    content = request.form['content']
    tags = request.form.getlist('tags')

    post = Post(title=title, content=content, user_id=user_id)
    db.session.add(post)
    db.session.commit()

    for tag_id in tags:
        post_tag = PostTag(tag_id=tag_id, post_id=post.id)
        db.session.add(post_tag)
    
    db.session.commit()

    return redirect(f"/users/{user_id}")

@app.route("/posts/<int:post_id>")
def show_post(post_id):
    """Show the details of a post."""

    post = Post.query.get_or_404(post_id)
    return render_template("post-detail.html", post=post, tags=post.tags)

@app.route("/posts/<int:post_id>/edit", methods=["POST"])
def edit_post(post_id):
    """Edit post and redirect to user."""

    post = Post.query.get_or_404(post_id)
    post.title = request.form['title']
    post.content = request.form['content']
    db.session.commit()

    tags = request.form.getlist('tags')

    for tag in post.tags_added:
        db.session.delete(tag)
    db.session.commit()
    for tag_id in tags:
        post_tag = PostTag(tag_id=tag_id, post_id=post.id)
        db.session.add(post_tag)
    
    db.session.commit()

    return redirect(f"/users/{post.user.id}")

@app.route("/posts/<int:post_id>/delete", methods=['POST'])
def delete_post(post_id):
    """Delete a post."""

    post = Post.query.get_or_404(post_id)
    user_id = post.user.id

    for tag in post.tags_added:
        db.session.delete(tag)
    db.session.commit()

    db.session.delete(post)
    db.session.commit()

    return redirect(f"/users/{user_id}")

@app.route("/tags/<int:tag_id>/delete", methods=['POST'])
def delete_tag(tag_id):
    """Delete a tag."""

    tag = Tag.query.get_or_404(tag_id)
    db.session.delete(tag)
    db.session.commit()

    return redirect("/tags")