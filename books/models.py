from django.db import models
from slugify import slugify


class Genre(models.Model):
    genre = models.CharField(max_length=30, unique=True)
    slug = models.SlugField(max_length=30, primary_key=True, blank=True, unique=True)

    def __str__(self) -> str:
        return self.genre
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.genre)
        super().save()
    

class Book(models.Model):
    title = models.CharField(max_length=50, unique=True)
    genre = models.ManyToManyField(Genre, related_name='genres', blank=True)
    image = models.ImageField(upload_to='images/', blank=True)
    author = models.CharField(max_length=60)
    file = models.FileField(upload_to='books/', blank=True)
    year = models.SmallIntegerField()
    slug = models.SlugField(max_length=50, primary_key=True, blank=True, unique=True)
    added = models.DateField(auto_now_add=True)
    views = models.IntegerField(default=0)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save()
    
    def __str__(self) -> str:
        return self.title

