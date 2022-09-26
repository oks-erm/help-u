from django.forms import (ModelForm,
                          CharField,
                          TextInput,
                          Textarea,
                          Select)
from allauth.account.forms import SignupForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, HTML, Submit
from cloudinary.forms import CloudinaryFileField
from .models import Post


class CustomSignUpForm(SignupForm):
    first_name = CharField(max_length=30, label='First Name', required=True,
                           widget=TextInput(attrs={'placeholder': 'First Name', 'class': 'form-control'}))
    last_name = CharField(max_length=30, label='Last Name', required=True,
                          widget=TextInput(attrs={'placeholder': 'Last Name', 'class': 'form-control'}))

    def save(self, request):
        user = super(CustomSignUpForm, self).save(request)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.save()
        return user

    def __init__(self, *args, **kwargs):
        super(CustomSignUpForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.fields['password2'].label = ""


class CreatePostForm(ModelForm):

    class Meta:
        model = Post
        fields = ['title', 'text', 'image', 'country', 'city',
                  'area', 'type', 'category']
        widgets = {
            'title': TextInput(attrs={
                'placeholder': 'Title'
                }),
            'text': Textarea(attrs={
                'style': 'height: 150px;',
                }),
            'country': Select(attrs={
                'size': '5',
                'style': 'max-width: 400px;',
                }),
            'city': TextInput(attrs={
                'placeholder': 'City'
                }),
            'area': TextInput(attrs={
                'placeholder': 'Help to specify your location without an address (name a shopping mall or a metro station, etc)'
                }),
            'type': Select(attrs={
                'style': 'max-width: 200px;',
                }),
            'category': Select(attrs={
                'style': 'max-width: 200px;',
                }),
        }
    image = CloudinaryFileField(
        options={
            'crop': 'limit', 'width': 800, 'height': 800,
            'eager': [{'crop': 'fill', 'width': 350, 'height': 350}]
        })

    def __init__(self, *args, **kwargs):
        super(CreatePostForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.add_input(Submit('save', 'Save', css_class='btn btn-primary px-5'))
        self.helper.layout = Layout(
            'title',
            'text',
            HTML("""{% if form.image.value %}<img height=400 src="{{ DEFAULT_FILE_STORAGE }}{{ form.image.value.url }}">{% endif %}"""),
            'image',
            'country',
            'city',
            'area',
            'type',
            'category'
        )
