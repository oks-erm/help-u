import datetime
from unittest.mock import patch
from io import BytesIO
from django.test import TestCase
from django.http import HttpRequest
from django.core.files.uploadedfile import InMemoryUploadedFile
from PIL import Image
from cloudinary.forms import CloudinaryFileField
from .forms import CustomSignUpForm, CreatePostForm
from .models import Post, UserProfile, CustomUser


im = Image.new(mode='RGB', size=(200, 200))
im_io = BytesIO()
im.save(im_io, 'JPEG')
im_io.seek(0)
image = InMemoryUploadedFile(
    im_io, None, 'random-name.jpg', 'image/jpeg', len(im_io.getvalue()), None
)

file_dict = {'image': image}


class TestCustomSignUpForm(TestCase):
    """
    Test CustomSignUpForm.
    """
    def test_first_name_is_required(self):
        """
        Test that first_name is required.
        """
        form = CustomSignUpForm({'first_name': '', 'last_name': 'Last'})
        self.assertFalse(form.is_valid())
        self.assertIn('first_name', form.errors.keys())
        self.assertEqual(form.errors['first_name'][0],
                         'This field is required.')

    def test_last_name_is_required(self):
        """
        Test that second_name is required.
        """
        form = CustomSignUpForm({'first_name': 'First', 'last_name': ''})
        self.assertFalse(form.is_valid())
        self.assertIn('last_name', form.errors.keys())
        self.assertEqual(form.errors['last_name'][0],
                         'This field is required.')

    def test_form_fields(self):
        """
        Test that the form has the correct fields.
        """
        form = CustomSignUpForm()
        self.assertTrue('first_name' in form.fields)
        self.assertTrue('last_name' in form.fields)
        self.assertTrue('password2' in form.fields)

    def test_form_widget_attributes(self):
        """
        Test that the form sets the placeholder
        and class attributes correctly.
        """
        form = CustomSignUpForm()
        self.assertEqual(form.fields['first_name'].widget.attrs['placeholder'],
                         'First Name')
        self.assertEqual(form.fields['first_name'].widget.attrs['class'],
                         'form-control')
        self.assertEqual(form.fields['last_name'].widget.attrs['placeholder'],
                         'Last Name')
        self.assertEqual(form.fields['last_name'].widget.attrs['class'],
                         'form-control')

    def test_save_method(self):
        """
        Test that the save() method sets the first_name
        and last_name fields correctly.
        """
        request = HttpRequest()
        request.session = {}
        form = CustomSignUpForm({'email': 'test@mail.com',
                                 'first_name': 'John',
                                 'last_name': 'Doe',
                                 'password1': 'abcfgfgfg123',
                                 'password2': 'abcfgfgfg123'})
        self.assertTrue(form.is_valid())
        user = form.save(request)
        self.assertEqual(user.first_name, 'John')
        self.assertEqual(user.last_name, 'Doe')

    def test_init_method(self):
        """
        Test that the __init__ method sets the helper attribute correctly.
        """
        form = CustomSignUpForm()
        self.assertIsNotNone(form.helper)
        self.assertEqual(form.fields['password2'].label, '')

    def test_password2_field(self):
        """
        Test that password2 field has no label.
        """
        form = CustomSignUpForm()
        self.assertEqual(form.fields['password2'].label, "")


class TestCreatePostForm(TestCase):
    """
    Test CreatePstForm.
    """
    def test_form_fields(self):
        """
        Test that the form has the correct fields.
        """
        form = CreatePostForm()
        expected_fields = ['title', 'text', 'image', 'country', 'city',
                           'area', 'type', 'category']
        self.assertEqual(list(form.fields), expected_fields)

    def test_form_title_field_placeholder(self):
        """
        Test that the form displays the correct
        placeholder text for the title field.
        """
        form = CreatePostForm()
        expected_placeholder = 'Title'
        self.assertEqual(form.fields['title'].widget.attrs['placeholder'],
                         expected_placeholder)

    def test_form_text_field_style(self):
        """
        Test that the form displays the correct
        style for the text field.
        """
        form = CreatePostForm()
        expected_style = 'height: 150px;'
        self.assertEqual(form.fields['text'].widget.attrs['style'],
                         expected_style)

    def test_form_country_field_size(self):
        """
        Test that the form displays the correct size
        for the country field.
        """
        form = CreatePostForm()
        expected_size = '5'
        self.assertEqual(form.fields['country'].widget.attrs['size'],
                         expected_size)

    def test_form_city_field_placeholder(self):
        """
        Test that the form displays the correct
        placeholder text for the city field.
        """
        form = CreatePostForm()
        expected_placeholder = 'City'
        self.assertEqual(form.fields['city'].widget.attrs['placeholder'],
                         expected_placeholder)

    def test_form_area_field_placeholder(self):
        """
        Test that the form displays the correct
        placeholder text for the area field.
        """
        form = CreatePostForm()
        expected_placeholder = ('Help to specify your location '
                                'without an address (name a shopping '
                                'mall or a metro station, etc)')
        self.assertEqual(form.fields['area'].widget.attrs['placeholder'],
                         expected_placeholder)

    def test_form_type_field_style(self):
        """
        Test that the form displays the correct style for the type field
        """
        form = CreatePostForm()
        expected_style = 'max-width: 200px;'
        self.assertEqual(form.fields['type'].widget.attrs['style'],
                         expected_style)

    def test_form_category_field_style(self):
        """
        Test that the form displays the correct style for the category field
        """
        form = CreatePostForm()
        expected_style = 'max-width: 200px;'
        self.assertEqual(form.fields['category'].widget.attrs['style'],
                         expected_style)

    def test_image_field(self):
        """
        Test that the image field is an instance of CloudinaryFileField
        """
        form = CreatePostForm()
        self.assertIsInstance(form.fields['image'], CloudinaryFileField)

    def test_form_validation(self):
        """
        Test form validation
        """
        # Test that the form is invalid with empty fields
        form_data = {
            'title': '',
            'text': '',
            'image': '',
            'country': '',
            'city': '',
            'area': '',
            'type': '',
            'category': '',
        }
        form = CreatePostForm(data=form_data)
        self.assertFalse(form.is_valid())

        # Test that the form is valid with all fields filled out
        form_data = {
            'title': 'Test title',
            'text': 'Test text',
            'image': file_dict,
            'country': 'PT',
            'city': 'Lisbon',
            'area': 'Chiado',
            'type': 'give',
            'category': 'items',
        }

        with patch('cloudinary.uploader.upload'):
            form = CreatePostForm(data=form_data, files=file_dict)
            self.assertTrue(form.is_valid())

    def test_form_save(self):
        """
        Test that the form saves a new Post object to the database
        """
        user = CustomUser(1, 'test@mail.com', datetime.datetime.now(),
                          'True', 'First', 'Last')
        user.save()
        profile = UserProfile(1, 1)
        profile.save()

        form_data = {
            'title': 'Test title',
            'text': 'Test text',
            'image': file_dict,
            'country': 'PT',
            'city': 'Lisbon',
            'area': 'Chiado',
            'type': 'give',
            'category': 'items',
        }
        form = CreatePostForm(data=form_data, files=file_dict)
        form.instance.author = profile
        self.assertTrue(form.is_valid())

        form.save()
        # pylint: disable=no-member
        self.assertEqual(Post.objects.count(), 1)
        # pylint: disable=no-member
        self.assertEqual(Post.objects.first().title, 'Test title')
