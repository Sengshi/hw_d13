from django.urls import path
from django.views.decorators.cache import cache_page

from .views import BoardList, PostDetail, PostAdd, PostDelete, PostEdit, RetryAdd, retry_true, retry_false

urlpatterns = [
    path('', BoardList.as_view()),
    path('<int:pk>/', PostDetail.as_view(), name='post_detail'),
    path('add/', PostAdd.as_view(), name='post_add'),
    path('retry_add/<int:pk>/', RetryAdd.as_view(), name='retry_add'),
    path('<int:pk>/retry_true', retry_true, name='retry_true'),
    path('<int:pk>/retry_false', retry_false, name='retry_false'),
    path('<int:pk>/delete', PostDelete.as_view(), name='post_delete'),
    path('<int:pk>/edit', PostEdit.as_view(), name='post_update'),
]
