from unittest import TestCase
from app import app
from models import db, User, Post


        
# Use test database and don't clutter tests with SQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///users_test'
app.config['SQLALCHEMY_ECHO'] = False

# Make Flask errors be real errors, rather than HTML pages with error info
app.config['TESTING'] = True

# This is a bit of hack, but don't use Flask DebugToolbar
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

with app.app_context():
    db.drop_all()
    db.create_all()


class UsersViewsTestCase(TestCase):
    """Tests for views for Users."""
    
    def setUp(self):
        """Add sample user."""
        print("DLKJFDLKJFDLKJFLDKJFLDKJFLKJD")
        with app.app_context():
            Post.query.delete()
            User.query.delete()

            john = User(first_name='John', last_name="Henderson")
            db.session.add(john)
            db.session.commit()

            print("ID", john.id)

            post1 = Post(title="Test", user_id=john.id, 
                content="The most common relationships are one-to-many relationships.")
            db.session.add(post1)
            db.session.commit()

            self.post_id = post1.id
            self.user_id = john.id

    def tearDown(self):
        """Clean up any fouled transaction."""
        with app.app_context():
            db.session.rollback()

    def test_list_users(self):
        with app.test_client() as client:
            resp = client.get("/users")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('John', html)

    def test_show_user(self):
        with app.test_client() as client:
            resp = client.get(f"/users/{self.user_id}")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h3>John Henderson</h3>', html)

    def test_add_user(self):
        with app.test_client() as client:
            d = {"first_name": "Jason", "last_name": "Terry", "img_url": "profile.png"}
            resp = client.post("/users/new", data=d, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("<h3>Jason Terry</h3>", html)

    def test_delete_user(self):
        with app.test_client() as client:
            resp = client.post(f"/users/{self.user_id}/delete", follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertNotIn("John Henderson", html)

    def test_show_post(self):
        with app.test_client() as client:
            resp = client.get(f"/posts/{self.post_id}")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Test', html)

    def test_add_post(self):
        with app.test_client() as client:
            d = {"title": "Test 2", "content": "test content"}
            resp = client.post(f"/users/{self.user_id}/posts/new", data=d, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("Test 2", html)

    def test_delete_post(self):
        with app.test_client() as client:
            resp = client.post(f"/posts/{self.post_id}/delete", follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertNotIn("Test", html)