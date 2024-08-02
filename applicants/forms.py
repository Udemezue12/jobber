from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
import requests
from django.contrib.auth import get_user_model as user_model
from .models import CustomUser, Profile, Application, CompanyProfile, JobPost
import bcrypt
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

# CustomUser = user_model()


class CustomChoiceField(forms.ChoiceField):
    def validate(self, value):
        pass


# class UserRegistrationForm(UserCreationForm):
#     first_name = forms.CharField(label='First Name', max_length=100)
#     last_name = forms.CharField(label='Last Name', max_length=100)
#     phone_number = forms.CharField(label='Phone Number', max_length=20)
#     # password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
#     # password2 = forms.CharField(
#     #     label='Confirm Password', widget=forms.PasswordInput)
#     username = forms.CharField(label='Username', max_length=15, required=True)
#     email = forms.EmailField(
#         label='Email', help_text='A valid email address, please.', required=True)
#     role = forms.ChoiceField(label='Role', choices=CustomUser.ROLE_CHOICES)

#     def clean_email(self):
#         email = self.cleaned_data.get('email')
#         if User.objects.filter(email=email).exists():
#             raise ValidationError('The email has already been registered')
#         return email

#     country = CustomChoiceField(
#         label='Country', choices=[], widget=forms.Select(attrs={'id': 'country'}))
#     state = CustomChoiceField(
#         label='State', choices=[], widget=forms.Select(attrs={'id': 'state'}))

#     class Meta:
#         model = CustomUser
#         fields = ['first_name', 'last_name', 'email', 'password1',
#                   'password2', 'phone_number', 'country', 'state', 'username', 'role']

    # def __init__(self, *args, **kwargs):
    #     super(UserRegistrationForm, self).__init__(*args, **kwargs)
    #     self.fields['country'].choices = self.fetch_countries_choices()
    #     self.fields['state'].choices = []

    # def fetch_countries_choices(self):
    #     url = "https://country-api-1.onrender.com/country/countries"
    #     response = requests.get(url)
    #     if response.status_code == 200:
    #         return [(country[0], country[1]) for country in response.json()]
    #     else:
    #         return []

#     def clean_username(self):
#         username = self.cleaned_data.get('username')
#         if CustomUser.objects.filter(username=username).exists():
#             raise ValidationError('The username has already been registered')
#         return username

    # def clean_password(self):

    #     password = self.cleaned_data.get('password1')
    #     if password is None:
    #         raise ValidationError('Password cannot be empty')
    #     if len(password) < 8:
    #         raise ValidationError(
    #             'Password must be at least 8 characters long')
    #         return password

    # def clean(self):
    #     cleaned_data = super().clean()
    #     password = cleaned_data.get("password1")
    #     password2 = cleaned_data.get("password2")

    #     if password != password2:
    #         raise ValidationError("Passwords do not match.")

    #     self.clean_password()

    #     return cleaned_data

    # def save(self, commit=True):
    #     user = super().save(commit=False)
    #     user.set_password(self.cleaned_data["password1"])
    #     if commit:
    #         user.save()
    #     return user

    # def save(self, commit=True):
    #     user = super().save(commit=False)
    #     user.set_password(self.cleaned_data["password"])
    #     if commit:
    #         user.save()
    #     return user
    # def save(self, commit=True):
    #     user = super(UserCreationForm, self).save(commit=False)
    #     password = self.cleaned_data['password1']
    #     hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    #     user.password = hashed_password.decode('utf-8')
    #     if commit:
    #         user.save()
    #     return user


# class UserLoginForm(forms.Form):
#     username = forms.CharField(label='Username', max_length=150)
#     password = forms.CharField(label='Password', widget=forms.PasswordInput)

#     def clean(self):
#         cleaned_data = super().clean()
#         username = cleaned_data.get('username')
#         password = cleaned_data.get('password')

#         if username and password:
#             self.user_cache = authenticate(
#                 username=username, password=password)
#             if self.user_cache is None:
#                 raise forms.ValidationError('Invalid username or password.')
#             elif not self.user_cache.is_active:
#                 raise forms.ValidationError('This account is inactive.')
#         return cleaned_data

#     def get_user(self):
#         return self.user_cache if hasattr(self, 'user_cache') else None

# class CustomChoiceField(forms.ChoiceField):
#     def validate(self, value):
#         return super().validate(value)

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    country = CustomChoiceField(
        label='Country', choices=[], widget=forms.Select(attrs={'id': 'country'}))
    state = CustomChoiceField(
        label='State', choices=[], widget=forms.Select(attrs={'id': 'state'}))
    phone_number = forms.CharField(label='Phone Number', max_length=20)
    role = forms.ChoiceField(label='Role', choices=CustomUser.ROLE_CHOICES)

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password1', 'password2',
                  'first_name', 'last_name', 'phone_number', 'country', 'state', 'role')

    def __init__(self, *args, **kwargs):
        super(UserRegistrationForm, self).__init__(*args, **kwargs)
        self.fields['country'].choices = self.fetch_countries_choices()
        self.fields['state'].choices = []

    def fetch_countries_choices(self):
        url = "https://country-api-1.onrender.com/country/countries"
        response = requests.get(url)
        if response.status_code == 200:
            return [(country[0], country[1]) for country in response.json()]
        else:
            return []

class UserLoginForm(AuthenticationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'password')


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['resume', 'personal_details']


class CompanyProfileForm(forms.ModelForm):
    class Meta:
        model = CompanyProfile
        fields = ['company_name', 'company_address',
                  'hiring_needs', 'company_logo']


class JobPostForm(forms.ModelForm):
    class Meta:
        model = JobPost
        fields = ['job_title', 'job_description', 'job_location', 'job_type',
                  'job_salary', 'job_requirements']


class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ['cover_letter', 'resume']
