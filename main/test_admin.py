from unittest.mock import patch
from django.test import TestCase
from django.urls import reverse
from django.contrib import admin
from django.http import HttpRequest
from django.core.files.uploadedfile import SimpleUploadedFile
from .admin import CustomUserAdmin, UserProfileAdmin, CommentAdmin, PostAdmin, ContactFormAdmin
from .models import UserProfile, CustomUser, Post, Comment, ContactFormMessage


class CustomUserAdminTestCase(TestCase):
    """
    Test CustomUserAdmin class.
    """
    def setUp(self):
        self.admin = CustomUserAdmin(CustomUser, admin.site)
        self.test_users = [
            CustomUser.objects.create(
                first_name='John', last_name='Doe', email='jd@test.com'),
            CustomUser.objects.create(
                first_name='Jane', last_name='Doe', email='janed@test.com'),
            CustomUser.objects.create(
                first_name='Lou', last_name='Sirr', email='lousirr@test.com'),
        ]

    def test_fields_attribute(self):
        """
        Test that the admin for CustomUser has correct fields.
        """
        expected_fields = (('first_name', 'last_name'),
                           ('email', 'is_staff'),
                           ('date_joined', 'last_login'),
                           'user_permissions',
                           'groups',
                           'is_active')
        self.assertEqual(self.admin.fields, expected_fields)

    def test_list_display_attribute(self):
        """
        Test that the list_display attribute is set correctly.
        """
        expected_list_display = ('name', 'email', 'id', 'is_active')
        self.assertEqual(self.admin.list_display, expected_list_display)

    def test_list_filter_attribute(self):
        """
        Test that the list_filter attribute is set correctly.
        """
        expected_list_filter = ('is_staff', 'date_joined',
                                'last_login', 'is_active')
        self.assertEqual(self.admin.list_filter, expected_list_filter)

    def test_search_fields_attribute(self):
        """
        Test that the search_fields attribute is set correctly.
        """
        expected_search_fields = ('first_name', 'last_name', 'email')
        self.assertEqual(self.admin.search_fields, expected_search_fields)

    def test_name_method(self):
        for user in self.test_users:
            expected_name = f"{user.first_name} {user.last_name}"
            name = self.admin.name(user)
            self.assertEqual(name, expected_name)

    def test_id_method(self):
        for user in self.test_users:
            expected_id = f"{user.id}"
            user_id = self.admin.id(user)
            self.assertEqual(user_id, expected_id)


class UserProfileAdminTestCase(TestCase):
    """
    Test UserProfileAdmin class.
    """
    def setUp(self):
        self.admin = UserProfileAdmin(UserProfile, admin.site)
        self.test_users = [
            CustomUser.objects.create(
                first_name='John', last_name='Doe', email='jd@test.com'),
            CustomUser.objects.create(
                first_name='Jane', last_name='Doe', email='janed@test.com'),
            CustomUser.objects.create(
                first_name='Lou', last_name='Sirr', email='lousirr@test.com'),
        ]
        try:
            self.test_profiles = [
                # pylint: disable=no-member
                UserProfile.objects.get(user=user) for user in self.test_users]
        # pylint: disable=no-member
        except UserProfile.DoesNotExist:
            self.test_profiles = [
                # pylint: disable=no-member
                UserProfile.objects.create(
                    user=user,
                    country='PT',
                    languages='English') for user in self.test_users
            ]

    def test_fields_attribute(self):
        """
        Test that the admin for User Profile has correct fields.
        """
        expected_fields = (('user', 'languages'),
                           ('country', 'city'),
                           'thumbnail_preview',
                           'userpic',
                           'bio')
        self.assertEqual(self.admin.fields, expected_fields)

    def test_list_display_attribute(self):
        """
        Test that the list_display attribute is set correctly.
        """
        expected_list_display = (
            'user', 'country', 'languages', 'active', 'id')
        self.assertEqual(self.admin.list_display, expected_list_display)

    def test_readonly_fields_attribute(self):
        """
        Test that the readonly_fields attribute is set correctly.
        """
        expected = ('thumbnail_preview',)
        self.assertEqual(self.admin.readonly_fields, expected)

    def test_search_fields_attribute(self):
        """
        Test that the search_fields attribute is set correctly.
        """
        expected_search_fields = (
            'user', 'bio', 'country', 'city', 'languages')
        self.assertEqual(self.admin.search_fields, expected_search_fields)

    def test_id_method(self):
        for user_profile in self.test_profiles:
            expected_id = f"{user_profile.id}"
            user_id = self.admin.id(user_profile)
            self.assertEqual(user_id, expected_id)

    def test_active_function(self):
        for user_profile in self.test_profiles:
            self.assertEqual(self.admin.active(user_profile), 'True')

        for user_profile in self.test_profiles:
            user_profile.user.is_active = False
            self.assertEqual(self.admin.active(user_profile), 'False')

    def test_thumbnail_preview_function(self):
        for user_profile in self.test_profiles:
            self.assertEqual(self.admin.thumbnail_preview(
                user_profile), user_profile.thumbnail_preview)


