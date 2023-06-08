import random
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.core.mail import send_mail
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic import FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from board.models import Retry
from .forms import Auth_codeForm
from .models import UsersAuth


code_not_correct = str('')


class IndexView(LoginRequiredMixin, FormView):
    template_name = 'lk.html'
    form_class = Auth_codeForm

    def dispatch(self, request, *args, **kwargs):
        if UsersAuth.objects.filter(user=self.request.user).exists():
            return super().dispatch(request, *args, **kwargs)
        return HttpResponseRedirect(reverse('auth_code'))

    def form_valid(self, form, **kwargs):
        global code_not_correct
        if form.cleaned_data['code'] == UsersAuth.objects.get(user=self.request.user).code:
            Group.objects.get(name='AuthUsers').user_set.add(self.request.user)
        else:
            code_not_correct = "Введен неверный код подтверждения"
        return HttpResponseRedirect(reverse('account_profile'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['code_not_correct'] = code_not_correct
        if self.request.user.groups.filter(name='AuthUsers').exists():
            context['auth'] = True
        else:
            context['auth'] = False
        if not self.request.GET.get('q'):
            context['retryes'] = Retry.objects.filter(post__author=self.request.user.id)
        else:
            query = self.request.GET.get('q')
            context['retryes'] = Retry.objects.filter(
                Q(post__title__icontains=query)
            ).filter(post__author=self.request.user.id)
        return context


@login_required
def auth_code(request):
    global code_not_correct
    code_not_correct = ""

    if not UsersAuth.objects.filter(user=request.user).exists():
        add_user = UsersAuth()
        add_user.user = request.user
        add_user.save()

    user = UsersAuth.objects.get(user=request.user)
    user.code = random.randint(1000, 9999)
    user.save()
    send_mail(
        subject=f'BoardSF13: подтверждение e-mail',
        message=f'Доброго дня, {request.user}! Для подтверждения регистрации, введите код {user.code} на '
                f'странице регистрации\nhttp://127.0.0.1:8000/sign',
        from_email='testpysend@mail.ru',
        recipient_list=[request.user.email, ],
    )
    return HttpResponseRedirect(reverse('account_profile'))
