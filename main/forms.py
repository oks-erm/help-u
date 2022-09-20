from django.forms import ModelForm, CharField, TextInput, Textarea, FileInput, Select
from allauth.account.forms import SignupForm
from .models import CustomUser, Post


class CustomSignUpForm(SignupForm):
    first_name = CharField(max_length=30, label='First Name', required=True,
                           widget=TextInput(attrs={'placeholder': 'First Name'}))
    last_name = CharField(max_length=30, label='Last Name', required=True,
                          widget=TextInput(attrs={'placeholder': 'Last Name'}))

    def save(self, request):
        user = super(CustomSignUpForm, self).save(request)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.save()
        return user


class CreatePostForm(ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'text', 'image', 'country', 'city',
                  'area', 'type', 'category']
        widgets = {
            'title': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Title'
                }),
            'text': Textarea(attrs={
                'class': 'form-control', 
                'style': 'height: 250px;',
                }),
            'image': FileInput(attrs={
                'class': 'form-control',
                'id': "formFileMultiple",

            }),
            'country': Select(attrs={
                'class': 'form-select',
                'size': '6',
                'style': 'max-width: 400px;',
                }),
            'city': TextInput(attrs={
                'class': 'form-control',

                'placeholder': 'City'
                }),
            'area': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Help to specify your location without an address (name a shopping mall or a metro station, etc)'
                }),
            'type': Select(attrs={
                'class': 'form-select',
                'style': 'max-width: 200px;',
                }),
            'category': Select(attrs={
                'class': 'form-select',
                'style': 'max-width: 200px;',
                }),
        }