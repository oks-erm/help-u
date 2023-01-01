"""
Tests for views.py of main app.
"""
from unittest.mock import patch, Mock
from io import BytesIO
from django.test import TestCase
from django.http import HttpRequest
from django.urls import reverse
from django.core.files.uploadedfile import InMemoryUploadedFile
from PIL import Image
from main.models import UserProfile, CustomUser
from .forms import ProfileForm
from .views import (ProfileCreateView, UserProfileDetailView,
                    UserProfileUpdateView)


im = Image.new(mode='RGB', size=(200, 200))
im_io = BytesIO()
im.save(im_io, 'JPEG')
im_io.seek(0)
image = InMemoryUploadedFile(
    im_io, None, 'random-name.jpg', 'image/jpeg', len(im_io.getvalue()), None
)
file_dict = {'userpic': image}


class ProfileCreateViewTestCase(TestCase):
    """
    Tests ProfileCreateView class.
    """
    def setUp(self):
        self.url = reverse('users:create-profile')
        self.user = CustomUser.objects.create(
            email='test@example.com',
            first_name='Test',
            last_name='User',
            password='testpass',
            is_active=True)
        self.form_data = {
            'languages': 'English',
            'userpic': image,
            'country': 'PT',
            'city': 'Lisbon'
        }

    def test_view_redirects_to_login_page_for_unauthenticated_users(self):
        """
        Test that when an unauthenticated user tries to
        access the view, they are redirected to the login page.
        """
        response = self.client.get(self.url)

        self.assertRedirects(response, '/accounts/login/?next=' + self.url)

    def test_view_returns_200_for_authenticated_users(self):
        """
        Test that when an authenticated user tries to
        access the view, they receive a status code of 200.
        """
        self.client.force_login(user=self.user)
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)

    def test_get_success_url(self):
        """
        Test that the get_success_url method of the PostCreateView
        returns the correct URL.
        """
        self.client.force_login(user=self.user)
        view = ProfileCreateView()
        view.object = Mock()
        expected_url = reverse('users:profile', kwargs={'pk': view.object.pk})

        self.assertEqual(view.get_success_url(), expected_url)

    def test_form_valid_sets_author(self):
        """
        Test that the form_valid method correctly updates an existing post.
        """
        self.client.force_login(user=self.user)
        with patch('cloudinary.uploader.upload'):
            form = ProfileForm(
                # pylint: disable=no-member
                instance=UserProfile.objects.get(user=self.user),
                data=self.form_data, files=file_dict)
            print(form.errors)
            view = ProfileCreateView()
            view.request = HttpRequest()
            view.request.user = self.user
            print(form.errors)
            response = view.form_valid(form)
            self.assertEqual(response.status_code, 302)
            # pylint: disable=no-member
            self.assertEqual(UserProfile.objects.count(), 1)
            # pylint: disable=no-member
            profile = UserProfile.objects.first()
            self.assertEqual(profile.user, self.user)


class UserProfileUpdateViewTestCase(TestCase):
    """
    Tests ProfileUpdateView class.
    """
    def setUp(self):
        self.user = CustomUser.objects.create(
            email='test@example.com',
            first_name='Test',
            last_name='User',
            password='testpass',
            is_active=True)
        try:
            # pylint: disable=no-member
            self.user_profile = UserProfile.objects.get(user=self.user)
        # pylint: disable=no-member
        except UserProfile.DoesNotExist:
            # If not, create a new UserProfile object
            # pylint: disable=no-member
            self.user_profile = UserProfile.objects.create(
                user=self.user,
                languages='English',
                country='PT',
                city='Lisbon')
        self.url = reverse('users:update_profile', kwargs={
                           'pk': self.user_profile.pk})

    def test_view_redirects_to_login_page_for_unauthenticated_users(self):
        """
        Test that when an unauthenticated user tries to
        access the view, they are redirected to the login page.
        """
        response = self.client.get(self.url)

        self.assertRedirects(response, '/accounts/login/?next=' + self.url)

    def test_view_returns_200_for_authenticated_users(self):
        """
        Test that when an authenticated user tries to
        access the view, they receive a status code of 200.
        """
        self.client.force_login(user=self.user)
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)

    def test_form_valid_updates_post(self):
        """
        Test that the form_valid method
        correctly updates an existing post.
        """
        self.client.force_login(user=self.user)
        form = ProfileForm(instance=self.user_profile, data={
                              'languages': 'English',
                              'userpic': image,
                              'country': 'US',
                              'city': 'Los Angeles'
                              })
        with patch('cloudinary.uploader.upload'):
            self.assertTrue(form.is_valid())
        view = UserProfileUpdateView()
        view.object = self.user_profile
        view.request = HttpRequest()
        view.request.user = self.user
        response = view.form_valid(form)

        self.assertEqual(response.status_code,
                         # pylint: disable=bad-super-call
                         super(UserProfileUpdateView,
                               view).form_valid(form).status_code)
        # pylint: disable=no-member
        updated_profile = UserProfile.objects.get(id=self.user_profile.id)
        self.assertEqual(updated_profile.country, 'US')
        self.assertEqual(updated_profile.city, 'Los Angeles')

    def test_get_success_url(self):
        """
        Test that the get_success_url method of the PostCreateView
        returns the correct URL.
        """
        self.client.force_login(user=self.user)
        view = ProfileCreateView()
        view.object = Mock()
        expected_url = reverse('users:profile', kwargs={'pk': view.object.pk})

        self.assertEqual(view.get_success_url(), expected_url)


class UserProfileDetailTestCase(TestCase):
    """
    Tests UserProfileDetail view class.
    """
    def setUp(self):
        self.user = CustomUser.objects.create(
            email='test@example.com',
            first_name='Test',
            last_name='User',
            password='testpass',
            is_active=True)

        try:
            # pylint: disable=no-member
            self.user_profile = UserProfile.objects.get(user=self.user)
        # pylint: disable=no-member
        except UserProfile.DoesNotExist:
            # If not, create a new UserProfile object
            # pylint: disable=no-member
            self.user_profile = UserProfile.objects.create(
                user=self.user,
                languages='English',
                country='PT',
                city='Lisbon')
        self.url = reverse('users:profile', kwargs={
                           'pk': self.user_profile.pk})

    def test_view_redirects_to_login_page_for_unauthenticated_users(self):
        """
        Test that when an unauthenticated user tries to
        access the view, they are redirected to the login page.
        """
        response = self.client.get(self.url)

        self.assertRedirects(response, '/accounts/login/?next=' + self.url)

    def test_view_returns_200_for_authenticated_users(self):
        """
        Test that when an authenticated user tries to
        access the view, they receive a status code of 200.
        """
        self.client.force_login(user=self.user)
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)

    def test_get_queryset(self):
        """
        Test that the view only returns active posts.
        """
        self.client.force_login(user=self.user)
        view = UserProfileDetailView()
        queryset = view.get_queryset()
        # pylint: disable=no-member
        self.assertQuerysetEqual(UserProfile.objects.all(), queryset)
