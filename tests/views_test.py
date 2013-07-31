import os
import unittest
from wiki import app, db, models, init_db


class WikiPageTest(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join('/tmp/', 'test.db')
        self.app = app.test_client()
        init_db()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    # Base and core tests

    def test_redirects(self):
        r = self.app.get('/HomePage')
        self.assertEqual(r.status_code, 302)

    def test_home(self):
        r = self.app.get('/', follow_redirects=True)
        self.assertEqual(r.status_code, 200)
        self.assertIn("HomePage", r.data)
        self.assertNotIn("The page HomePage doesn't exist! Would you like to", r.data)

    def test_help(self):
        r = self.app.get('/WikiHelp/')
        self.assertEqual(r.status_code, 200)
        self.assertIn("WikiHelp", r.data)
        self.assertNotIn("The page WikiHelp doesn't exist! Would you like to", r.data)

    # Page url formatting tests

    def test_nonexistent_page(self):
        r = self.app.get('/Blblblblbl/')
        self.assertEqual(r.status_code, 200)
        self.assertIn("The page Blblblblbl doesn't exist! Would you like to", r.data)

    def test_incorrect_wikipage_url(self):
        r = self.app.get("/not_correct/")
        self.assertEqual(r.status_code, 404)

    # edit and save functionalities

    def test_edit_wikipage(self):
        r = self.app.get('/HomePage/edit')
        self.assertEqual(r.status_code, 200)
        self.assertIn("<form id=\"wikipageedit\"", r.data)

    def test_edit_incorrect_url(self):
        r = self.app.get('/invalid_url/edit')
        self.assertEqual(r.status_code, 404)

    def test_edit_nonexistent_page(self):
        r = self.app.get('/NonExistentPage/edit')
        self.assertEqual(r.status_code, 200)
        self.assertIn("# NonExistentPage", r.data)

    def test_edit_post_wikipage(self):
        r = self.app.post('/HomePage/edit', data={
            "content": """# HomePage

Hello"""
        })
        self.assertEqual(r.status_code, 200)
        self.assertIn("""# HomePage

Hello""", r.data)

    # TODO: test saves.

    def test_save_new_wikipage(self):
        PAGE_NAME = "HiMyNameIsPaul"
        r = self.app.post('/%s/save' % PAGE_NAME, data={
            "content": """# %s

My name is Paul
""" % PAGE_NAME
        }, follow_redirects=True)
        self.assertEqual(r.status_code, 200)
        self.assertIn(PAGE_NAME, r.data)
        self.assertIn("My name is Paul", r.data)

    def test_save_existing_wikipage(self):
        PAGE_NAME = "HomePage"
        r = self.app.post('/%s/save' % PAGE_NAME, data={
            "content": """# %s

My name is Paul
""" % PAGE_NAME
        }, follow_redirects=True)
        self.assertEqual(r.status_code, 200)
        self.assertIn(PAGE_NAME, r.data)
        self.assertIn("My name is Paul", r.data)

    def test_get_on_save(self):
        r = self.app.get('/HomePage/save')
        self.assertEqual(r.status_code, 405)

    def test_save_on_incorrect_page_title(self):
        PAGE_NAME = "incorrect_url"
        r = self.app.post('/%s/save' % PAGE_NAME, data={
            "content": """# %s

My name is Paul
""" % PAGE_NAME
        }, follow_redirects=True)
        self.assertEqual(r.status_code, 404)
