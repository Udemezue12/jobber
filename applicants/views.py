from datetime import timedelta
import requests
from django.shortcuts import get_object_or_404, render, redirect
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_GET, require_POST
from django.utils.decorators import method_decorator
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from applicants.models import Application, CustomUser, JobPost, CompanyProfile, Notification, Profile, Complaint
from django.contrib.auth.forms import AuthenticationForm
from .forms import ManagerResponseForm, UserLoginForm, ApplicantRegistrationForm, ManagerRegistrationForm, EmployerRegistrationForm, ApplicationForm, CompanyProfileForm, JobPostForm, ProfileForm, ComplaintForm, UserReplyForm

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
    if request.user.is_authenticated:
        if request.user.role == 'job_applicant':
            return redirect(reverse('job_post_list'))
        elif request.user.role == 'employer':
            return render(request, 'dashboard.html')

    return render(request, 'index.html')

def register(request):
    return render(request, 'register.html')

def create_notification(user, message):
    Notification.objects.create(recipient=user, message=message)


# def fetch_countries_choices(request):
#     form = UserRegistrationForm()
#     countries = form.fetch_countries_choices()
#     return JsonResponse(countries, safe=False)
def fetch_countries_choices(request):
    form = EmployerRegistrationForm()
    countries = form.fetch_countries_choices()
    return JsonResponse(countries, safe=False)


def fetch(request):
    form = ApplicantRegistrationForm()
    countries = form.fetch()
    return JsonResponse(countries, safe=False)


def fetch_choices(request):
    form = ManagerRegistrationForm()
    countries = form.fetch_choices()
    return JsonResponse(countries, safe=False)


def fetch_countries(request):
    form = JobPostForm()
    countries = form.fetch_countries()
    return JsonResponse(countries, safe=False)


def fetch_states(request, country_code):
    url = f"https://country-api-1.onrender.com/states/states/{country_code}/"
    response = requests.get(url)
    if response.status_code == 200:
        states = response.json().get(country_code, [])
        return JsonResponse(states, safe=False)
    else:
        return JsonResponse([], safe=False)


# def register(request):
#     if request.method == 'POST':
#         form = UserRegistrationForm(request.POST)
#         if form.is_valid():
#             user = form.save()
#             login(request, user)
#             if user.role == 'employer':
#                 return redirect('create_company_profile')
#             elif user.role == 'job_applicant':
#                 return redirect('create_profile')
#     else:
#         form = UserRegistrationForm()
#     return render(request, 'register.html', {'form': form})
def applicant_register(request):
    if request.method == 'POST':
        form = ApplicantRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            if user.role == CustomUser.JOB_APPLICANT:
                return redirect('create_profile')
    else:
        form = ApplicantRegistrationForm()
    return render(request, 'applicant_register.html', {'form': form})


def employer_register(request):
    if request.method == 'POST':
        form = EmployerRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            if user.role == CustomUser.EMPLOYER:
                return redirect('create_company_profile')
    else:
        form = EmployerRegistrationForm()
    return render(request, 'employer_register.html', {'form': form})
def manager_register(request):
    if request.method == 'POST':
        form = ManagerRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            if user.role == CustomUser.MANAGER:
                return redirect('login')
    else:
        form = ManagerRegistrationForm()
    return render(request, 'admin_register.html', {'form': form})

