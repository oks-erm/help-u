"""
Tests for models.py of main app.
"""
import time
from io import BytesIO
from datetime import datetime
from django.utils import timezone
from django.test import TestCase
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from django.db.models import (ForeignKey, CharField, DateTimeField,
                              BooleanField, EmailField)
from django.db import IntegrityError
from django.core.files.uploadedfile import InMemoryUploadedFile
from PIL import Image
from .models import UserProfile, CustomUser, Post, Comment, ContactFormMessage


im = Image.new(mode='RGB', size=(200, 200))
im_io = BytesIO()
im.save(im_io, 'JPEG')
im_io.seek(0)
image = InMemoryUploadedFile(
    im_io, None, 'random-name.jpg', 'image/jpeg', len(im_io.getvalue()), None
)


class PostUserCreatedSignalTestCase(TestCase):
    """
    Test user_created signal is handled correctly.
    """

    def test_user_profile_created(self):
        """
        Test UserProfile is created when user is saved.
        """
        user = CustomUser.objects.create(
            email='test@example.com',
            first_name='Test',
            last_name='User',
            password='testpass')
        # pylint: disable=no-member
        self.assertTrue(UserProfile.objects.filter(user=user).exists())


class UserProfileTestCase(TestCase):

    def setUp(self):
        self.user = CustomUser.objects.create(
            email='test@example.com',
            first_name='Test',
            last_name='User',
            password='testpass')
        self.user2 = CustomUser.objects.create(
            email='test2@example.com',
            first_name='Test2',
            last_name='User2',
            password='testpass2')
        # Check if the user already has an associated UserProfile object
        try:
            # pylint: disable=no-member
            self.user_profile = UserProfile.objects.get(user=self.user)
            self.user_profile2 = UserProfile.objects.get(user=self.user2)
        except UserProfile.DoesNotExist:
            # If not, create a new UserProfile object
            # pylint: disable=no-member
            self.user_profile = UserProfile.objects.create(
                user=self.user,
                languages='English',
                userpic=image,
                country='US',
                city='New York')
            self.user_profile2 = UserProfile.objects.create(
                user=self.user,
                languages='English',
                country='US',
                city='New York')

    def test_user_profile_str(self):
        """
        Test that the string representation of
        a user profile is the user's first and last name.
        """
        self.assertEqual(str(self.user_profile), 'Test User')

    def test_thumbnail_preview(self):
        """
        Test the thumbnail_preview method to make sure
        it returns the correct HTML tag with the correct image URL.
        """
        self.assertEqual(self.user_profile.thumbnail_preview,
                         '<img src="{}" width="auto" height="400" />'.format(
                            self.user_profile.userpic.url))

    def test_userpic_default(self):
        """
        Test that the default value for userpic is 'placeholder'.
        """
        # pylint: disable=no-member, disable=protected-access
        field = UserProfile._meta.get_field('userpic')
        self.assertIn('placeholder', field.default)

    def test_bio_default(self):
        """
        Test that the default value for bio is an empty string.
        """
        self.assertEqual(self.user_profile.bio, '')

    def test_languages_max_length(self):
        """
        Test that the languages field has a maximum
        length of 200 characters.
        """
        self.user_profile.languages = 'a' * 201
        self.user_profile.country = "PT"
        try:
            self.assertFalse(self.user_profile.full_clean())
        except ValidationError:
            pass


class CustomUserTests(TestCase):

    def test_username_field(self):
        """
        Test that the username field is set to 'email'.
        """
        self.assertEqual(get_user_model().USERNAME_FIELD, 'email')

    def test_required_fields(self):
        """
        Test that the required fields are ['first_name', 'last_name'].
        """
        self.assertEqual(get_user_model().REQUIRED_FIELDS,
                         ['first_name', 'last_name'])

    def test_str_representation(self):
        """
        Test that the string representation of
        a user is their first and last name.
        """
        user = get_user_model().objects.create_user(
            email='test@example.com',
            password='password',
            first_name='Test',
            last_name='User'
        )
        self.assertEqual(str(user), 'Test User')


