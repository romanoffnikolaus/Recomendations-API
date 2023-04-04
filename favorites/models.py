from django.db import models
from django.contrib.auth import get_user_model

from books.models import Book


User = get_user_model()


class Favorites(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorite')
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='favorite')
    in_favorites = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f'{self.book} in favorites of user: {self.user.email}'
    

class History(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='history')
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='history')
    viewed_on = models.DateTimeField(auto_now_add=True)