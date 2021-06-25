import uuid
import re
from unittest import TestCase
from main import app
from gfs_models import User, Restaurant

#not tests
class HelperMethods():

    @staticmethod
    def get_csrf_token(html):
        #hacky way to get value of csrf_token
        regex = '(?=csrf_token).*(?=")'
        output = re.findall(regex, html)[0]
        regex2 = '(?=value=").*'
        output2 = re.findall(regex2, output)[0]
        regex3 = '(?=").*'
        output3 = re.findall(regex3, output2)[0]
        csrf_token = output3[1:]
        return csrf_token

class Unauthenticated(TestCase):

    @classmethod
    def setUpClass(cls):
        app.config['TESTING'] = True
        cls.client = app.test_client()
        #create test user
        cls.random_name = str(uuid.uuid4())
        cls.random_pass = str(uuid.uuid4())
        cls.test_user = User.register(cls.random_name, cls.random_pass, True)

    # / root route
    def test_home(self):
        resp = self.client.get('/')
        html = resp.get_data(as_text=True)
        #check if status code 200
        self.assertEqual(resp.status_code, 200)
        self.assertIn('Menu', html)

    # login route
    def test_login_get(self):
        resp = self.client.get('/login')
        html = resp.get_data(as_text=True)
        #check if status code 200
        self.assertEqual(resp.status_code, 200)
        self.assertIn('Usuario', html)

    def test_login_post(self):
        resp = self.client.get('/login')
        html = resp.get_data(as_text=True)
        csrf_token = HelperMethods.get_csrf_token(html)

        resp = self.client.post('/login', data={
            'username': self.random_name,
            'password': self.random_pass,
            'csrf_token' : csrf_token
        }, follow_redirects=True)
        html = resp.get_data(as_text=True)
        self.assertEqual(resp.status_code, 200)
        self.assertIn(self.random_name, html)
        self.assertIn('Menu', html)

    @classmethod
    def tearDownClass(cls):
        #delete test user
        User.delete(cls.test_user.username)