class PostTestCase(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create(
            email='test@example.com',
            first_name='Test',
            last_name='User',
            password='testpass')
        # Check if the user already has an associated UserProfile object
        try:
            # pylint: disable=no-member
            self.user_profile = UserProfile.objects.get(user=self.user)
        except UserProfile.DoesNotExist:
            # If not, create a new UserProfile object
            # pylint: disable=no-member
            self.user_profile = UserProfile.objects.create(
                user=self.user,
                languages='English',
                country='US',
                city='New York')
        # pylint: disable=no-member
        self.post = Post.objects.create(
            author=self.user_profile, title='Test Post',
            image=image, text='This is a test post.', country='US',
            city='New York', area='Manhattan', status=0, relevance=1,
            type='offer', category='services'
        )
        self.post2 = Post.objects.create(
            author=self.user_profile, title='test post',
            image=image, text='This is a test post.', country='US',
            city='New York', area='Manhattan', status=0, relevance=1,
            type='offer', category='services'
        )

    def test_title_field(self):
        """
        Test that the title field has correct properties.
        """
        # pylint: disable=no-member, disable=protected-access
        field = Post._meta.get_field('title')
        self.assertEqual(field.verbose_name, 'title')
        self.assertEqual(field.max_length, 200)
        self.assertTrue(field.unique)

    def test_text_field(self):
        """
        Test that the text field has correct properties.
        """
        # pylint: disable=no-member, disable=protected-access
        field = Post._meta.get_field('text')
        self.assertEqual(field.verbose_name, 'text')
        self.assertTrue(field.blank)

    def test_country_field(self):
        """
        Test that the country field has correct properties.
        """
        # pylint: disable=no-member, disable=protected-access
        field = Post._meta.get_field('country')
        self.assertEqual(field.verbose_name, 'country')
        self.assertFalse(field.blank)

    def test_city_field(self):
        """
        Test that the city field has correct properties.
        """
        # pylint: disable=no-member, disable=protected-access
        field = Post._meta.get_field('city')
        self.assertEqual(field.verbose_name, 'city')
        self.assertFalse(field.blank)

    def test_area_field(self):
        """
        Test that the area field has correct properties.
        """
        # pylint: disable=no-member, disable=protected-access
        field = Post._meta.get_field('area')
        self.assertEqual(field.verbose_name, 'area')
        self.assertTrue(field.blank)

    def test_post_str(self):
        """
        Test that the __str__ method of the Post model
        returns the title of the post.
        """
        self.assertEqual(str(self.post), 'Test Post')

    def test_post_get_absolute_url(self):
        """
        Test that the get_absolute_url method of the
        Post model returns the correct URL for the post.
        """
        self.assertEqual(self.post.get_absolute_url(), f'/{self.post.slug}/')

    def test_post_save_method(self):
        """
        Test that the save method of the Post model correctly
        sets the slug field if it is not already set.
        """
        # pylint: disable=no-member
        post = Post.objects.create(
            author=self.user_profile, title='Test Post 2', image='placeholder',
            text='This is another test post.', country='US', city='New York',
            area='Manhattan', status=0, relevance=1, type='offer',
            category='services'
        )
        self.assertIsNotNone(post.slug)
        self.assertFalse(self.post.slug == self.post2.slug)

    def test_image_default(self):
        """
        Test that the default value for image is 'placeholder'.
        """
        # pylint: disable=no-member, disable=protected-access
        field = Post._meta.get_field('image')
        self.assertEqual(field.default, 'placeholder')

    def test_image_thumbnail_preview(self):
        """
        Test that the thumbnail_preview property returns an
        image tag with the correct URL for the post's image.
        """
        self.assertIn('<img src="{}" width="auto" height="400" />'.format(
            self.post.image.url), self.post.thumbnail_preview)

    def test_image_thumbnail_preview_no_image(self):
        """
        Test that the thumbnail_preview property returns
        an empty string if the post has no image.
        """
        self.post.image = None
        self.assertEqual(self.post.thumbnail_preview, '')

    def test_status_choices(self):
        """
        Get the 'status' field from the Post model.
        """
        # pylint: disable=no-member, disable=protected-access
        field = Post._meta.get_field('status')
        self.assertEqual(field.choices, (
            (0, 'Pending'),
            (1, 'Approved'),
        ))

    def test_relevance_choices(self):
        """
        Test that the relevance field has the correct choices.
        """
        # pylint: disable=no-member, disable=protected-access
        field = Post._meta.get_field('relevance')
        self.assertEqual(field.choices, ((0, "Closed"), (1, "Open")))

    def test_created_on_field(self):
        """
        Test that the created_on field is set to the current
        date and time when a new post is created.
        """
        # pylint: disable=no-member
        post = Post.objects.create(
            author=self.user_profile,
            title='Test Post' + str(int(time.time())),
            slug='test-post' + str(int(time.time())),
            country='US',
            city='New York',
            type='offer',
            category='help'
        )
        self.assertAlmostEqual(
            post.created_on, timezone.now(),
            delta=timezone.timedelta(seconds=1))

    def test_updated_on_field(self):
        """Test that the updated_on field is set to the
        current date and time when an existing post is updated.
        """
        self.post.title = 'Updated Test Post'
        self.post.save()
        self.assertAlmostEqual(
            self.post.updated_on, timezone.now(),
            delta=timezone.timedelta(seconds=1))

    def test_favourite_field(self):
        """
        Test that the favourite field is a many-to-many field
        that relates to the UserProfile model.
        """
        # pylint: disable=no-member, disable=protected-access
        field = Post._meta.get_field('favourite')
        self.assertEqual(field.related_model, UserProfile)
        self.assertEqual(field.many_to_many, True)

    def test_title_unique(self):
        """
        Test that the title field is unique and that an error
        is raised when trying to create a post with a duplicate title.
        """
        with self.assertRaises(IntegrityError):
            # pylint: disable=no-member
            Post.objects.create(
                author=self.user_profile,
                title=self.post.title,  # duplicate title
                slug='unique-slug',
                country='US',
                city='New York',
                type='offer',
                category='help'
            )

    def test_slug_unique(self):
        """
        Test that the slug field is unique and that an error
        is raised when trying to create a post with a duplicate slug.
        """
        with self.assertRaises(IntegrityError):
            # pylint: disable=no-member
            Post.objects.create(
                author=self.user_profile,
                title='Unique Title',
                slug=self.post.slug,  # duplicate slug
                country='US',
                city='New York',
                type='offer',
                category='help'
            )


class CommentTestCase(TestCase):

    def setUp(self):
        self.user = CustomUser.objects.create(
            email='test@example.com',
            first_name='Test',
            last_name='User',
            password='testpass')
        # Check if the user already has an associated UserProfile object
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
                country='US',
                city='New York')
        # pylint: disable=no-member
        self.post = Post.objects.create(
            author=self.user_profile, title='Test Post',
            image=image, text='This is a test post.', country='US',
            city='New York', area='Manhattan', status=1, relevance=1,
            type='offer', category='services'
        )
        # pylint: disable=no-member
        self.comment = Comment.objects.create(
            post=self.post, user=self.user_profile,
            body='Test comment'
        )

    def test_comment_str(self):
        """
        Test that the str method of the Comment model
        returns the correct string representation.
        """
        self.assertEqual(str(self.comment),
                         'Comment Test comment by Test User')

    def test_approved_field(self):
        """
        Test that the approved field of the Comment model
        has the correct default value.
        """
        self.assertFalse(self.comment.approved)

    def test_post_field(self):
        """
        Test that the post field of the Comment model is a
        ForeignKey field to the Post model.
        """
        # pylint: disable=protected-access
        field = self.comment._meta.get_field('post')
        self.assertIsInstance(field, ForeignKey)
        self.assertEqual(field.related_model, Post)

    def test_user_field(self):
        """
        Test that the user field of the Comment model is a
        ForeignKey field to the UserProfile model.
        """
        # pylint: disable=protected-access
        field = self.comment._meta.get_field('user')
        self.assertIsInstance(field, ForeignKey)
        self.assertEqual(field.related_model, UserProfile)

    def test_comment_creation(self):
        """
        Test if the instance is created correctly.
        """
        self.assertEqual(self.comment.post, self.post)
        self.assertEqual(self.comment.user, self.user_profile)
        self.assertEqual(self.comment.body, 'Test comment')
        self.assertTrue(isinstance(self.comment.created_on, datetime))
        self.assertFalse(self.comment.approved)

    def test_approve_comment(self):
        """
        Test approving a comment.
        """
        self.assertFalse(self.comment.approved)
        self.comment.approved = True
        self.comment.save()
        # pylint: disable=no-member
        self.assertTrue(Comment.objects.get(pk=self.comment.pk).approved)


