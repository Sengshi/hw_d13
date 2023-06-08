from django.forms import ModelForm
from .models import Post, Retry


class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'post', 'category_id', )


class RetryForm(ModelForm):
    class Meta:
        model = Retry
        fields = ['retries', ]
