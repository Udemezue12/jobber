from django.contrib.auth.models import User,AbstractUser, Group, Permission
from django.db import models
from .doc import image, document

class CustomUser(AbstractUser):
    EMPLOYER = 'employer'
    JOB_APPLICANT = 'job_applicant'
    
    ROLE_CHOICES = [
        (EMPLOYER, 'Employer'),
        (JOB_APPLICANT, 'Job Applicant'),
    ]
    
    country = models.CharField(max_length=100, null=False, blank=False)
    state = models.CharField(max_length=100, null=False, blank=False)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default=JOB_APPLICANT, null=False)

    groups = models.ManyToManyField(
        Group,
        related_name='custom_user_set',
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        related_query_name='custom_user',
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='custom_user_set',
        blank=True,
        help_text='Specific permissions for this user.',
        related_query_name='custom_user',
    )

    def __str__(self):
        return self.username
    
    def get_company(self):
        try:
            return self.companyprofile
        except CompanyProfile.DoesNotExist:
            return None


class Profile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    resume = models.FileField(upload_to=document, null=True, blank=True)
    personal_details= models.TextField(null=True, blank=True)
    # is_employer = models.BooleanField(default=False)



class CompanyProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='company_profile')
    company_name = models.CharField(max_length=100, null=False, blank=False)
    company_address = models.CharField(max_length=100, null=False, blank=False)
    company_logo = models.ImageField(upload_to=image, null=True, blank=True)
    hiring_needs = models.TextField()
    business_info = models.TextField()
    

class JobPost(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='job_poster')
    job_title = models.CharField(max_length=100, null=False, blank=False)
    job_description = models.TextField(null=False, blank=False)
    job_location = models.CharField(max_length=100, null=False, blank=False)
    job_type = models.CharField(max_length=100, null=False, blank=False)
    job_salary = models.CharField(max_length=100, null=False, blank=False)
    job_requirements = models.TextField(null=False, blank=False)
    job_posted_date = models.DateTimeField(auto_now_add=True)
    company = models.ForeignKey(CompanyProfile, on_delete=models.CASCADE, related_name='company_job_posts', null=False, blank=False)

    
    


class Application(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='user_applications')
    job_post = models.ForeignKey(JobPost, on_delete=models.CASCADE, related_name='job_applications')
    resume = models.FileField(upload_to=document, null=False)
    cover_letter = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, choices=[('pending', 'Pending'), ('reviewed', 'Reviewed'), ('rejected', 'Rejected')])

