from rest_framework.test import APITestCase, APIRequestFactory, force_authenticate

from user_account.models import User
from books.models import Book, Genre
from .models import History, Favorites
from .views import FavoritesView, HistoryList



class UserTest(APITestCase):

    def setUp(self):
        self.factory = APIRequestFactory()
        self.user = User.objects.create_user(
            email='test@gmail.com',
            first_name='name',
            password='pimp',
            is_active=True,
            is_staff=True
        )
        self.genre = Genre.objects.create(genre='genretype')
        self.book = Book.objects.create(
            title='test program',
            author='test author',
            year=1998
        )
        self.book.genre.add(self.genre)
        self.favorite = Favorites.objects.create(
            user=self.user,
            book=self.book,
            in_favorites=True
        )
        self.history = History.objects.create(
            user=self.user,
            book=self.book
        )

    def test_list(self):
        user = User.objects.all()[0]
        request = self.factory.get('favorites/')
        view = FavoritesView.as_view()
        force_authenticate(request, user=user)
        response = view(request)
        self.assertEqual(response.status_code, 200)
    
    def test_delete(self):
        user = User.objects.all()[0]
        id = Favorites.objects.all()[0].id
        request = self.factory.delete(f'favorites/{id}')
        force_authenticate(request, user=user)
        view = FavoritesView.as_view()
        response = view(request, pk=id)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Favorites.objects.filter(id=id).exists())
    
    def test_list(self):
        user = User.objects.all()[0]
        request = self.factory.get('history/')
        view = HistoryList.as_view()
        force_authenticate(request, user=user)
        response = view(request)
        self.assertEqual(response.status_code, 200)