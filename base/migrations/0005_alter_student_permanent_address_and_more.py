# Generated by Django 4.0.4 on 2022-05-16 17:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0004_event_news'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='permanent_address',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='permanent address'),
        ),
        migrations.AlterField(
            model_name='student',
            name='residential_address',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='residential address'),
        ),
    ]
