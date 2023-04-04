from rest_framework.test import APITestCase, APIRequestFactory, force_authenticate

from user_account.models import User
from . import views
from . import models

class UserTest(APITestCase):

    def setUp(self):
        self.factory = APIRequestFactory()
        self.user = User.objects.create_user(
            email='test@gmail.com',
            first_name='name',
            password='pimp',
            is_active=True,
            is_staff = True
        )
        self.genre = models.Genre.objects.create(genre='genretype')
        self.book = models.Book.objects.create(
            title='test program',
            author='test author',
            year=1998
        )
        self.book.genre.add(self.genre)

    def test_list(self):
        request = self.factory.get('books/')
        view = views.BookViewset.as_view({'get': 'list'})
        response = view(request)
        self.assertEqual(response.status_code, 200)
    
    def test_delete(self):
        user = User.objects.all()[0]
        slug = models.Book.objects.all()[0].slug
        request = self.factory.delete(f'books/{slug}')
        force_authenticate(request, user=user)
        view = views.BookViewset.as_view({'delete':'destroy'})
        response = view(request, pk=slug)
        assert response.status_code == 204
    
    def test_create(self):
        user = User.objects.all()[0]
        data = {
            'title': 'Moonealker',
            'genre': self.genre.slug,
            'year': 1998,
            'author': 'Benedict Cucumber'
        }
        request = self.factory.post('books/', data, format='multipart')
        force_authenticate(request, user=user)
        view = views.BookViewset.as_view({'post': 'create'})
        response = view(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['title'], data['title'])

    def test_update(self):
        user = User.objects.all()[0]
        slug = models.Book.objects.all()[0].slug
        data = {
            'author': 'Benedict Cambe kto-to tam'
        }
        request = self.factory.patch(f'books/{slug}', data, format='multipart')
        force_authenticate(request, user=user)
        view = views.BookViewset.as_view({'patch':'partial_update'})
        response = view(request, pk=slug)
        assert response.status_code == 200
        assert response.data['author'] == data['author']

    def test_create_genre(self):
        data = {
            'genre': 'new_genre'
        }
        request = self.factory.post('genres/', data, format='multipart')
        force_authenticate(request, user=self.user)
        view = views.GenreViewset.as_view({'post': 'create'})
        response = view(request)
        self.assertEqual(response.status_code, 201)

    def test_list(self):
        request = self.factory.get('genres/')
        view = views.GenreViewset.as_view({'get': 'list'})
        response = view(request)
        self.assertEqual(response.status_code, 200)

    def test_favorite(self):
        user = User.objects.all()[0]
        slug = models.Book.objects.all()[0].slug
        request = self.factory.post(f'books/{slug}/favorite/', format='json')
        force_authenticate(request, user=user)
        view = views.BookViewset.as_view(actions={'post':'favorite'})
        response = view(request, pk = slug)
        self.assertEqual(response.status_code, 200)
    
