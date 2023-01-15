"""
Views of the users app.
"""
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import reverse
from main.models import UserProfile
from .forms import ProfileForm


class ProfileCreateView(LoginRequiredMixin, generic.CreateView):
    """
    A view for creating User Profile.
    """
    template_name = "create_user_profile.html"
    form_class = ProfileForm

    def get_success_url(self):
        """
        Returns the URL to redirect to after a successful form submission.
        """
        return reverse('users:profile', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        """
        Saves the form if it is valid and redirects the user
        to the user profile page.
        """
        form.instance.user = self.request.user
        form.save()
        return super(ProfileCreateView, self).form_valid(form)


class UserProfileDetailView(LoginRequiredMixin, generic.DetailView):
    """
    A view for displaying User Profile in details.
    """
    template_name = "profile.html"
    context_object_name = "profile"

    def get_queryset(self):
        """
        Returns a queryset containing all user profiles.
        """
        # pylint: disable=no-member
        queryset = UserProfile.objects.all()
        return queryset


class UserProfileUpdateView(LoginRequiredMixin, generic.UpdateView):
    """
    A view for updating User Profile.
    """
    template_name = "update_profile.html"
    form_class = ProfileForm
    # pylint: disable=no-member
    queryset = UserProfile.objects.all()

    def get_success_url(self):
        """
        Returns the URL for the updated user profile page.
        """
        return reverse(
            'users:profile',
            kwargs={'pk': self.request.user.userprofile.id})

    def form_valid(self, form):
        """
        Saves the form and returns the
        superclass's form_valid method.
        """
        form.save()
        return super(UserProfileUpdateView, self).form_valid(form)
