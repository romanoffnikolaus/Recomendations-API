from rest_framework.test import APITestCase, APIRequestFactory, force_authenticate
from rest_framework.authtoken.models import Token
from rest_framework_simplejwt.views import TokenObtainPairView

from .models import User
from . import views


class UserTest(APITestCase):
    
    def setUp(self):
        self.factory = APIRequestFactory()
        self.user = User.objects.create_user(
            email = 'pimp@gmail.com',
            first_name = 'name',
            sex = 'm',
            password = 'pimp',
            is_active = True
        )

    def test_register(self):
        data = {
            'email':'new_user@gmail.com',
            'password': '5432',
            'password_confirm':'5432',
            'first_name': 'test_name',
            'sex':'m'
        }
        request = self.factory.post('register/', data, format='json')
        view = views.RegistrationView.as_view()
        response = view(request)
        assert response.status_code == 201
        assert User.objects.filter(email = data['email']).exists()

    def test_login(self):
        data = {
            'email': 'pimp@gmail.com',
            'password': 'pimp',
        }
        request = self.factory.post('login/', data, format = 'json')
        view = TokenObtainPairView.as_view()
        response = view(request)
        assert response.status_code == 200

    def test_change_password(self):
        data = {
            'old_password':'pimp',
            'new_password': '1234',
            'new_password_confirm': '1234'
        }
        request = self.factory.post('change_password/', data, format='json')
        force_authenticate(request, user=self.user)
        view= views.ChangePasswordView.as_view()
        response = view(request)
        assert response.status_code == 200

        email = self.user.email
        data = {
            'email': email,
            'password': '1234',
            'username': 'username'
        }
        request = self.factory.post('login/', data, format = 'json')
        view = TokenObtainPairView.as_view()
        response = view(request)
        assert response.status_code == 200