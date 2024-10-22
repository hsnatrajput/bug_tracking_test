from django import forms
from .models import  User
from django.contrib.auth.forms import UserCreationForm


class UserForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('email', 'phone_number', 'user_type')
        help_texts = {
            'username': '',
            'password' : '',
        }
    def __init__(self, *args, **kwargs):
        user_type = kwargs.pop('user_type', None)  
        super(UserForm, self).__init__(*args, **kwargs)       
        self.fields['username'].widget.attrs.update({
            'class': 'form-control', 'placeholder': 'Username'
        })
        self.fields['phone_number'].widget.attrs.update({
            'class': 'form-control', 'placeholder': 'Mobile Number'
        })
        self.fields['email'].widget.attrs.update({
            'class': 'form-control', 'placeholder': 'E-mail'
        })
        self.fields['password1'].widget.attrs.update({
            'class': 'form-control', 'placeholder': 'Password'
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'form-control', 'placeholder': 'Confirm Password'
        })
        for fieldname in self.fields:
            self.fields[fieldname].label = ""     
        if user_type:
            self.fields['user_type'].widget = forms.HiddenInput()
            self.fields['user_type'].initial = user_type        
        self.fields['email'].widget.attrs.update({'placeholder': 'Email Address'})
        self.fields['phone_number'].widget.attrs.update({'placeholder': 'Phone Number'})


class UserTypeForm(forms.Form):
    USER_TYPE_CHOICES = [
        ('manager', 'Manager'),
        ('developer', 'Developer'),
        ('qa', 'QA'),
    ]
    user_type = forms.ChoiceField(choices=USER_TYPE_CHOICES, widget=forms.RadioSelect)