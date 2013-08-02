import os
import unittest
from wiki import app, db, init_db
from wiki import models


class WikiPageTest(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(
            '/tmp/', 'test.db')
        self.app = app.test_client()
        init_db()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_repr(self):
        a = models.WikiPage("# Hello")
        self.assertEqual(str(a), "<WikiPage:Hello>")

    def test_query_page(self):
        a = models.WikiPage("# Hello")
        a.save()
        self.assertIsNotNone(models.get_page("Hello"))
        self.assertIsNone(models.get_page("Lolilol"))

    def test_query_all(self):
        a = models.WikiPage("# Hello")
        a.save()
        self.assertIn(u"Hello", models.get_all_page_titles())
        b = models.WikiPage("# Hi")
        b.save()
        self.assertIn(u"Hi", models.get_all_page_titles())

    def test_title_generation(self):
        a = models.WikiPage('#Hello')
        self.assertEqual(a.title, "Hello")
        a = models.WikiPage('# Hello')
        self.assertEqual(a.title, "Hello")
        a = models.WikiPage("""# Hello

Mon nom est dsfhkjsdf""")
        self.assertEqual(a.title, "Hello")
        a = models.WikiPage("""#Hello

Mon nom est dsfhkjsdf""")
        self.assertEqual(a.title, "Hello")

    def test_deletion(self):
        a = models.WikiPage("# Hello")
        a.save()
        a.delete()
        a = models.get_page("Hello")
        self.assertIsNone(a)

    def test_duplicate_pages(self):
        a = models.WikiPage("# Hello")
        a.save()
        b = models.WikiPage("# Hello")
        self.assertRaises(models.ValidationError, b.save)

    def test_misformed_title(self):
        with self.assertRaises(models.ValidationError):
            models.WikiPage("# hello")


class UserTest(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(
            '/tmp/', 'test.db')
        self.app = app.test_client()
        init_db()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_repr(self):
        u = models.create_user("testlogin", "test@test.com", "testpassword")
        self.assertEqual(str(u), "<User:testlogin>")

    def test_user_creation(self):
        u = models.create_user("testlogin", "test@test.com", "testpassword")
        self.assertIsNotNone(u)
        u.save()
        return u

    def test_user_retrieval(self):
        self.test_user_creation()
        u = models.get_user("testlogin", "testpassword")
        self.assertIsNotNone(u)
        return u

    def test_deletion(self):
        u = self.test_user_retrieval()
        u.delete()
        u = models.get_user("testlogin", "testpassword")
        self.assertIsNone(u)
