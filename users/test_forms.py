"""
Tests for forms.py of users app.
"""
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, HTML, Submit
from django.test import TestCase
from cloudinary.forms import CloudinaryFileField
from .forms import ProfileForm


class TestProfileForm(TestCase):
    """
    Test Profile Form.
    """
    def setUp(self):
        self.form = ProfileForm()

    def test_form_fields(self):
        """
        Test that the form has the correct fields.
        """
        expected_fields = ['country', 'city', 'userpic', 'languages', 'bio']
        self.assertEqual(list(self.form.fields), expected_fields)

    def test_form_country_field_style(self):
        """
        Test that the form displays the correct
        style for the country field.
        """
        expected_style = 'max-width: 400px;'
        self.assertEqual(self.form.fields['country'].widget.attrs['style'],
                         expected_style)

    def test_form_city_field_placeholder(self):
        """
        Test that the form displays the correct
        placeholder text for the city field.
        """
        expected_placeholder = 'City or area'
        self.assertEqual(self.form.fields['city'].widget.attrs['placeholder'],
                         expected_placeholder)

    def test_form_languages_field_placeholder(self):
        """
        Test that the form displays the correct
        placeholder text for the languages field.
        """
        expected_placeholder = "languages you're able to communicate"
        self.assertEqual(self.form.fields['languages'].widget.attrs['placeholder'],
                         expected_placeholder)

    def test_form_bio_field_style(self):
        """
        Test that the form displays the correct style and placeholder
        for the bio field.
        """
        expected_style = 'height: 150px;'
        expected_placeholder = "Tell a little about yourself, mention what you need or how you can help"
        self.assertEqual(self.form.fields['bio'].widget.attrs['style'],
                         expected_style)
        self.assertEqual(self.form.fields['bio'].widget.attrs['placeholder'],
                         expected_placeholder)

    def test_userpic_field(self):
        """
        Test that the userpic field is an instance of CloudinaryFileField
        """
        self.assertIsInstance(self.form.fields['userpic'], CloudinaryFileField)

    def test_form_has_expected_helper(self):
        """
        Test that the form has the expected FormHelper object.
        """
        expected = [
            'country',
            'city',
            'userpic',
            'languages',
            'bio',
        ]
        self.assertIsInstance(self.form.helper, FormHelper)
        self.assertEqual(self.form.helper.inputs[0].name, 'save')
        self.assertEqual(self.form.helper.inputs[0].value, 'Save')
        self.assertEqual(list(self.form.fields.keys()), expected)
