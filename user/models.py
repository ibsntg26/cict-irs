from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
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
    residential_address = models.CharField(_('residential address'), max_length=255)
    user = models.OneToOneField(CustomUser, related_name='evaluator', on_delete=models.CASCADE)

    def __str__(self):
        return self.user.email
    class Meta:
        db_table = 'evaluator'

class Student(models.Model):
    student_number = models.IntegerField(_('student number'), primary_key=True, unique=True)
    year_level = models.CharField(_('year level'), max_length=10)
    section = models.CharField(_('section'), max_length=10)
    residential_address = models.CharField(_('residential address'), max_length=255)
    permanent_address = models.CharField(_('permanent address'), max_length=255)
    user = models.OneToOneField(CustomUser, related_name='student', on_delete=models.CASCADE)

    def __str__(self):
        return self.user.email
    class Meta:
        db_table = 'student'