def custom_login(request):
    if request.method == 'POST':
        form = UserLoginForm(request, request.POST)
        if form.is_valid():
            user = form.get_user()
            if user is not None:
                login(request, user)
                if user.role == CustomUser.EMPLOYER:
                    return redirect('employer_dashboard')
                elif user.role == CustomUser.JOB_APPLICANT:
                    return redirect('job_post_list')
                elif user.role == CustomUser.MANAGER:
                    return redirect('index')
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = UserLoginForm()
    return render(request, 'login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('index')


@login_required
def create_profile(request):
    if request.user.role != 'job_applicant':
        return render(request, 'error.html', {'message': 'You do not have permission to view this page.'})

    try:
        profile = Profile.objects.get(user=request.user)
        return redirect('update_profile')
    except Profile.DoesNotExist:
        if request.method == 'POST':
            form = ProfileForm(request.POST, request.FILES)
            if form.is_valid():
                profile = form.save(commit=False)
                profile.user = request.user
                profile.save()
                return redirect('login')
        else:
            form = ProfileForm()

    return render(request, 'create_profile.html', {'form': form})


@login_required
def view_profile(request):
    if request.user.role != 'job_applicant':
        return render(request, 'error.html', {'message': 'You do not have permission to view this page.'})

    profile = Profile.objects.get(user=request.user)
    return render(request, 'view_profile.html', {'profile': profile})


@login_required
def create_company_profile(request):
    if request.user.role != 'employer':
        return render(request, 'error.html', {'message': 'You do not have permission to view this page.'})

    try:
        company_profile = CompanyProfile.objects.get(user=request.user)
        return redirect('update_company_profile')
    except CompanyProfile.DoesNotExist:
        if request.method == 'POST':
            form = CompanyProfileForm(request.POST, request.FILES)
            if form.is_valid():
                profile = form.save(commit=False)
                profile.user = request.user
                profile.save()
                return redirect('login')
        else:
            form = CompanyProfileForm()
        return render(request, 'create_company_profile.html', {'form': form})


@login_required
def view_company_profile(request):
    if request.user.role != 'employer':
        return render(request, 'error.html', {'message': 'You do not have permission to view this page.'})

    try:
        company_profile = CompanyProfile.objects.get(user=request.user)
        return render(request, 'view_company_profile.html', {'company_profile': company_profile})
    except CompanyProfile.DoesNotExist:
        return redirect('create_company_profile')


@login_required
def update_company_profile(request):
    if request.user.role != 'employer':
        return render(request, 'error.html', {'message': 'You do not have permission to view this page.'})

    company_profile = get_object_or_404(CompanyProfile, user=request.user)

    if request.method == 'POST':
        form = CompanyProfileForm(
            request.POST, request.FILES, instance=company_profile)
        if form.is_valid():
            form.save()
            return redirect('employer_dashboard')
    else:
        form = CompanyProfileForm(instance=company_profile)
    return render(request, 'update_company_profile.html', {'form': form})


@login_required
def update_profile(request):
    if request.user.role != 'job_applicant':
        return render(request, 'error.html', {'message': 'You do not have permission to view this page.'})

    profile = get_object_or_404(Profile, user=request.user)

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('view_profile')
    else:
        form = ProfileForm(instance=profile)

    return render(request, 'update_profile.html', {'form': form})


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
    template_name = 'post_job.html'
    success_url = reverse_lazy('job_list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.company = self.request.user.company_profile
        return super().form_valid(form)


@method_decorator(login_required, name='dispatch')
class JobPostListView(ListView):
    model = JobPost
    template_name = 'job_post_list.html'
    context_object_name = 'jobs'
    paginate_by = 10

    def get_queryset(self):
        return JobPost.objects.all().order_by('-job_posted_date')




class JobPostDetailView(LoginRequiredMixin, DetailView):
    model = JobPost
    template_name = 'job_post_detail.html'
    context_object_name = 'job'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        job = self.get_object()
        user_applications = Application.objects.filter(user=self.request.user, job_post=job)
        context['user_applied'] = user_applications.exists()
        return context





@login_required
def apply_to_job(request, pk):
    job = get_object_or_404(JobPost, pk=pk)
    
    if Application.objects.filter(user=request.user, job_post=job).exists():
        messages.warning(request, 'You have already applied for this job.')
        return redirect('job_post_detail', pk=pk)
    
    if request.method == 'POST':
        form = ApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            application = form.save(commit=False)
            application.user = request.user
            application.job_post = job
            application.submitted_at = timezone.now()
            application.status = 'pending'
            application.save()

            message = f"{request.user.full_name} with {request.user.email} from {request.user.country} and {request.user.state} has applied for {job.job_title}."
            create_notification(job.company.user, message)

            messages.success(request, 'You have successfully applied for the job.')
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
        return redirect('dashboard')
    if request.method == 'POST':
        form = ApplicationForm(
            request.POST, request.FILES, instance=application)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = ApplicationForm(instance=application)
    return render(request, 'update_resume.html', {'form': form})


@login_required
def update_application_status(request, application_id, status):
    if request.user.role != 'employer':
        return redirect('index')

    application = get_object_or_404(
        Application, id=application_id, job_post__company=request.user.company_profile)
    application.status = status
    application.save()
    message = f"Your application for {application.job_post.job_title} has been {status}."
    create_notification(application.user, message)
    return redirect('review_applications')


@login_required
def edit_job(request, job_id):
    if request.user.role != 'employer':
        return redirect('index')

    job_post = get_object_or_404(
        JobPost, id=job_id, company=request.user.company_profile)

    if request.method == 'POST':
        form = JobPostForm(request.POST, instance=job_post)
        if form.is_valid():
            form.save()
            return redirect('view_posted_jobs')
    else:
        form = JobPostForm(instance=job_post)

    return render(request, 'edit_job.html', {'form': form})


@login_required
def view_posted_jobs(request):
    if request.user.role != 'employer':
        return redirect('index')

    posted_jobs = JobPost.objects.filter(company=request.user.company_profile)
    return render(request, 'view_posted_jobs.html', {'posted_jobs': posted_jobs})


@login_required
def delete_job(request, job_id):
    if request.user.role != 'employer':
        return redirect('index')

    job_post = get_object_or_404(
        JobPost, id=job_id, company=request.user.company_profile)

    if request.method == 'POST':
        job_post.delete()
        return redirect('view_posted_jobs')

    return render(request, 'confirm_delete_job.html', {'job_post': job_post})


def admin_dashboard(request):
    users = CustomUser.objects.all()
    return render(request, 'admin_dashboard.html', {'users': users})


# def manage_user(request, user_id):
#     user = get_object_or_404(CustomUser, id=user_id)
#     if request.method == 'POST':
#         form = UserRegistrationForm(request.POST, instance=user)
#         if form.is_valid():
#             form.save()
#             return redirect('admin_dashboard')
#     else:
#         form = UserRegistrationForm(instance=user)
#     return render(request, 'manage_user.html', {'form': form})


@login_required
def accept_application(request, pk):
    application = get_object_or_404(Application, pk=pk)

    if application.status == 'accepted':
        messages.warning(
            request, "This application has already been accepted.")
    else:
        application.status = 'accepted'
        application.save()

        Notification.notify_user(
            application.user,f'Your application for the job "{application.job_post.job_title}" has been accepted.')
        messages.success(request, "Application has been accepted.")

    return redirect('company_applications')


@login_required
def decline_application(request, pk):
    application = get_object_or_404(Application, pk=pk)

    if application.status == 'declined':
        messages.warning(
            request, "This application has already been declined.")
    else:
        application.status = 'declined'
        application.save()

        Notification.notify_user(application.user,f'Your application for the job "{application.job_post.job_title}" has been declined.')
        messages.success(request, "Application has been declined.")

    return redirect('company_applications')


def job_list(request):
    jobs = JobPost.objects.all()
    return render(request, 'job_list.html', {'jobs': jobs})


def job_detail(request, job_id):
    job = get_object_or_404(JobPost, id=job_id)
    return render(request, 'job_detail.html', {'job': job})


@login_required
def notification_list(request):
    notifications = Notification.objects.filter(
        recipient=request.user).order_by('-timestamp')
    return render(request, 'notification_list.html', {'notifications': notifications})


@login_required
def notification_detail(request, notification_id):
    notification = get_object_or_404(
        Notification, id=notification_id, recipient=request.user)

    if not notification.is_read:
        notification.is_read = True
        notification.save()

    return render(request, 'notification_detail.html', {'notification': notification})


@login_required
def notification_delete(request, notification_id):
    notification = get_object_or_404(
        Notification, id=notification_id, recipient=request.user)
    notification.delete()
    return redirect('notification_list')


@login_required
def view_applications(request):
    applications = Application.objects.filter(
        user=request.user).select_related('job_post')

    return render(request, 'view_applications.html', {'applications': applications})


@login_required
def submit_complaint(request):
    if request.user.role not in ['employer', 'job_applicant']:
        return render(request, 'error.html', {'message': 'You do not have permission to view this page.'})

    if request.method == 'POST':
        form = ComplaintForm(request.POST)
        if form.is_valid():
            complaint = form.save(commit=False)
            complaint.sender = request.user
            complaint.sender_role = request.user.role
            complaint.manager= CustomUser.objects.filter(
                role='manager').first()  
            complaint.save()
            return redirect('complaint_list')
    else:
        form = ComplaintForm()

    return render(request, 'submit_complaint.html', {'form': form})


@login_required
def respond_to_complaint(request, complaint_id):
    if request.user.role != 'manager':
        return render(request, 'error.html', {'message': 'You do not have permission to view this page.'})

    complaint = get_object_or_404(
        Complaint, id=complaint_id, manager=request.user)

    if complaint.user_reply and not complaint.reply_viewed_by_manager:
        complaint.reply_viewed_by_manager = True
        complaint.save()

    if request.method == 'POST':
        form = ManagerResponseForm(request.POST, instance=complaint)
        if form.is_valid():
            complaint = form.save(commit=False)
            complaint.response_submitted_at = timezone.now()
            complaint.save()
            return redirect('complaint_lists')
    else:
        form = ManagerResponseForm(instance=complaint)

    return render(request, 'respond_to_complaint.html', {
        'form': form,
        'complaint': complaint,
    })






# @login_required
# def view_complaint_response(request, complaint_id):
#     if request.user.role not in ['employer', 'job_applicant']:
#         return render(request, 'error.html', {'message': 'You do not have permission to view this page.'})

#     complaint = get_object_or_404(
#         Complaint, id=complaint_id, sender=request.user)

#     if complaint.manager_response and not complaint.response_viewed:
#         complaint.response_viewed = True
#         complaint.save()

#     if request.method == 'POST':
#         form = UserReplyForm(request.POST, instance=complaint)
#         if form.is_valid():
#             complaint = form.save(commit=False)
#             complaint.user_reply_submitted_at = timezone.now()  
#             complaint.reply_viewed_by_manager = False  
#             complaint.save()
#             return redirect('complaint_list')
#     else:
#         form = UserReplyForm(instance=complaint)

#     return render(request, 'view_complaint_response.html', {
#         'complaint': complaint,
#         'form': form,
#     })


@login_required
def view_complaints(request):
    complaints = Complaint.objects.filter(sender=request.user)
    return render(request, 'complaint_list.html', {'complaints': complaints})


@login_required
def view_all_complaints(request):
    if request.user.role != 'manager':
        return render(request, 'error.html', {'message': 'You do not have permission to view this page.'})

    complaints = Complaint.objects.all()
    return render(request, 'admin_complaint_list.html', {'complaints': complaints})




def search_jobs(request):
    query = request.GET.get('q')  
    results = []
    
    if query:
        results = JobPost.objects.filter(
            Q(job_title__icontains=query) | 
            Q(job_description__icontains=query) |  
            Q(country__icontains=query) |  
            Q(state__icontains=query) |  
            Q(job_type__icontains=query) |  
            Q(company__company_name__icontains=query) 
        )

    return render(request, 'search_results.html', {'results': results, 'query': query})


class UserListView(LoginRequiredMixin, ListView):
    model = CustomUser
    template_name = 'user_list.html'
    context_object_name = 'users'

    def get_queryset(self):
        return CustomUser.objects.all() 
    
class UserDetail(LoginRequiredMixin, DetailView):
    model = JobPost
    template_name = 'user_detail.html'
    context_object_name = 'user'

    

@login_required
def view_complaint_response(request, complaint_id):
    complaint = get_object_or_404(Complaint, id=complaint_id, sender=request.user)

    if complaint.manager_response and not complaint.response_viewed:
        complaint.response_viewed = True
        complaint.save()

    if request.method == 'POST':
        form = UserReplyForm(request.POST, instance=complaint)
        if form.is_valid():
            complaint = form.save(commit=False)
            complaint.user_reply_submitted_at = timezone.now()
            complaint.reply_viewed_by_manager = False 
            complaint.save()
            return redirect('complaint_list')
    else:
        form = UserReplyForm(instance=complaint)

    return render(request, 'view_complaint_response.html', {
        'complaint': complaint,
        'form': form,
    })