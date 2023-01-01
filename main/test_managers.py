"""
Tests for managers.py of main app.
"""
from django.test import TestCase
from django.contrib.auth import get_user_model


class CustomUserManagerTests(TestCase):
    """
    Test CustomUserManager manager.
    """
    def test_create_user(self):
        """
        Test that a user is created with the correct email and password.
        """
        email = 'test@example.com'
        password = 'password'
        user = get_user_model().objects.create_user(email=email,
                                                    password=password)
        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_create_user_with_no_email(self):
        """
        Test that a ValueError is raised
        when creating a user with no email.
        """
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(email=None,
                                                 password='password')

    def test_create_superuser(self):
        """
        Test that a superuser is created with the
        correct email and password.
        """
        email = 'test@example.com'
        password = 'password'
        user = get_user_model().objects.create_superuser(email=email,
                                                         password=password)
        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_active)

    def test_create_superuser_with_invalid_is_staff(self):
        """
        Test that a ValueError is raised when creating
        a superuser with is_staff=False.
        """
        with self.assertRaises(ValueError):
            get_user_model().objects.create_superuser(email='test@example.com',
                                                      password='password',
                                                      is_staff=False)

    def test_create_superuser_with_invalid_is_superuser(self):
        """
        Test that a ValueError is raised when creating
        a superuser with is_superuser=False.
        """
        with self.assertRaises(ValueError):
            get_user_model().objects.create_superuser(email='test@example.com',
                                                      password='password',
                                                      is_superuser=False)
