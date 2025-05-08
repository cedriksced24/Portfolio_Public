from django.db import models
from ckeditor.fields import RichTextField


# Model for a blog post
class Post(models.Model):
    title = models.CharField(max_length=200)
    content = RichTextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    order = models.IntegerField(default=0)

    # Returns the post title
    def __str__(self):
        return self.title


# Model for a book
class Book(models.Model):
    title = models.CharField(max_length=200)

    # Returns the book title
    def __str__(self):
        return self.title


# Model for a book page
class Page(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="pages")
    title = models.CharField(max_length=200)
    content = models.TextField()
    order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        # Returns book and page title
        return f"{self.book.title} – {self.title}"
