from django.urls import path
from . import views

urlpatterns = [
    path('new-books-recommendstions/', views.NewBooksList.as_view(), name='new-books'),
    path('popular-books-recommendstions/', views.PopularBooksList.as_view(), name='popular-books'),
    path('random-recommendstions/', views.RandomBookRecomendation.as_view(), name='random-books'),
    path('history-recommendstions/', views.HistoryBookRecommendation.as_view(), name='history-recommendstions'),
    path('live-search/', views.LiveSearchView.as_view(), name='live-search'),

]
