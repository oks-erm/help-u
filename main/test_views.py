"""
Tests for views.py of main app.
"""
from unittest.mock import patch, MagicMock, Mock
from io import BytesIO
from django.test import TestCase, RequestFactory, Client
from django.http import HttpRequest, HttpResponse
from django.urls import reverse
from django.template.exceptions import TemplateDoesNotExist
from django.core.files.uploadedfile import InMemoryUploadedFile
from PIL import Image
from messenger.models import Message, Conversation
from .forms import CreatePostForm
from .views import (LandingView, PostList, API_KEY, PostFull, PostCreateView,
                    PostUpdateView, PostDeleteView)
from .models import ContactFormMessage, Post, CustomUser, UserProfile, Comment


class LandingViewTestCase(TestCase):
    """
    Test LandingView class.
    """
    def setUp(self):
        self.request = HttpRequest()
        self.request.POST['name'] = 'Test User'
        self.request.POST['email'] = 'test@example.com'
        self.request.POST['subject'] = 'Test Subject'
        self.request.POST['message'] = 'Test Message'
        self.view = LandingView()

    def test_post_method(self):
        """
        Test that the post method correctly creates a
        ContactFormMessage object with the correct data.
        """
        self.view.post(self.request)
        # pylint: disable=no-member
        message = ContactFormMessage.objects.first()

        self.assertEqual(message.name, 'Test User')
        self.assertEqual(message.email, 'test@example.com')
        self.assertEqual(message.subject, 'Test Subject')
        self.assertEqual(message.message, 'Test Message')

    def test_post_method_response(self):
        """
        Test that the post method returns a status code of
        200 when the request method is POST.
        """
        self.request.method = 'POST'
        response = self.view.post(self.request)

        self.assertEqual(response.status_code, 200)

    @patch('django.template.loader.get_template',
           side_effect=TemplateDoesNotExist)
    def test_view_exception_handling(self, *args, **kwargs):
        """
        Test that the view properly handles an exception
        when a template does not exist.
        """
        request = HttpRequest()
        view = LandingView()

        with self.assertRaises(Exception):
            view.get(request)


im = Image.new(mode='RGB', size=(200, 200))
im_io = BytesIO()
im.save(im_io, 'JPEG')
im_io.seek(0)
image = InMemoryUploadedFile(
    im_io, None, 'random-name.jpg', 'image/jpeg', len(im_io.getvalue()), None
)
file_dict = {'image': image}


class PostListTestCase(TestCase):
    """
    Tests PostList view class.
    """
    def setUp(self):
        self.url = reverse('main:posts_list', kwargs={'type': 'all'})
        self.view = PostList()
        self.factory = RequestFactory()
        self.client = Client()
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
        self.post_1 = Post.objects.create(
            author=self.user_profile, title='Test Post', slug='test-post-1',
            image=image, text='This is a test post 1.', country='PT',
            city='Lisbon', area='Chiado', status=1, relevance=1,
            type='give', category='items'
        )
        # pylint: disable=no-member
        self.post_2 = Post.objects.create(
            author=self.user_profile, title='Test Post 2', slug='test-post-2',
            image=image, text='This is a test post 2.', country='PT',
            city='Lisbon', area='Chiado', status=1, relevance=1,
            type='receive', category='services'
        )
        # pylint: disable=no-member
        self.post_3 = Post.objects.create(
            author=self.user_profile, title='Test Post 3', slug='test-post-3',
            image=image, text='This is a test post 3.', country='PT',
            city='Lisbon', area='Chiado', status=1, relevance=1,
            type='give', category='services'
        )
        # pylint: disable=no-member
        self.post_4 = Post.objects.create(
            author=self.user_profile, title='Test Post 4', slug='test-post-4',
            image=image, text='This is a test post 4.', country='PT',
            city='Lisbon', area='Chiado', status=0, relevance=1,
            type='give', category='services'
        )

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

    def test_post_list_view_context_data(self):
        """
        Test that the post list view includes the correct context data.
        """
        self.client.force_login(user=self.user)
        response = self.client.get(
            reverse('main:posts_list', kwargs={'type': 'all'}))

        self.assertContains(response, API_KEY)

    def test_view_filters_queryset_by_type(self):
        """
        Test that the view filters the queryset of posts correctly
        based on the 'type' parameter in the URL.
        """
        self.client.force_login(user=self.user)
        response = self.client.get(
            reverse('main:posts_list', kwargs={'type': 'give'}))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['post_list']), 2)
        # because they are sorted in reverse order
        self.assertEqual(response.context['post_list'][0].title, 'Test Post 3')

        response = self.client.get(
            reverse('main:posts_list', kwargs={'type': 'receive'}))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['post_list']), 1)
        self.assertEqual(response.context['post_list'][0].title, 'Test Post 2')

    def test_view_filters_queryset_based_on_q_parameter(self):
        """
        Test that the view filters the queryset of posts correctly
        based on the 'q' parameter in the URL.
        """
        request = self.factory.get("/posts?q=test")
        request.user = self.user
        view = PostList.as_view()
        response = view(request)

        self.assertEqual(response.context_data["object_list"].count(), 3)
        # because they are sorted in reverse order
        self.assertEqual(
            response.context_data["object_list"][0].title, "Test Post 3")
        self.assertEqual(
            response.context_data["object_list"][1].title, "Test Post 2")

    def test_ajax_request(self):
        """
        Test that the view correctly handles an AJAX request by
        returning the correct content type.
        """
        self.client.force_login(user=self.user)
        response = self.client.get(
            reverse('main:posts_list', kwargs={'type': 'all'}),
            HTTP_X_REQUESTED_WITH='XMLHttpRequest',
            HTTP_ACCEPT='application/json'
        )

        self.assertEqual(response["Content-Type"], "application/json")

    def test_non_ajax_request(self):
        """
        To test the response for a non-AJAX request.
        """
        self.client.force_login(user=self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'posts.html')

    def test_post_list_only_returns_active_posts(self):
        """
        Test that the post list view only returns posts that
        are marked as active.
        """
        self.client.force_login(user=self.user)
        response = self.client.get(
            reverse('main:posts_list', kwargs={'type': 'all'}))
        queryset = response.context_data['view'].get_queryset()

        self.assertTrue(all(post.status == 1 for post in queryset))

    def test_post_list_filters_by_type(self):
        """
        Test that the post list view correctly filters the queryset
        of posts by the 'type' parameter in the URL.
        """
        self.client.force_login(user=self.user)
        request = self.factory.get(
            reverse("main:posts_list", kwargs={'type': 'all'}))
        request.user = self.user
        response = PostList.as_view()(request, type="give")

        self.assertEqual(response.context_data["object_list"].count(), 2)
        self.assertEqual(response.context_data["object_list"][0].type, "give")


