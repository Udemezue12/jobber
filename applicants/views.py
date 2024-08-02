from django.shortcuts import get_object_or_404, render, redirect
import requests
import time
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from applicants.models import Application, CustomUser, JobPost, CompanyProfile
from django.contrib.auth.forms import AuthenticationForm
from .forms import UserLoginForm, UserRegistrationForm, ApplicationForm, CompanyProfileForm, JobPostForm, ProfileForm
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_GET, require_POST
from django.utils.decorators import method_decorator
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.urls import reverse_lazy
from django.utils import timezone
from datetime import timedelta

# /////////////////////////////////////////////////ERROR PAGES/////////// ///////////////////////////////////////////////////////////////////////


def bad_request(request, exception):
    return render(request, 'error_pages/400.html', status=400)


def forbidden(request, exception):
    return render(request, 'error_pages/403.html', status=403)


def page_not_found(request, exception):
    return render(request, 'error_pages/404.html', status=404)


def internal_server_error(request):
    return render(request, 'error_pages/500.html', status=500)
# /////////////////////////////////////////////////////////////////////////////////////////////////////


def index(request):
    return render(request, 'index.html')


# def register(request):
#     start_time = time.time()
#     if request.method == 'POST':
#         form = UserRegistrationForm(request.POST)
#         if form.is_valid():
#             user = form.save()
#             login(request, user)
#             end_time = time.time()
#             print(f"Form processing time: {end_time - start_time} seconds")
#             return redirect('index')
#         else:
#             end_time = time.time()
#             print(f"Form validation time: {end_time - start_time} seconds")
#             print(form.errors)
#     else:
#         form = UserRegistrationForm()
#     return render(request, 'register.html', {'form': form})

def fetch_countries_choices(request):
    form = UserRegistrationForm()
    countries = form.fetch_countries_choices()
    return JsonResponse(countries, safe=False)


def fetch_states(request, country_code):
    url = f"https://country-api-1.onrender.com/states/states/{country_code}/"
    response = requests.get(url)
    if response.status_code == 200:
        states = response.json().get(country_code, [])
        return JsonResponse(states, safe=False)
    else:
        return JsonResponse([], safe=False)


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            if user.role == 'employer':
                return redirect('create_company_profile')
            elif user.role == 'job_applicant':
                return redirect('create_profile')
    else:
        form = UserRegistrationForm()
    return render(request, 'register.html', {'form': form})


def custom_login(request):
    if request.method == 'POST':
        form = UserLoginForm(request, request.POST)
        if form.is_valid():
            user = form.get_user()
            if user is not None:
                login(request, user)
                if user.role == 'employer':
                    return redirect('employer_dashboard')
                elif user.role == 'job_applicant':
                    return redirect('job_post_list')
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = UserLoginForm()
    return render(request, 'login.html', {'form': form})

# def custom_login(request):
#     if request.method == 'POST':
#         form = UserLoginForm(request.POST)
#         if form.is_valid():
#             user = form.get_user()
#             if user is not None:
#                 login(request, user)
#                 if user.role == 'employer':
#                     return redirect('dashboard')
#                 elif user.role == 'job_applicant':
#                     return redirect('job_list')
#             else:
#                 messages.error(request, "Invalid username or password.")
#         else:
#             print("Form is not valid")
#             print(form.errors)
#             messages.error(request, "Invalid username or password.")
#     else:
#         form = UserLoginForm()
#     return render(request, 'login.html', {'form': form})

# def custom_login(request):
#     if request.method == 'POST':
#         form = UserLoginForm(request.POST)
#         if form.is_valid():
#             username = form.cleaned_data['username']
#             password = form.cleaned_data['password']
#             user = authenticate(request, username=username, password=password)
#             if user is not None:
#                 login(request, user)
#                 if user.role == 'employer':
#                     return redirect('dashboard')
#                 elif user.role == 'job_applicant':
#                     return redirect('job_list')
#             else:
#                 form.add_error(None, 'Invalid username or password')
#     else:
#         form = UserLoginForm()
#     return render(request, 'login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('index')


@login_required
def create_profile(request):
    if request.user.role != 'job_applicant':
        return render(request, 'error.html', {'message': 'You do not have permission to view this page.'})

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            profile.save()
            return redirect('dashboard')
    else:
        form = ProfileForm()
    return render(request, 'create_profile.html', {'form': form})


@login_required
@login_required
def create_company_profile(request):
    if request.user.role != 'employer':
        return render(request, 'error.html', {'message': 'You do not have permission to view this page.'})

    # Check if the user already has a CompanyProfile
    try:
        company_profile = CompanyProfile.objects.get(user=request.user)
        return redirect('update_company_profile')  # Redirect to update form if profile exists
    except CompanyProfile.DoesNotExist:
        if request.method == 'POST':
            form = CompanyProfileForm(request.POST, request.FILES)
            if form.is_valid():
                profile = form.save(commit=False)
                profile.user = request.user
                profile.save()
                return redirect('employer_dashboard')
        else:
            form = CompanyProfileForm()
        return render(request, 'create_company_profile.html', {'form': form})

