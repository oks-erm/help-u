from . import views
from django.urls import path


urlpatterns = [
    path('', views.home_page, name='home'),
    path('posts/', views.PostList.as_view(), name='posts'),
    path('<slug:slug>/', views.PostFull.as_view(), name='full'),
]