class PostFullTestCase(TestCase):
    """
    Tests PostFull view class.
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
        # pylint: disable=no-member
        self.post = Post.objects.create(
            author=self.user_profile, title='Test Post', slug='test-post',
            image=image, text='This is a test post.', country='PT',
            city='Lisbon', area='Chiado', status=1, relevance=1,
            type='give', category='items')
        self.url = reverse('main:full', kwargs={'slug': self.post.slug})

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
        view = PostFull()
        queryset = view.get_queryset()
        self.assertTrue(all(post.status == 1 for post in queryset))

    def test_post_method_saves_comment(self):
        """
        Test that the post method correctly
        saves a new comment to the database.
        """
        self.client.force_login(user=self.user)
        response = self.client.post(
            reverse('main:full', kwargs={'slug': self.post.slug}),
            {'body': 'Test comment'})

        self.assertEqual(response.status_code, 200)
        # pylint: disable=no-member
        self.assertEqual(Comment.objects.count(), 1)
        # pylint: disable=no-member
        comment = Comment.objects.first()

        self.assertEqual(comment.post, self.post)
        self.assertEqual(comment.user, self.user_profile)
        self.assertEqual(comment.body, 'Test comment')

    def test_get_context_data(self):
        """
        Test that the view includes the correct context data.
        """
        self.client.force_login(user=self.user)
        request = HttpRequest()
        request.user = self.user

        view = PostFull()
        view.object = self.post
        context = view.get_context_data(object=self.post)

        self.assertEqual(context['key'], API_KEY)
        self.assertQuerysetEqual(
            context['comments'],
            # pylint: disable=no-member
            Comment.objects.filter(approved=True, post=self.post.id)
        )


class PostCreateViewTestCase(TestCase):
    """
    Tests PostCreateView class.
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

        self.form_data = {
            'title': 'Test Post',
            'slug': 'test-post',
            'image': image,
            'text': 'This is a test post.',
            'country': 'PT',
            'city': 'Lisbon',
            'area': 'Chiado',
            'status': 1,
            'relevance': 1,
            'type': 'give',
            'category': 'items'
        }
        self.url = reverse('main:new')

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

    def test_form_valid_sets_author(self):
        """
        Test that the form_valid method of the PostCreateView correctly
        sets the author of a newly created post.
        """
        self.client.force_login(user=self.user)
        with patch('cloudinary.uploader.upload'):
            form = CreatePostForm(data=self.form_data, files=file_dict)
            view = PostCreateView()
            view.request = HttpRequest()
            view.request._messages = MagicMock()
            view.request.user = self.user
            response = view.form_valid(form)
            self.assertEqual(response.status_code, 302)
            # pylint: disable=no-member
            self.assertEqual(Post.objects.count(), 1)
            # pylint: disable=no-member
            post = Post.objects.first()
            self.assertEqual(post.author, self.user_profile)

    def test_get_success_url(self):
        """
        Test that the get_success_url method of the PostCreateView
        returns the correct URL.
        """
        self.client.force_login(user=self.user)
        view = PostCreateView()
        view.object = Mock(type='give')
        expected_url = reverse('main:posts_list', kwargs={'type': 'give'})

        self.assertEqual(view.get_success_url(), expected_url)


