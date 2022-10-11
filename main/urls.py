from . import views
from django.urls import path


app_name = "main"


urlpatterns = [
    path('', views.LandingView.as_view(), name='home'),
    path('afterlogin/', views.after_login, name='after_login'),
    path('new/', views.PostCreateView.as_view(), name='new'),
    path('<slug:slug>/update/', views.PostUpdateView.as_view(), name='update'),
    path('<slug:slug>/delete/', views.PostDeleteView.as_view(), name='delete'),
    path('posts_list/<type>/', views.PostList.as_view(), name='posts_list'),
    path('<slug:slug>/', views.PostFull.as_view(), name='full'),
    path('<slug:slug>/bookmark', views.BookMark.as_view(), name='bookmark'),
]
