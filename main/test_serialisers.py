from django.test import TestCase
from .models import CustomUser, UserProfile
from .serialisers import CustomUserSerializer


class CustomUserSerializerTest(TestCase):
    """
    Test case for the MessageSerialiser class.
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

    def test_custom_user_serializer(self):
        """
        Tests that the CustomUserSerializer correctly serializes a valid
        instance of CustomUser model. It checks that the serialized
        output contains the correct data and has the correct fields.
        """
        serializer = CustomUserSerializer(self.user)
        data = serializer.data
        self.assertEqual(data['id'], self.user.id)
        self.assertEqual(data['first_name'], self.user.first_name)
        self.assertEqual(data['last_name'], self.user.last_name)
        self.assertEqual(data['profile'], self.user_profile.id)
