from django.test import TestCase
from django.http import HttpRequest
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from main.models import CustomUser

from .views import MessagesView


class MessagesViewTests(TestCase):
    def setUp(self):
        # pylint: disable=no-member
        self.user = CustomUser.objects.create(
            email='test@example.com',
            first_name='Test',
            last_name='User',
            password='testpass',
            is_active=True)
        self.view = MessagesView()
        self.request = HttpRequest()

    def test_get_context_data(self):
        self.view.request = self.request
        self.view.request.user = self.user
        context = self.view.get_context_data()
        self.assertEqual(context["id"], self.user.id)
        self.assertEqual(context["name"], self.user.first_name)
