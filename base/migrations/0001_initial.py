# Generated by Django 4.0.4 on 2022-05-14 10:07

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.db.models.manager


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='email address')),
                ('picture', models.ImageField(blank=True, default='user.png', upload_to='profile-picture/')),
                ('last_name', models.CharField(max_length=100, verbose_name='last name')),
                ('first_name', models.CharField(max_length=100, verbose_name='first name')),
                ('middle_initial', models.CharField(blank=True, max_length=10, null=True, verbose_name='middle initial')),
                ('mobile_number', models.CharField(blank=True, max_length=15, null=True, verbose_name='mobile number')),
                ('role', models.PositiveSmallIntegerField(choices=[(1, 'admin'), (2, 'evaluator'), (3, 'student')], default=3)),
                ('is_active', models.BooleanField(default=True, verbose_name='active status')),
                ('is_staff', models.BooleanField(default=False, verbose_name='staff status')),
                ('is_superuser', models.BooleanField(default=False, verbose_name='superuser status')),
                ('date_joined', models.DateTimeField(auto_now_add=True, verbose_name='date joined')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'db_table': 'user',
            },
        ),
        migrations.CreateModel(
            name='Evaluator',
            fields=[
                ('employee_number', models.IntegerField(primary_key=True, serialize=False, unique=True, verbose_name='employee number')),
                ('position', models.CharField(max_length=100, verbose_name='position')),
                ('residential_address', models.CharField(max_length=255, verbose_name='residential address')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='evaluator', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'evaluator',
            },
            managers=[
                ('object', django.db.models.manager.Manager()),
            ],
        ),
        migrations.CreateModel(
            name='Incident',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('report_type', models.CharField(max_length=255, verbose_name='report type')),
                ('type_others', models.CharField(blank=True, max_length=255, null=True, verbose_name='type others')),
                ('message', models.TextField(verbose_name='message')),
                ('details', models.CharField(blank=True, max_length=255, null=True, verbose_name='details')),
                ('file', models.FileField(blank=True, null=True, upload_to='files/', verbose_name='file')),
                ('status', models.CharField(default='Open', max_length=20, verbose_name='status')),
                ('date_created', models.DateTimeField(auto_now_add=True, verbose_name='date created')),
                ('date_updated', models.DateTimeField(auto_now=True, verbose_name='date updated')),
                ('date_completed', models.DateTimeField(blank=True, null=True, verbose_name='date completed')),
                ('evaluator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='evaluator', to='base.evaluator')),
            ],
            options={
                'db_table': 'incident',
            },
            managers=[
                ('object', django.db.models.manager.Manager()),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('student_number', models.IntegerField(primary_key=True, serialize=False, unique=True, verbose_name='student number')),
                ('year_level', models.CharField(max_length=10, verbose_name='year level')),
                ('section', models.CharField(max_length=10, verbose_name='section')),
                ('residential_address', models.CharField(max_length=255, verbose_name='residential address')),
                ('permanent_address', models.CharField(max_length=255, verbose_name='permanent address')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='student', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'student',
            },
            managers=[
                ('object', django.db.models.manager.Manager()),
            ],
        ),
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject', models.CharField(max_length=100, verbose_name='subject')),
                ('message', models.TextField(verbose_name='message')),
                ('is_read', models.BooleanField(default=False)),
                ('date_created', models.DateTimeField(auto_now_add=True, verbose_name='date created')),
                ('incident', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='incident_notif', to='base.incident')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_notif', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'notification',
            },
            managers=[
                ('object', django.db.models.manager.Manager()),
            ],
        ),
        migrations.AddField(
            model_name='incident',
            name='student',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='student', to='base.student'),
        ),
        migrations.CreateModel(
            name='Followup',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.TextField(verbose_name='message')),
                ('file', models.FileField(blank=True, null=True, upload_to='files/', verbose_name='file')),
                ('is_solution', models.BooleanField(default=False)),
                ('incident', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='incident_followup', to='base.incident')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_followup', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'incident_follow_up',
            },
            managers=[
                ('object', django.db.models.manager.Manager()),
            ],
        ),
    ]