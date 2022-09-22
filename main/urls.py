from . import views
from django.urls import path


urlpatterns = [
    path('', views.home_page, name='home'),
    path('new/', views.post_create, name='new'),
    path('<slug:slug>/update', views.post_update, name='update'),
    path('posts/<type>/', views.PostList.as_view(), name='posts'),
    path('<slug:slug>/', views.PostFull.as_view(), name='full'),
]
