from django.db import models
from djongo import models
from django.utils.translation import gettext_lazy as _

class Incident(models.Model):
    student_id = models.CharField(_('student'), max_length=100)
    report_type = models.CharField(_('report type'), max_length=255)
    type_others = models.CharField(_('type others'), max_length=255, null=True, blank=True)
    evaluator_id = models.CharField(_('evaluator'), max_length=100)
    message = models.TextField(_('message'))
    details = models.CharField(_('details'), max_length=255, null=True, blank=True)
    attachment = models.FileField(_('attachment'), upload_to='ticket-attachment/', blank=True, null=True)
    status = models.CharField(_('status'), max_length=20)
    date_created = models.DateTimeField(_('date created'), auto_now_add=True)
    date_updated = models.DateTimeField(_('date updated'), auto_now=True)
    date_completed = models.DateTimeField(_('date completed'), null=True, blank=True)

    object = models.DjongoManager()

    def __str__(self):
        return str(self.report_type)
    class Meta:
        db_table = 'incident'

class Followup(models.Model):
    incident = models.ForeignKey(Incident, related_name='incident', on_delete=models.CASCADE)
    user_id = models.CharField(_('user'), max_length=100)
    message = models.TextField(_('message'))
    attachment = models.FileField(_('attachment'), upload_to='ticket-attachment/', blank=True, null=True)
    is_solution = models.BooleanField(default=False)

    object = models.DjongoManager()

    def __str__(self):
        return str(self.id)
    class Meta:
        db_table = 'incident_follow_up'

class Notification(models.Model):
    incident = models.ForeignKey(Incident, related_name='incident_notif', on_delete=models.CASCADE)
    user_id = models.CharField(_('user'), max_length=100)
    message = models.TextField(_('message'))
    is_read = models.BooleanField(default=False)
    date_created = models.DateTimeField(_('date created'), auto_now_add=True)

    object = models.DjongoManager()

    def __str__(self):
        return str(self.id)
    class Meta:
        db_table = 'notification'