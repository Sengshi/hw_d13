from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import EmailMultiAlternatives
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView
from django.contrib.auth.models import User

from .forms import PostForm, RetryForm
from .models import Post, Category, Retry


class BoardList(ListView):
    model = Post
    template_name = 'board_all.html'
    context_object_name = 'posts'
    queryset = Post.objects.order_by('-date_create')
    paginate_by = 10


class PostDetail(DetailView):
    model = Post
    template_name = 'post_detail.html'
    context_object_name = 'post_detail'


class PostAdd(LoginRequiredMixin, CreateView):
    template_name = 'post_add.html'
    form_class = PostForm

    def post(self, request, *args, **kwargs):
        post = Post(
            author=User(request.user.id),
            title=request.POST['title'],
            post=request.POST['post'],
            category_id=Category(request.POST['category_id']),
        )
        post.save()
        return redirect('/')


class RetryAdd(LoginRequiredMixin, CreateView):
    permission_required = ('board.add_retry',)
    template_name = 'retry_add.html'
    form_class = RetryForm

    def post(self, request, *args, **kwargs):
        post = Retry(
            user=User(request.user.id),
            retries=request.POST['retries'],
            post=Post(id=self.kwargs.get('pk')),
        )
        post.save()
        return redirect('/')


class PostDelete(LoginRequiredMixin, DeleteView):
    template_name = 'post_delete.html'
    queryset = Post.objects.all()
    success_url = '/'


class PostEdit(LoginRequiredMixin, UpdateView):
    template_name = 'post_add.html'
    form_class = PostForm
    success_url = '/'

    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)


@login_required
def retry_false(request, **kwargs):
    retry = Retry.objects.get(id=kwargs['pk'])
    retry.delete()
    recipient = [retry.user.email]
    html_content = render_to_string(
                'retry_delete.html',
                {
                    'post': retry,
                    'author': retry.user,
                }
            )
    msg = EmailMultiAlternatives(
                subject=f'{retry.post.author}',
                body=retry.retries,
                from_email='testpysend@mail.ru',
                to=recipient,
            )
    msg.attach_alternative(html_content, "text/html")
    print(html_content)
    msg.send()
    return redirect('/sign/')


@login_required
def retry_true(request, **kwargs):
    retry = Retry.objects.get(id=kwargs['pk'])
    retry.retry_enable = True
    retry.save()
    recipient = [retry.user.email]
    html_content = render_to_string(
                'retry_allowed.html',
                {
                    'post': retry,
                    'author': retry.user,
                }
            )
    msg = EmailMultiAlternatives(
                subject=f'{retry.post.author}',
                body=retry.retries,
                from_email='testpysend@mail.ru',
                to=recipient,
            )
    msg.attach_alternative(html_content, "text/html")
    print(html_content)
    msg.send()

    return redirect('/sign/')
