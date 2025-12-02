from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

User = get_user_model()

class UserRegisterForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        placeholders = {
            'username': 'Enter your username',
            'email': 'Enter your email address',
            'password1': 'Create a strong password',
            'password2': 'Confirm your password',
            'first_name': 'Enter your First name',
            'last_name': 'Enter your Last name',
        }
        
        for field_name, field in self.fields.items():
            field.widget.attrs.update({
                'placeholder': placeholders.get(field_name, f'Enter {field_name}')
            })
    role = forms.ChoiceField(choices=User.ROLE_CHOICES)

    class Meta:
        model = User
        fields = ['username', 'email', 'role', 'first_name', 'last_name', 'password1', 'password2']

class UserLoginForm(forms.Form):
    email = forms.EmailField(widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your email'
        }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your password'
        }))

class JobSeekerProfileForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        placeholders = {
            'first_name': 'Enter your First name',
            'last_name': 'Enter your Last name',
            'address': 'Enter your full address',
            'mobile': 'Enter your mobile number',
            'headline': 'Enter a short headline',
        }
        
        for field_name, field in self.fields.items():
            field.widget.attrs.update({
                'placeholder': placeholders.get(field_name, f'Enter {field_name}')
            })

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'address', 'mobile', 'headline']
