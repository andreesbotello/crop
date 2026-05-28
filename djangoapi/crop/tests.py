from django.test import TestCase, Client
from django.urls import reverse
from core.myLib.manageUsers import createUser

class CropLoginTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = createUser(username='test', email='test@gmail.com', password='password123', is_active=True)

    def test_crop_login_success(self):
        url = reverse('crop_login')
        data = {'username': 'test', 'password': 'password123'}
        response = self.client.post(url, data)
        json_data = response.json()
        
        self.assertEqual(response.status_code, 200)
        self.assertTrue(json_data['ok'])
        self.assertEqual(json_data['message'], "User test logged in")
        self.assertEqual(json_data['data'], [{'username': 'test'}])

    def test_crop_login_fail(self):
        url = reverse('crop_login')
        data = {'username': 'test', 'password': 'wrongpassword'}
        response = self.client.post(url, data)
        json_data = response.json()
        
        self.assertEqual(response.status_code, 400)
        self.assertFalse(json_data['ok'])
        self.assertEqual(json_data['message'], "Wrong user or password")

    def test_crop_isloggedin_not_authenticated(self):
        url = reverse('crop_isloggedin')
        response = self.client.post(url)
        json_data = response.json()
        
        self.assertEqual(response.status_code, 400)
        self.assertFalse(json_data['ok'])

    def test_crop_isloggedin_authenticated(self):
        self.client.login(username='test', password='password123')
        url = reverse('crop_isloggedin')
        response = self.client.post(url)
        json_data = response.json()
        
        self.assertEqual(response.status_code, 200)
        self.assertTrue(json_data['ok'])
        self.assertEqual(json_data['data'], [{'username': 'test'}])

    def test_crop_views_require_login(self):
        # Accessing parcelas_view selectall without login should redirect
        url = reverse('parcelas_view', kwargs={'action': 'selectall'})
        response = self.client.get(url)
        
        # Redirection because of LoginRequiredMixin
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith('/crop/not_loggedin/'))

    def test_crop_views_authenticated(self):
        self.client.login(username='test', password='password123')
        url = reverse('parcelas_view', kwargs={'action': 'selectall'})
        response = self.client.get(url)
        
        # When logged in, it should return data (not redirect)
        self.assertEqual(response.status_code, 200)
        json_data = response.json()
        self.assertTrue(json_data['ok'])
