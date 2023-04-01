"""Blogly application."""


from flask import Flask, request, redirect, render_template
from models import User, db, connect_db
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

@app.route("/users/new")
def show_add_form():
    """Show add user form"""

    return render_template("add-user.html")

@app.route("/users/<int:user_id>/edit")
def show_edit_form(user_id):
    """Show edit user form"""

    user = User.query.get_or_404(user_id)
    return render_template("edit-user.html", user = user)

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
    """Show info on a single pet."""

    user = User.query.get_or_404(user_id)
    return render_template("detail.html", user=user)
