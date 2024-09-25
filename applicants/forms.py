from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
import requests
from django.contrib.auth import get_user_model as user_model
from .models import Complaint, CustomUser, Notification, Profile, Application, CompanyProfile, JobPost
import bcrypt
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

# CustomUser = user_model()


class CustomChoiceField(forms.ChoiceField):
    def validate(self, value):
        pass


# class UserRegistrationForm(UserCreationForm):
#     email = forms.EmailField(required=True)
#     country = CustomChoiceField(
#         label='Country', choices=[], widget=forms.Select(attrs={'id': 'country'}))
#     state = CustomChoiceField(
#         label='State', choices=[], widget=forms.Select(attrs={'id': 'state'}))
#     phone_number = forms.CharField(label='Phone Number', max_length=20)
#     role = forms.ChoiceField(label='Role', choices=CustomUser.ROLE_CHOICES)

#     class Meta:
#         model = CustomUser
#         fields = ('username', 'email', 'password1', 'password2',
#                   'first_name', 'last_name', 'phone_number', 'country', 'state', 'role')

#     def __init__(self, *args, **kwargs):
#         super(UserRegistrationForm, self).__init__(*args, **kwargs)
#         self.fields['country'].choices = self.fetch_countries_choices()
#         self.fields['state'].choices = []

#     def fetch_countries_choices(self):
#         url = "https://country-api-1.onrender.com/country/countries"
#         response = requests.get(url)
#         if response.status_code == 200:
#             return [(country[0], country[1]) for country in response.json()]
#         else:
#             return []

#     def clean_email(self):
#         email = self.cleaned_data.get('email')
#         if CustomUser.objects.filter(email=email).exists():
#             raise forms.ValidationError(
#                 "This Email already exists.")
#         return email

#     def clean_phone_number(self):
#         phone_number = self.cleaned_data.get('phone_number')
#         if CustomUser.objects.filter(phone_number=phone_number).exists():
#             raise forms.ValidationError(
#                 "This Phone Number already exists.")
#         return phone_number

#     def clean_username(self):
#         username = self.cleaned_data.get('username')
#         if CustomUser.objects.filter(username=username).exists():
#             raise forms.ValidationError(
#                 "This Username already exists.")
#         return username
class ApplicantRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    country = CustomChoiceField(
        label='Country', choices=[], widget=forms.Select(attrs={'id': 'country'}))
    state = CustomChoiceField(
        label='State', choices=[], widget=forms.Select(attrs={'id': 'state'}))
    phone_number = forms.CharField(label='Phone Number', max_length=20)
    role = forms.ChoiceField(label='Role', choices=[(CustomUser.JOB_APPLICANT, 'Job Applicant')])

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password1', 'password2',
                  'first_name', 'last_name', 'phone_number', 'country', 'state', 'role')

    def __init__(self, *args, **kwargs):
        super(ApplicantRegistrationForm, self).__init__(*args, **kwargs)
        self.fields['country'].choices = self.fetch()
        self.fields['state'].choices = []

    def fetch(self):
        url = "https://country-api-1.onrender.com/country/countries"
        response = requests.get(url)
        if response.status_code == 200:
            return [(country[0], country[1]) for country in response.json()]
        else:
            return []

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError(
                "This Email already exists.")
        return email

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        if CustomUser.objects.filter(phone_number=phone_number).exists():
            raise forms.ValidationError(
                "This Phone Number already exists.")
        return phone_number

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if CustomUser.objects.filter(username=username).exists():
            raise forms.ValidationError(
                "This Username already exists.")
        return username


class EmployerRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    country = CustomChoiceField(
        label='Country', choices=[], widget=forms.Select(attrs={'id': 'country'}))
    state = CustomChoiceField(
        label='State', choices=[], widget=forms.Select(attrs={'id': 'state'}))
    phone_number = forms.CharField(label='Phone Number', max_length=20)
    role = forms.ChoiceField(label='Role', choices=[(CustomUser.EMPLOYER, 'Employer')])

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password1', 'password2',
                  'first_name', 'last_name', 'phone_number', 'country', 'state', 'role')

    def __init__(self, *args, **kwargs):
        super(EmployerRegistrationForm, self).__init__(*args, **kwargs)
        self.fields['country'].choices = self.fetch_countries_choices()
        self.fields['state'].choices = []

    def fetch_countries_choices(self):
        url = "https://country-api-1.onrender.com/country/countries"
        response = requests.get(url)
        if response.status_code == 200:
            return [(country[0], country[1]) for country in response.json()]
        else:
            return []

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError(
                "This Email already exists.")
        return email

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        if CustomUser.objects.filter(phone_number=phone_number).exists():
            raise forms.ValidationError(
                "This Phone Number already exists.")
        return phone_number

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if CustomUser.objects.filter(username=username).exists():
            raise forms.ValidationError(
                "This Username already exists.")
        return username


class ManagerRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    country = CustomChoiceField(
        label='Country', choices=[], widget=forms.Select(attrs={'id': 'country'}))
    state = CustomChoiceField(
        label='State', choices=[], widget=forms.Select(attrs={'id': 'state'}))
    phone_number = forms.CharField(label='Phone Number', max_length=20)
    role = forms.ChoiceField(label='Role', choices=[(CustomUser.MANAGER, 'Manager')])

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password1', 'password2',
                  'first_name', 'last_name', 'phone_number', 'country', 'state', 'role')

    def __init__(self, *args, **kwargs):
        super(ManagerRegistrationForm, self).__init__(*args, **kwargs)
        self.fields['country'].choices = self.fetch_choices()
        self.fields['state'].choices = []

    def fetch_choices(self):
        url = "https://country-api-1.onrender.com/country/countries"
        response = requests.get(url)
        if response.status_code == 200:
            return [(country[0], country[1]) for country in response.json()]
        else:
            return []

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError(
                "This Email already exists.")
        return email

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        if CustomUser.objects.filter(phone_number=phone_number).exists():
            raise forms.ValidationError(
                "This Phone Number already exists.")
        return phone_number

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if CustomUser.objects.filter(username=username).exists():
            raise forms.ValidationError(
                "This Username already exists.")
        return username


class UserLoginForm(AuthenticationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'password')


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['resume', 'personal_details', 'picture']


class CompanyProfileForm(forms.ModelForm):
    class Meta:
        model = CompanyProfile
        fields = ['company_name', 'company_address',
                  'hiring_needs', 'company_logo']


class JobPostForm(forms.ModelForm):
    country = CustomChoiceField(
        label='Country', choices=[], widget=forms.Select(attrs={'id': 'country'}))
    state = CustomChoiceField(
        label='State', choices=[], widget=forms.Select(attrs={'id': 'state'}))
    expiry_date = forms.DateField(
        widget=forms.SelectDateWidget,
        required=False,
        help_text="Select the expiry date for the job post"
    )

    class Meta:
        model = JobPost
        fields = ['job_title', 'job_description', 'country', 'state', 'job_type',
                  'job_salary', 'job_requirements', 'expiry_date']

    def __init__(self, *args, **kwargs):
        super(JobPostForm, self).__init__(*args, **kwargs)
        self.fields['country'].choices = self.fetch_countries()
        self.fields['state'].choices = []

    def fetch_countries(self):
        url = "https://country-api-1.onrender.com/country/countries"
        response = requests.get(url)
        if response.status_code == 200:
            return [(country[0], country[1]) for country in response.json()]
        else:
            return []


class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ['cover_letter', 'resume']


class NotificationForm(forms.ModelForm):
    class Meta:
        model = Notification
        fields = ['recipient', 'message', 'is_read']


class ComplaintForm(forms.ModelForm):
    class Meta:
        model = Complaint
        fields = ['subject', 'message']


class ManagerResponseForm(forms.ModelForm):
    class Meta:
        model = Complaint
        fields = ['manager_response']
