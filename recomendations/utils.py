import difflib
from books.models import Book

def get_similar_words(word):
    title_words = Book.objects.values_list('title', flat=True)
    author_words = Book.objects.values_list('author', flat=True)
    all_words = title_words.union(author_words)
    similar_words = difflib.get_close_matches(word, all_words, n=5, cutoff=0.6)
    return similar_words
