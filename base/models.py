from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from djongo import models
from django.utils.translation import gettext_lazy as _

class CustomAccountManager(BaseUserManager):
    def create_superuser(self, email, password, **other_fields):
        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)
        other_fields.setdefault('role', 1)

        if other_fields.get('is_staff') is not True:
            raise ValueError(
                'Superuser must be assigned to is_staff=True.')
        if other_fields.get('is_superuser') is not True:
            raise ValueError(
                'Superuser must be assigned to is_superuser=True.')

        return self.create_user(email, password, **other_fields)

    def create_user(self, email, password, **other_fields):
        if not email:
            raise ValueError(_('You must provide an email address'))

        email = self.normalize_email(email)
        user = self.model(email=email, **other_fields)
        user.set_password(password)
        user.save()
        return user

class CustomUser(AbstractBaseUser, PermissionsMixin):
    ADMIN = 1
    EVALUATOR = 2
    STUDENT = 3

    ROLE_CHOICES = (
        (ADMIN, 'admin'),
        (EVALUATOR, 'evaluator'),
        (STUDENT, 'student')
    )

    email = models.EmailField(_('email address'), unique=True)
    picture = models.ImageField(default='user.png', upload_to='profile-picture/', blank=True)
    last_name = models.CharField(_('last name'), max_length=100)
    first_name = models.CharField(_('first name'), max_length=100)
    middle_initial = models.CharField(_('middle initial'), max_length=10, null=True, blank=True)
    mobile_number = models.CharField(_('mobile number'), max_length=15, null=True, blank=True)
    role = models.PositiveSmallIntegerField(choices=ROLE_CHOICES, default=3)
    is_active = models.BooleanField(_('active status'), default=True)
    is_staff = models.BooleanField(_('staff status'), default=False)
    is_superuser = models.BooleanField(_('superuser status'), default=False)
    date_joined = models.DateTimeField(_('date joined'), auto_now_add=True)
    last_login = models.DateTimeField(_('last login'), blank=True, null=True)

    objects = CustomAccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email
    class Meta:
        db_table = 'user'
        verbose_name = 'user'
        verbose_name_plural = 'users'

class Evaluator(models.Model):
    employee_number = models.IntegerField(_('employee number'), primary_key=True, unique=True)
    position = models.CharField(_('position'), max_length=100)
    residential_address = models.CharField(_('residential address'), max_length=255, null=True, blank=True)
    user = models.OneToOneField(CustomUser, related_name='evaluator', on_delete=models.CASCADE)

    # object = models.DjongoManager()

    def __str__(self):
        return self.user.email
    class Meta:
        db_table = 'evaluator'

class Student(models.Model):
    student_number = models.IntegerField(_('student number'), primary_key=True, unique=True)
    year_level = models.CharField(_('year level'), max_length=10)
    section = models.CharField(_('section'), max_length=10)
    residential_address = models.CharField(_('residential address'), max_length=255, null=True, blank=True)
    permanent_address = models.CharField(_('permanent address'), max_length=255, null=True, blank=True)
    user = models.OneToOneField(CustomUser, related_name='student', on_delete=models.CASCADE)

    # object = models.DjongoManager()

    def __str__(self):
        return self.user.email
    class Meta:
        db_table = 'student'


# Other tables
class Incident(models.Model):
    student = models.ForeignKey(Student, related_name='student', on_delete=models.CASCADE)
    report_type = models.CharField(_('report type'), max_length=255)
    report_title = models.CharField(_('report title'), max_length=255, null=True, blank=True)
    evaluator = models.ForeignKey(Evaluator, related_name='evaluator', on_delete=models.CASCADE, null=True, blank=True)
    report_details = models.TextField(_('report details'), null=True, blank=True)
    subject_add = models.CharField(_('subject add'), max_length=255, null=True, blank=True)
    file = models.FileField(_('file'), upload_to='files/', blank=True, null=True)
    status = models.CharField(_('status'), max_length=20, default='Open')
    date_created = models.DateTimeField(_('date created'), auto_now_add=True)
    date_updated = models.DateTimeField(_('date updated'), auto_now=True)
    date_completed = models.DateTimeField(_('date completed'), null=True, blank=True)

    # object = models.DjongoManager()

    def __str__(self):
        return f'{self.report_type} | #{self.id}'
    class Meta:
        db_table = 'incident'
        # ordering = ['-date_created']

class Followup(models.Model):
    incident = models.ForeignKey(Incident, related_name='incident_followup', on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, related_name='user_followup', on_delete=models.CASCADE)
    message = models.TextField(_('message'))
    file = models.FileField(_('file'), upload_to='files/', blank=True, null=True)
    is_solution = models.BooleanField(default=False)
    date_created = models.DateTimeField(_('date created'), auto_now_add=True)

    # object = models.DjongoManager()

    def __str__(self):
        return str(self.id)
    class Meta:
        db_table = 'incident_follow_up'
        ordering = ['-date_created']

class Notification(models.Model):
    incident = models.ForeignKey(Incident, related_name='incident_notif', on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, related_name='user_notif', on_delete=models.CASCADE)
    subject = models.CharField(_('subject'), max_length=100)
    message = models.TextField(_('message'))
    is_read = models.BooleanField(default=False)
    date_created = models.DateTimeField(_('date created'), auto_now_add=True)

    # object = models.DjongoManager()

    def __str__(self):
        return str(self.id)
    class Meta:
        db_table = 'notification'
        ordering = ['-date_created']


class News(models.Model):
    title = models.CharField(_('title'), max_length=255)
    description = models.TextField(_('description'))
    news_date = models.DateTimeField(_('news date'), )
    location = models.CharField(_('location'), max_length=255)
    attachment = models.ImageField(_('attachment'), upload_to='news-attachment/', blank=True, null=True)
    date_created = models.DateTimeField(_('date created'), auto_now_add=True)
    date_updated = models.DateTimeField(_('date updated'), auto_now=True)

    def __str__(self):
        return self.title
    class Meta:
        db_table = 'news'
        verbose_name = 'news'
        verbose_name_plural = 'news'

class Event(models.Model):
    title = models.CharField(_('title'), max_length=255)
    description = models.TextField(_('description'), )
    start_date = models.DateTimeField(_('start date'), )
    end_date = models.DateTimeField(_('end date'), )
    attendee = models.CharField(_('attendees'), max_length=255)
    location = models.CharField(_('location'), max_length=255)
    attachment = models.ImageField(_('attachment'), upload_to='event-attachment/', blank=True, null=True)
    date_created = models.DateTimeField(_('date created'), auto_now_add=True)
    date_updated = models.DateTimeField(_('date updated'), auto_now=True)

    def __str__(self):
        return self.title
    class Meta:
        db_table = 'event'