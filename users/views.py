from django.shortcuts import render, redirect
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import reverse
from main.models import UserProfile
from .forms import ProfileForm


class ProfileCreateView(LoginRequiredMixin, generic.CreateView):
    template_name = "create_user_profile.html"
    form_class = ProfileForm 

    def get_success_url(self):
        return reverse('users:profile', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.save()
        return super(ProfileCreateView, self).form_valid(form)


class UserProfileDetailView(LoginRequiredMixin, generic.DetailView):
    template_name = "profile.html"
    context_object_name = "profile"

    def get_queryset(self):
        queryset = UserProfile.objects.all()
        return queryset


class UserProfileUpdateView(LoginRequiredMixin, generic.UpdateView):
    template_name = "update_profile.html"
    form_class = ProfileForm
    queryset = UserProfile.objects.all()

    def get_success_url(self):
        return reverse('users:profile', kwargs={'pk': self.request.user.userprofile.id})

    def form_valid(self, form):
        form.save()
        return super(UserProfileUpdateView, self).form_valid(form)