class CommentAdminTestCase(TestCase):
    """
    Test CommentAdmin class.
    """
    def setUp(self):
        self.admin = CommentAdmin(Comment, admin.site)
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
        # pylint: disable=no-member
        self.post = Post.objects.create(
            author=self.user_profile, title='Test Post', slug='test-post',
            image='image', text='This is a test post.', country='PT',
            city='Lisbon', area='Chiado', status=1, relevance=1,
            type='give', category='items')
        self.comment_1 = Comment.objects.create(
            user=self.user_profile, post=self.post, body='Test comment 1',
            approved=False,
        )
        self.comment_2 = Comment.objects.create(
            user=self.user_profile, post=self.post, body='Test comment 2',
            approved=False,
        )
        self.comment_3 = Comment.objects.create(
            user=self.user_profile, post=self.post, body='Test comment 3',
            approved=True,
        )

    def test_fields_attribute(self):
        """
        Test that the admin for Comment has correct fields.
        """
        expected_fields = ('user',
                           'created_on',
                           'post',
                           'body',
                           'approved')
        self.assertEqual(self.admin.fields, expected_fields)

    def test_list_display_attribute(self):
        """
        Test that the list_display attribute is set correctly.
        """
        expected_list_display = ('user', 'created_on', 'approved')
        self.assertEqual(self.admin.list_display, expected_list_display)

    def test_readonly_fields_attribute(self):
        """
        Test that the readonly_fields attribute is set correctly.
        """
        expected = ('user', 'post', 'created_on')
        self.assertEqual(self.admin.readonly_fields, expected)

    def test_list_filter_attribute(self):
        """
        Test that the list_filter attribute is set correctly.
        """
        expected_list_filter = ('approved', 'created_on')
        self.assertEqual(self.admin.list_filter, expected_list_filter)

    def test_search_fields_attribute(self):
        """
        Test that the search_fields attribute is set correctly.
        """
        expected_search_fields = ('user', 'body')
        self.assertEqual(self.admin.search_fields, expected_search_fields)

    def test_approve_comments(self):
        """
        Test that the approve_comments method correctly updates
        the status of the selected comments to True.
        """
        request = HttpRequest()
        # pylint: disable=no-member
        queryset = Comment.objects.filter(approved=False)
        self.admin.approve_comments(request, queryset)
        # pylint: disable=no-member
        self.assertTrue(Comment.objects.get(pk=self.comment_1.pk).approved)
        # pylint: disable=no-member
        self.assertTrue(Comment.objects.get(pk=self.comment_2.pk).approved)
        # pylint: disable=no-member
        self.assertTrue(Comment.objects.get(pk=self.comment_3.pk).approved)


