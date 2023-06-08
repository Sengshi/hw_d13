from django.urls import path
from .views import IndexView, auth_code

urlpatterns = [
    path('', IndexView.as_view(), name='account_profile'),
    path('auth_code', auth_code, name='auth_code'),

]
