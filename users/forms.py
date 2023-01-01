from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, HTML, Submit
from cloudinary.forms import CloudinaryFileField
from main.models import UserProfile


class ProfileForm(forms.ModelForm):

    class Meta:
        model = UserProfile
        fields = ['country', 'city', 'userpic', 'languages', 'bio']

        widgets = {
            'country': forms.Select(attrs={
                'style': 'max-width: 400px;',
                }),
            'city': forms.TextInput(attrs={
                'placeholder': 'City or area'
                }),
            'languages': forms.TextInput(attrs={
                'placeholder': "languages you're able to communicate"
                }),
            'bio': forms.Textarea(attrs={
                'style': 'height: 150px;',
                'placeholder': "Tell a little about yourself, mention what you need or how you can help"
                }),
        }
    userpic = CloudinaryFileField(
        options={
            'crop': 'limit', 'width': 600, 'height': 600,
            'eager': [{'crop': 'fill', 'width': 350, 'height': 350}]
        })

    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.add_input(Submit('save', 'Save', css_class='btn btn-primary px-5'))
        self.helper.layout = Layout(
            'country',
            'city',
            HTML("""{% if form.userpic.value %}<img height=400 src="{{ DEFAULT_FILE_STORAGE }}{{ form.userpic.value.url }}">{% endif %}"""),
            'userpic',
            'languages',
            'bio',
        )
