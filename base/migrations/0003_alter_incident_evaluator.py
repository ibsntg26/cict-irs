# Generated by Django 4.0.4 on 2022-05-14 13:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0002_alter_evaluator_managers_alter_followup_managers_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='incident',
            name='evaluator',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='evaluator', to='base.evaluator'),
        ),
    ]