class PostUpdateViewTestCase(TestCase):
    """
    Tests PostUpdateView class.
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
        # pylint: disable=no-member
        self.post = Post.objects.create(
            author=self.user_profile, title='Test Post', slug='test-post',
            image=image, text='This is a test post.', country='PT',
            city='Lisbon', area='Chiado', status=1, relevance=1,
            type='give', category='items')
        self.url = reverse('main:update', kwargs={'slug': self.post.slug})

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
        form = CreatePostForm(instance=self.post, data={
                              'title': 'Updated title',
                              'text': 'Updated body',
                              'country': 'PT',
                              'city': 'Lisbon',
                              'type': 'give',
                              'category': 'items'
                              })
        with patch('cloudinary.uploader.upload'):
            self.assertTrue(form.is_valid())
        view = PostUpdateView()
        view.object = self.post
        response = view.form_valid(form)

        self.assertEqual(response.status_code,
                         # pylint: disable=bad-super-call
                         super(PostUpdateView,
                               view).form_valid(form).status_code)
        # pylint: disable=no-member
        updated_post = Post.objects.get(id=self.post.id)
        self.assertEqual(updated_post.title, 'Updated title')
        self.assertEqual(updated_post.text, 'Updated body')

    def test_get_success_url(self):
        """
        Test that the get_success_url method returns the correct URL.
        """
        self.client.force_login(user=self.user)
        view = PostUpdateView()
        view.object = self.post
        expected_url = reverse('main:full', kwargs={'slug': self.post.slug})
        self.assertEqual(view.get_success_url(), expected_url)


class PostDeleteViewTestCase(TestCase):
    """
    Tests PostDeleteView class.
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
        # pylint: disable=no-member
        self.post = Post.objects.create(
            author=self.user_profile, title='Test Post', slug='test-post',
            image=image, text='This is a test post.', country='PT',
            city='Lisbon', area='Chiado', status=1, relevance=1,
            type='give', category='items')
        self.url = reverse('main:delete', kwargs={'slug': self.post.slug})

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
        Test that the get_success_url method returns the correct URL.
        """
        self.client.force_login(user=self.user)
        view = PostDeleteView()
        view.object = self.post
        expected_url = reverse('main:posts_list', kwargs={
                               'type': self.post.type})

        self.assertEqual(view.get_success_url(), expected_url)


class BookMarkTestCase(TestCase):
    """
    Tests BookMark class.
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
        # pylint: disable=no-member
        self.post = Post.objects.create(
            author=self.user_profile, title='Test Post', slug='test-post',
            image=image, text='This is a test post.', country='PT',
            city='Lisbon', area='Chiado', status=1, relevance=1,
            type='give', category='items')
        self.url = reverse('main:bookmark', kwargs={'slug': self.post.slug})

    def test_post_adds_user_to_favourite_field(self):
        """
        Test that a POST request to the bookmark view correctly adds
        the current user to the favourite field of the post.
        """
        self.client.force_login(user=self.user)
        request = self.client.post(self.url)
        self.assertEqual(request.status_code, 200)
        # pylint: disable=no-member
        post = Post.objects.get(slug='test-post')
        self.assertIn(self.user_profile, post.favourite.all())

    def test_post_removes_user_from_favourite_field(self):
        """
        Test that a POST request to the bookmark view correctly removes
        the current user from the favourite field of the post.
        """
        self.client.force_login(user=self.user)
        self.post.favourite.add(self.user.userprofile)
        remove = self.client.post(
            reverse('main:bookmark', kwargs={'slug': self.post.slug}))
        self.assertEqual(remove.status_code, 200)
        # pylint: disable=no-member
        updated_post = Post.objects.get(id=self.post.id)

        self.assertNotIn(self.user_profile, updated_post.favourite.all())
        self.assertTrue(isinstance(remove, HttpResponse))
        self.assertEqual(remove.status_code, 200)


class MessagesTestCase(TestCase):
    """
    Tests messages method.
    """
    def setUp(self):
        self.user = CustomUser.objects.create(
            email='test@example.com',
            first_name='Test',
            last_name='User',
            password='testpass',
            is_active=True)
        self.user2 = CustomUser.objects.create(
            email='test2@example.com',
            first_name='Test2',
            last_name='User2',
            password='testpass2',
            is_active=True)
        self.client.force_login(user=self.user)
        self.url = reverse('main:unread')

    def test_messages_view_success(self):
        """
        Test that the MessagesView returns the correct data when
        called with a valid request.
        """
        # pylint: disable=no-member
        conv = Conversation.objects.create(
            name=f'conv{self.user.id}_{self.user2.id}')
        # pylint: disable=no-member
        Message.objects.create(
            conversation=conv, from_user=self.user2,
            to_user=self.user, read=True)
        # pylint: disable=no-member
        Message.objects.create(
            conversation=conv, from_user=self.user2,
            to_user=self.user, read=False)

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['unread'], 1)