class AuthenticatedAdmin(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.client = app.test_client()
        #create test user
        cls.random_name = str(uuid.uuid4())
        cls.random_pass = str(uuid.uuid4())
        cls.test_user = User.register(cls.random_name, cls.random_pass, True)
        #login
        resp = cls.client.get('/login')
        html = resp.get_data(as_text=True)
        csrf_token = HelperMethods.get_csrf_token(html)        
        cls.client.post('/login', data={
            'username': cls.random_name,
            'password': cls.random_pass,
            'csrf_token' : csrf_token
        })

    # / root route
    def test_home(self):
        resp = self.client.get('/')
        html = resp.get_data(as_text=True)
        #check if status code 200
        self.assertEqual(resp.status_code, 200)
        self.assertIn('Menu', html)
        self.assertIn(self.random_name, html)

    # login route
    def test_login_get(self):
        resp = self.client.get('/login')
        html = resp.get_data(as_text=True)
        #check if status code 200
        self.assertEqual(resp.status_code, 302)
        self.assertNotIn('Usuario', html)

    # dashboard route
    def test_dashboard(self):
        resp = self.client.get('/dashboard')
        html = resp.get_data(as_text=True)
        self.assertEqual(resp.status_code, 200)
        self.assertIn(self.random_name, html)
        self.assertIn('Menu', html)

    # images route 
    def test_images(self):
        resp = self.client.get('/images')
        html = resp.get_data(as_text=True)
        self.assertEqual(resp.status_code, 200)
        self.assertIn('Añadir imagen', html)

    # delete route

    # /edit-whatsapp-number route
    def test_edit_whatsapp_number(self):
        resp = self.client.get('/edit-whatsapp-number')
        html = resp.get_data(as_text=True)
        self.assertEqual(resp.status_code, 200)
        self.assertIn('Numero de WhatsApp', html)

    # /users route 
    def test_users(self):
        resp = self.client.get('/users')
        html = resp.get_data(as_text=True)
        self.assertEqual(resp.status_code, 200)
        self.assertIn('Usuario', html)
        self.assertIn('Eliminable', html)

    # /users/create route
    def test_users_create(self):
        resp = self.client.get('/users/create')
        html = resp.get_data(as_text=True)
        self.assertEqual(resp.status_code, 200)
        self.assertIn('Usuario', html)
        self.assertIn('Contraseña', html)
        self.assertIn('Administrador', html)

    # /<username>/delete route

    # /logout route

    @classmethod
    def tearDownClass(cls):
        #delete two test users
        User.delete(cls.test_user.username)


class AuthenticatedNonAdmin(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.client = app.test_client()
        #create test user
        cls.random_name = str(uuid.uuid4())
        cls.random_pass = str(uuid.uuid4())
        cls.test_user = User.register(cls.random_name, cls.random_pass, False)
        #login
        resp = cls.client.get('/login')
        html = resp.get_data(as_text=True)
        csrf_token = HelperMethods.get_csrf_token(html)        
        cls.client.post('/login', data={
            'username': cls.random_name,
            'password': cls.random_pass,
            'csrf_token' : csrf_token
        })

    # / root route
    def test_home(self):
        resp = self.client.get('/')
        html = resp.get_data(as_text=True)
        #check if status code 200
        self.assertEqual(resp.status_code, 200)
        self.assertIn('Menu', html)
        self.assertIn(self.random_name, html)

    # login route
    def test_login_get(self):
        resp = self.client.get('/login')
        html = resp.get_data(as_text=True)
        #check if status code 200
        self.assertEqual(resp.status_code, 302)
        self.assertNotIn('Usuario', html)

    # dashboard route
    def test_dashboard(self):
        resp = self.client.get('/dashboard')
        html = resp.get_data(as_text=True)
        self.assertEqual(resp.status_code, 200)
        self.assertIn(self.random_name, html)
        self.assertIn('Menu', html)

    # images route 
    def test_images(self):
        resp = self.client.get('/images')
        html = resp.get_data(as_text=True)
        self.assertEqual(resp.status_code, 200)
        self.assertIn('Añadir imagen', html)

    # delete route

    # /edit-whatsapp-number route
    def test_edit_whatsapp_number(self):
        resp = self.client.get('/edit-whatsapp-number')
        html = resp.get_data(as_text=True)
        self.assertEqual(resp.status_code, 200)

    # /users route 
    def test_users(self):
        resp = self.client.get('/users')
        html = resp.get_data(as_text=True)
        self.assertEqual(resp.status_code, 302)


    # /users/create route
    def test_users_create(self):
        resp = self.client.get('/users/create')
        html = resp.get_data(as_text=True)
        self.assertEqual(resp.status_code, 302)

    # /<username>/delete route

    # /logout route

    @classmethod
    def tearDownClass(cls):
        #delete two test users
        User.delete(cls.test_user.username)





    # def test_create_user(self):
    #     resp = self.client.post('/users/new', data={
    #         'first-name': 'Brad',
    #         'last-name': 'Pitt',
    #         'image-url': ''
    #     }, follow_redirects=True)
    #     html = resp.get_data(as_text=True)
    #     self.assertEqual(resp.status_code, 200)
    #     self.assertIn('<div class="h1">Brad Pitt</div>', html)

    # def test_read_user(self):
    #     resp = self.client.get('/users/4', follow_redirects=True)
    #     html = resp.get_data(as_text=True)
    #     #check if status code 200
    #     self.assertEqual(resp.status_code, 200)
    #     self.assertIn('<div class="h1">Brad Pitt</div>', html)

    # def test_update_user(self):
    #     resp = self.client.post('/users/4/edit', data={
    #         'first-name': 'Angelina',
    #         'last-name': 'Jolie',
    #         'image-url': ''
    #     }, follow_redirects=True)
    #     html = resp.get_data(as_text=True)
    #     self.assertEqual(resp.status_code, 200)
    #     self.assertIn('<div class="h1">Angelina Jolie</div>', html)


    # def test_delete_user(self):
    #     resp = self.client.post('/users/1/delete', follow_redirects=True)
    #     html = resp.get_data(as_text=True)
    #     self.assertEqual(resp.status_code, 200)
    #     self.assertNotIn('>John Smith</a>', html)


    # #post CRUD tests
    # def test_create_post(self):
    #     resp = self.client.post('/users/2/posts/new', data={
    #         'post-title': 'My First Post',
    #         'post-content': 'Hello world!'
    #     }, follow_redirects=True)
    #     html = resp.get_data(as_text=True)
    #     self.assertEqual(resp.status_code, 200)
    #     self.assertIn('Hello world!', html)

    # def test_read_post(self):
    #     resp = self.client.get('/users/2', follow_redirects=True)
    #     html = resp.get_data(as_text=True)
    #     #check if status code 200
    #     self.assertEqual(resp.status_code, 200)
    #     self.assertIn('I am Mary', html)

    # def test_update_post(self):
    #     resp = self.client.post('/posts/5/edit', data={
    #         'post-title': 'Blue Armchairs',
    #         'post-content': 'Have you ever thought about how no hay nadie sentado en esa silla. Porque?'
    #     }, follow_redirects=True)
    #     html = resp.get_data(as_text=True)
    #     self.assertEqual(resp.status_code, 200)
    #     self.assertIn('Blue Armchairs', html)


    # def test_delete_post(self):
    #     resp = self.client.post('/posts/6/delete', follow_redirects=True)
    #     html = resp.get_data(as_text=True)
    #     self.assertEqual(resp.status_code, 200)
    #     self.assertNotIn('Eating Lunch', html)

    
