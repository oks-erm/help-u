from django.forms import (ModelForm,
                          CharField,
                          TextInput,
                          Textarea,
                          Select)
from allauth.account.forms import SignupForm
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
                'style': 'height: 150px;',
                }),
            'country': Select(attrs={
                'class': 'form-select',
                'size': '5',
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
    image = CloudinaryFileField(
        options={ 
            'tags': "directly_uploaded",
            'crop': 'limit', 'width': 800, 'height': 800,
            'eager': [{'crop': 'fill', 'width': 150, 'height': 150}]
        })