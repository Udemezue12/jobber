import logging
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
from django.contrib.auth.models import User, AbstractUser, Group, Permission
from django.db import models
from .doc import image, document


# Configure logging (optional, but useful for debugging)
logger = logging.getLogger(__name__)


class CustomUser(AbstractUser):
    EMPLOYER = 'employer'
    JOB_APPLICANT = 'job_applicant'
    MANAGER = 'manager'

    ROLE_CHOICES = [
        (EMPLOYER, 'Employer'),
        (JOB_APPLICANT, 'Job Applicant'),
        (MANAGER, 'manager'),
    ]
    phone_number = models.CharField(max_length=15, null=True, blank=True)

    country = models.CharField(max_length=100, null=False, blank=False)
    state = models.CharField(max_length=100, null=False, blank=False)
    role = models.CharField(
        max_length=20, choices=ROLE_CHOICES, default=JOB_APPLICANT, null=False)

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
    personal_details = models.TextField(null=True, blank=True)
    picture = models.ImageField(upload_to=image, null=True, blank=True)


class CompanyProfile(models.Model):
    user = models.OneToOneField(
        CustomUser, on_delete=models.CASCADE, related_name='company_profile')
    company_name = models.CharField(max_length=100, null=False, blank=False)
    company_address = models.CharField(max_length=100, null=False, blank=False)
    company_logo = models.ImageField(upload_to=image, null=True, blank=True)
    hiring_needs = models.TextField()
    business_info = models.TextField()


class JobPost(models.Model):
    user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name='posted_jobs')
    job_title = models.CharField(max_length=100)
    job_description = models.TextField()
    country = models.CharField(max_length=100, null=False, blank=False)
    state = models.CharField(max_length=100, null=False, blank=False)
    job_type = models.CharField(max_length=50, choices=[
        ('Full-time', 'Full-time'),
        ('Part-time', 'Part-time'),
        ('Freelance', 'Freelance'),
        ('Contract', 'Contract')
    ])
    expiry_date = models.DateField(null=True, blank=True)
    job_salary = models.DecimalField(max_digits=10, decimal_places=2)
    job_requirements = models.TextField()
    job_posted_date = models.DateTimeField(auto_now_add=True)
    company = models.ForeignKey(CompanyProfile, on_delete=models.CASCADE,
                                related_name='company_job_posts', null=False, blank=False)

    def is_expired(self):
        return self.expiry_date and self.expiry_date < timezone.now().date()


class Notification(models.Model):
    recipient = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name='notifications')
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification for {self.recipient} - {self.message[:20]}"

    @staticmethod
    def notify_user(recipient, message):
        """Utility function to create a notification for a user with error handling."""
        try:
            if not isinstance(recipient, CustomUser):
                raise ValueError(
                    "Recipient must be a valid CustomUser instance.")

            Notification.objects.create(recipient=recipient, message=message)
            logger.info(f"Notification sent to {recipient.email}: {message}")

        except ObjectDoesNotExist:
            logger.error(f"Recipient {recipient} does not exist.")
            return False

        except ValueError as ve:
            logger.error(f"ValueError: {ve}")
            return False

        except Exception as e:
            logger.error(f"Failed to send notification: {e}")
            return False

        return True


class Application(models.Model):
    user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name='user_applications')
    job_post = models.ForeignKey(
        JobPost, on_delete=models.CASCADE, related_name='job_applications')
    resume = models.FileField(upload_to=document, null=False)
    cover_letter = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, choices=[(
        'pending', 'Pending'), ('reviewed', 'Reviewed'), ('rejected', 'Rejected')])


class Complaint(models.Model):
    SENDER_ROLE_CHOICES = [
        ('employer', 'Employer'),
        ('job_applicant', 'Job Applicant'),
    ]

    sender = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name='sent_complaints')
    sender_role = models.CharField(max_length=20, choices=SENDER_ROLE_CHOICES)
    manager = models.ForeignKey(CustomUser, on_delete=models.CASCADE,
                              related_name='received_complaints', limit_choices_to={'role': 'manager'})
    subject = models.CharField(max_length=255)
    message = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)
    manager_response = models.TextField(
        null=True, blank=True)  
    response_submitted_at = models.DateTimeField(null=True, blank=True)
    response_viewed = models.BooleanField(default=False)

    def __str__(self):
        return f"Complaint from {self.sender} ({self.sender_role}) to Manager"
