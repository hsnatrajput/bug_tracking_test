from django import forms
from .models import Project, Bug, Screenshot, User
from django.contrib.auth.forms import UserCreationForm

class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True

class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())  
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = single_file_clean(data, initial)
        return result

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['name', 'image', 'description']
        widgets = {
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control', 'maxlength': 200}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }



class BugForm(forms.ModelForm):
    class Meta:
        model = Bug
        fields = ['title', 'description', 'deadline', 'type', 'status', 'project', 'assigned_to']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'deadline': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'type': forms.Select(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'project': forms.Select(attrs={'class': 'form-control'}),
            'assigned_to': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
       
        self.user = kwargs.pop('user', None)
        super(BugForm, self).__init__(*args, **kwargs)

        
        if self.user and self.user.user_type == 'developer':
            for field in self.fields:
                if field != 'status':
                    self.fields[field].widget.attrs['disabled'] = True

        if 'type' in self.data:
            try:
                bug_type = self.data.get('type')
                if bug_type == 'bug':
                    self.fields['status'].choices = Bug.STATUS_CHOICES_BUG
                else:
                    self.fields['status'].choices = Bug.STATUS_CHOICES_FEATURE
            except (ValueError, TypeError):
                pass 
        elif self.instance.pk:  
            if self.instance.type == 'bug':
                self.fields['status'].choices = Bug.STATUS_CHOICES_BUG
            else:
                self.fields['status'].choices = Bug.STATUS_CHOICES_FEATURE
        else:
            self.fields['status'].choices = Bug.STATUS_CHOICES_BUG  

      
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(BugForm, self).__init__(*args, **kwargs)

        if user and user.user_type in ['manager', 'qa']:
            self.fields['assigned_to'].queryset = User.objects.filter(user_type='developer')

class ScreenshotForm(forms.ModelForm):
    image = MultipleFileField(label='Select files', required=False)

    class Meta:
        model = Screenshot
        fields = ['image']



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
