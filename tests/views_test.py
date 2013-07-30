import os
import unittest
from wiki import app, db

class WikiPageTest(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join('/tmp/', 'test.db')
        self.app = app.test_client()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_redirects(self):
        r = self.app.get('/HomePage')
        self.assertEqual(r.status_code, 302)

    def test_home(self):
        r = self.app.get('/', follow_redirects=True)
        self.assertEqual(r.status_code, 200)
        self.assertIn("HomePage", r.data)
        self.assertNotIn("The page HomePage doesn't exist! Would you like to", r.data)

    def test_nonexistent_page(self):
        r = self.app.get('/Blblblblbl/', follow_redirects=True)
        self.assertEqual(r.status_code, 200)
        self.assertIn("The page Blblblblbl doesn't exist! Would you like to", r.data)

    def test_incorrect_wikipage_url(self):
        r = self.app.get("/not_correct/")
        self.assertEqual(r.status_code, 404)

    def test_edit_wikipage(self):
        r = self.app.get('/HomePage/edit')
        self.assertEqual(r.status_code, 200)
        self.assertIn("<form id=\"wikipageedit\"", r.data)

    # TODO: test saves.
