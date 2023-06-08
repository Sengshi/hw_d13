from django.contrib.auth.models import User
from django.db import models
from ckeditor.fields import RichTextField


class Category(models.Model):
    category = models.CharField(max_length=255)

    def __str__(self):
        return self.category


class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author')
    title = models.CharField(max_length=255, null=False)
    post = RichTextField(null=False)
    category_id = models.ForeignKey(Category, on_delete=models.CASCADE, null=False)
    date_create = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    def get_author(self):
        return self.author.username

    def count_retries(self):
        return Retry.objects.filter(post=self.id).filter(retry_enable=True).count()


class Retry(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    retries = models.TextField(null=False)
    retry_enable = models.BooleanField(default=False)