@login_required
def update_company_profile(request):
    if request.user.role != 'employer':
        return render(request, 'error.html', {'message': 'You do not have permission to view this page.'})

    # Fetch the user's existing CompanyProfile
    company_profile = get_object_or_404(CompanyProfile, user=request.user)

    if request.method == 'POST':
        form = CompanyProfileForm(request.POST, request.FILES, instance=company_profile)
        if form.is_valid():
            form.save()
            return redirect('employer_dashboard')
    else:
        form = CompanyProfileForm(instance=company_profile)
    return render(request, 'update_company_profile.html', {'form': form})


# @login_required


@login_required
def employer_dashboard(request):
    if request.user.role == 'employer':
        return render(request, 'dashboard.html', {'user': request.user})


@login_required
def applicant_dashboard(request):
    if request.user.role == 'job_applicant':
        return render(request, 'job_list.html', {'user': request.user})


@login_required
def post_job(request):
    if request.user.role != 'employer':
        return redirect('index')

    if request.method == 'POST':
        form = JobPostForm(request.POST)
        if form.is_valid():
            job_post = form.save(commit=False)
            job_post.company = request.user.companyprofile
            job_post.save()
            return redirect('job_list')
    else:
        form = JobPostForm()
    return render(request, 'post_job.html', {'form': form})


@method_decorator(login_required, name='dispatch')
class JobPostCreateView(CreateView):
    model = JobPost
    form_class = JobPostForm
    template_name = 'post_ob.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.company = self.request.user.company_profile
        return super().form_valid(form)

@method_decorator(login_required, name='dispatch')
class JobPostListView(ListView):
    model = JobPost
    template_name = 'job_post_list.html'
    context_object_name = 'jobs'

class JobPostDetailView(DetailView):
    model = JobPost
    template_name = 'job_post_detail.html'
    context_object_name = 'job'

@login_required
def apply_to_job(request, pk):
    job = get_object_or_404(JobPost, pk=pk)
    if request.method == 'POST':
        form = ApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            application = form.save(commit=False)
            application.user = request.user
            application.job_post = job
            application.submitted_at = timezone.now()
            application.status = 'pending'
            application.save()
            return redirect('job_post_detail', pk=pk)
    else:
        form = ApplicationForm()
    return render(request, 'apply_to_job.html', {'form': form, 'job': job})

@method_decorator(login_required, name='dispatch')
class CompanyApplicationsView(ListView):
    model = Application
    template_name = 'company_applications.html'
    context_object_name = 'applications'

    def get_queryset(self):
        return Application.objects.filter(job_post__company=self.request.user.company_profile)

@login_required
def update_resume(request, pk):
    application = get_object_or_404(Application, pk=pk, user=request.user)
    if timezone.now() > application.submitted_at + timedelta(days=2):
        return redirect('dashboard')  # or some error page
    if request.method == 'POST':
        form = ApplicationForm(request.POST, request.FILES, instance=application)
        if form.is_valid():
            form.save()
            return redirect('dashboard')  # or some success page
    else:
        form = ApplicationForm(instance=application)
    return render(request, 'update_resume.html', {'form': form})

@login_required
def update_application_status(request, application_id, status):
    if request.user.role != 'employer':
        return redirect('index')

    application = get_object_or_404(Application, id=application_id, job_post__company=request.user.company_profile)
    application.status = status
    application.save()
    return redirect('review_applications')

@login_required
def edit_job(request, job_id):
    if request.user.role != 'employer':
        return redirect('index')

    job_post = get_object_or_404(JobPost, id=job_id, company=request.user.company_profile)

    if request.method == 'POST':
        form = JobPostForm(request.POST, instance=job_post)
        if form.is_valid():
            form.save()
            return redirect('manage_jobs')
    else:
        form = JobPostForm(instance=job_post)

    return render(request, 'edit_job.html', {'form': form})

@login_required
def manage_jobs(request):
    if request.user.role != 'employer':
        return redirect('index')

    jobs = JobPost.objects.filter(company=request.user.company_profile)
    return render(request, 'manage_jobs.html', {'jobs': jobs})


def admin_dashboard(request):
    users = CustomUser.objects.all()
    return render(request, 'admin_dashboard.html', {'users': users})

# @staff_member_required


def manage_user(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('admin_dashboard')
    else:
        form = UserRegistrationForm(instance=user)
    return render(request, 'manage_user.html', {'form': form})


def job_list(request):
    jobs = JobPost.objects.all()
    return render(request, 'job_list.html', {'jobs': jobs})


def job_detail(request, job_id):
    job = get_object_or_404(JobPost, id=job_id)
    return render(request, 'job_detail.html', {'job': job})
