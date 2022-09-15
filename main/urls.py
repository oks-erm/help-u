from . import views
from django.urls import path


urlpatterns = [
    path('', views.home_page, name='home'),
    path('posts/', views.posts_list, name='posts'),
]