class ContactFormMessageTestCase(TestCase):

    def setUp(self):
        # pylint: disable=no-member
        self.form_message = ContactFormMessage.objects.create(
            name='John',
            email='john@example.com',
            subject='Test message',
            message='This is a test message',
        )

    def test_name_field(self):
        """
        Test that the name field is a CharField with
        the correct max length.
        """
        # pylint: disable=no-member, disable=protected-access
        field = ContactFormMessage._meta.get_field("name")
        self.assertIsInstance(field, CharField)
        self.assertEqual(field.max_length, 50)
        self.assertFalse(field.blank)

    def test_email_field(self):
        """
        Test that the email field has correct properties.
        """
        # pylint: disable=no-member, disable=protected-access
        field = ContactFormMessage._meta.get_field("email")
        self.assertIsInstance(field, EmailField)
        self.assertEqual(field.max_length, 50)

    def test_subject_field(self):
        """
        Test that the subject field is a CharField with
        the correct max length.
        """
        # pylint: disable=no-member, disable=protected-access
        field = ContactFormMessage._meta.get_field("subject")
        self.assertIsInstance(field, CharField)
        self.assertEqual(field.max_length, 80)
        self.assertFalse(field.blank)

    def test_message_field(self):
        """
        Test that the message field is a CharField
        with the correct max length.
        """
        # pylint: disable=no-member, disable=protected-access
        field = ContactFormMessage._meta.get_field("message")
        self.assertIsInstance(field, CharField)
        self.assertEqual(field.max_length, 2000)
        self.assertFalse(field.blank)

    def test_date_field(self):
        """
        Test that the date field is a DateTimeField with auto_now=True.
        """
        # pylint: disable=no-member, disable=protected-access
        field = ContactFormMessage._meta.get_field("date")
        self.assertIsInstance(field, DateTimeField)
        self.assertTrue(field.auto_now)

    def test_responded_field(self):
        """
        Test that the responded field is a BooleanField.
        """
        # pylint: disable=no-member, disable=protected-access
        field = ContactFormMessage._meta.get_field('responded')
        self.assertIsInstance(field, BooleanField)
        self.assertEqual(field.choices, ((0, "No"), (1, "Yes")))
        self.assertEqual(field.default, 0)

    def test_str_method(self):
        """
        Test that the string representation of
        a contact form message.
        """
        self.assertEqual(str(self.form_message),
                         "from John | subject: Test message")
