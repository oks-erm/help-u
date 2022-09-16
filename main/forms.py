from django.forms import ModelForm, CharField, TextInput
from allauth.account.forms import SignupForm
from .models import CustomUser


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
