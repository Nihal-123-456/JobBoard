from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit

User = get_user_model()

class UserRegisterForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            'username', 'email', 'role', 'first_name', 'last_name', 'password1', 'password2',
            Submit('submit', 'Register Now', css_class='btn btn-primary w-100 py-2 mt-3 fw-bold rounded-pill')
        )
        
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
                'placeholder': placeholders.get(field_name, f'Enter {field_name}'),
                'class': 'form-control'
            })

        self.fields['username'].help_text = '' 
        self.fields['password1'].help_text = ''
        self.fields['password2'].help_text = ''
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
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            'email', 'password',
            Submit('submit', 'Sign In', css_class='btn btn-primary w-100 py-2 mt-3 fw-bold rounded-pill')
        )

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
