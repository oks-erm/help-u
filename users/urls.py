from django.urls import path
from .views import (ProfileCreateView, UserProfileDetailView,
                    UserProfileUpdateView)

app_name = 'users'

urlpatterns = [
    path('create/', ProfileCreateView.as_view(), name='create-profile'),
    path('profile/<pk>', UserProfileDetailView.as_view(), name='profile'),
    path('profile/update/<pk>', UserProfileUpdateView.as_view(),
         name='update_profile'),
]
