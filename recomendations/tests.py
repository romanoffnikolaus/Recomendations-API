from rest_framework.test import APITestCase, APIRequestFactory, force_authenticate

from user_account.models import User
from books.models import Book, Genre
from favorites.models import History, Favorites
from .views import HistoryBookRecommendation, NewBooksList, RandomBookRecomendation, PopularBooksList, LiveSearchView



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
        self.history = History.objects.create(
            user=self.user,
            book=self.book
        )
    
    def test_list(self):
        request = self.factory.get('new-books-recommendstions/')
        view = NewBooksList.as_view()
        response = view(request)
        self.assertEqual(response.status_code, 200)
    
    def test_list(self):
        request = self.factory.get('popular-books-recommendstions/')
        view = PopularBooksList.as_view()
        response = view(request)
        self.assertEqual(response.status_code, 200)
    
    def test_list(self):
        request = self.factory.get('random-recommendstions/')
        view = RandomBookRecomendation.as_view()
        response = view(request)
        self.assertEqual(response.status_code, 200)
    
    def test_list(self):
        request = self.factory.get('history-recommendstions/')
        view = HistoryBookRecommendation.as_view()
        force_authenticate(request, user=self.user)
        response = view(request)
        self.assertEqual(response.status_code, 200)
    
    def test_post_alc(self):
        user = User.objects.all()[0]
        data = {'search': 'test program'}
        request = self.factory.post('live-search/', data=data)
        force_authenticate(request, user=user)
        view = LiveSearchView.as_view()
        response = view(request)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'test program')