class PostAdminTestCase(TestCase):
    """
    Test PostAdmin class.
    """
    def setUp(self):
        image = SimpleUploadedFile('test_image', bytes(), 'image/jpeg')
        image.url = "http://"
        self.admin = PostAdmin(Post, admin.site)
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
        with patch('cloudinary.uploader.upload'):
            # pylint: disable=no-member
            self.post_1 = Post.objects.create(
                author=self.user_profile, title='Test Post 1',
                image=image, text='This is a test post.', country='PT',
                city='Lisbon', area='Chiado', status=0, relevance=1,
                type='give', category='items')
            # pylint: disable=no-member
            self.post_2 = Post.objects.create(
                author=self.user_profile, title='Test Post 2',
                image=image, text='This is a test post.', country='PT',
                city='Lisbon', area='Chiado', status=0, relevance=1,
                type='give', category='items')
            # pylint: disable=no-member
            self.post_3 = Post.objects.create(
                author=self.user_profile, title='Test Post 3',
                image=image, text='This is a test post.', country='PT',
                city='Lisbon', area='Chiado', status=1, relevance=1,
                type='give', category='items')

    def test_fields_attribute(self):
        """
        Test that the admin for Post has correct fields.
        """
        expected_fields = ('author',
                           'title',
                           'image',
                           'thumbnail_preview',
                           'text',
                           ('country', 'city'),
                           'area',
                           ('status', 'relevance'),
                           ('type', 'category'))
        self.assertEqual(self.admin.fields, expected_fields)

    def test_list_display_attribute(self):
        """
        Test that the list_display attribute is set correctly.
        """
        expected_list_display = ('title', 'author', 'country',
                                 'created_on', 'type', 'status')
        self.assertEqual(self.admin.list_display, expected_list_display)

    def test_readonly_fields_attribute(self):
        """
        Test that the readonly_fields attribute is set correctly.
        """
        expected = ('thumbnail_preview',)
        self.assertEqual(self.admin.readonly_fields, expected)

    def test_list_filter_attribute(self):
        """
        Test that the list_filter attribute is set correctly.
        """
        expected_list_filter = ('type', 'status', 'created_on')
        self.assertEqual(self.admin.list_filter, expected_list_filter)

    def test_search_fields_attribute(self):
        """
        Test that the search_fields attribute is set correctly.
        """
        expected_search_fields = ('name', 'email', 'author', 'title')
        self.assertEqual(self.admin.search_fields, expected_search_fields)

    def test_approve_posts(self):
        """
        Test that the approve_comments method correctly updates
        the status of the selected comments to True.
        """
        request = HttpRequest()
        # pylint: disable=no-member
        queryset = Post.objects.filter(status=0)
        self.admin.approve_posts(request, queryset)
        # pylint: disable=no-member
        self.assertTrue(Post.objects.get(pk=self.post_1.pk).status)
        # pylint: disable=no-member
        self.assertTrue(Post.objects.get(pk=self.post_2.pk).status)
        # pylint: disable=no-member
        self.assertTrue(Post.objects.get(pk=self.post_3.pk).status)

    def test_thumbnail_preview_function(self):
        self.assertEqual(self.admin.thumbnail_preview(
            self.post_1), self.post_1.thumbnail_preview)
        self.assertEqual(self.admin.thumbnail_preview(
            self.post_2), self.post_2.thumbnail_preview)


class ContactFormAdminTestCase(TestCase):
    """
    Test ContactFormAdmin class.
    """
    def setUp(self):
        self.admin = ContactFormAdmin(ContactFormMessage, admin.site)

    def test_fields_attribute(self):
        """
        Test that the admin for Contact Form has correct fields.
        """
        expected_fields = (('name', 'email'),
                           'subject',
                           'message',
                           'date',
                           'responded')
        self.assertEqual(self.admin.fields, expected_fields)

    def test_list_display_attribute(self):
        """
        Test that the list_display attribute is set correctly.
        """
        expected_list_display = (
            'subject', 'name', 'email', 'date', 'responded')
        self.assertEqual(self.admin.list_display, expected_list_display)

    def test_readonly_fields_attribute(self):
        """
        Test that the readonly_fields attribute is set correctly.
        """
        expected = ('date',)
        self.assertEqual(self.admin.readonly_fields, expected)

    def test_list_filter_attribute(self):
        """
        Test that the list_filter attribute is set correctly.
        """
        expected_list_filter = ('date', 'responded')
        self.assertEqual(self.admin.list_filter, expected_list_filter)

    def test_search_fields_attribute(self):
        """
        Test that the search_fields attribute is set correctly.
        """
        expected_search_fields = ('name', 'email', 'subject', 'message')
        self.assertEqual(self.admin.search_fields, expected_search_fields)

    def test_mark_as_responded(self):
        """
        Test that the approve_comments method correctly updates
        the status of the selected comments to True.
        """
        # pylint: disable=no-member
        form_1 = ContactFormMessage.objects.create(
            name='name',
            email='email',
            subject='subject',
            message='message',
        )
        # pylint: disable=no-member
        form_2 = ContactFormMessage.objects.create(
            name='name2',
            email='email2',
            subject='subject2',
            message='message2',
        )
        request = HttpRequest()
        # pylint: disable=no-member
        queryset = ContactFormMessage.objects.filter(responded=0)
        self.admin.mark_as_responded(request, queryset)
        # pylint: disable=no-member
        self.assertTrue(ContactFormMessage.objects.get(
            pk=form_1.pk).responded)
        # pylint: disable=no-member
        self.assertTrue(ContactFormMessage.objects.get(
            pk=form_2.pk).responded)

