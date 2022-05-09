from django.db import models
from django.utils.translation import gettext_lazy as _
from user.models import CustomUser, Student, Evaluator

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

class Incident(models.Model):
    student = models.ForeignKey(Student, related_name='student', on_delete=models.CASCADE)
    report_type = models.CharField(_('report type'), max_length=255)
    type_others = models.CharField(_('type others'), max_length=255)
    evaluator = models.ForeignKey(Evaluator, related_name='evaluator', on_delete=models.CASCADE)
    message = models.TextField(_('message'))
    details = models.CharField(_('details'), max_length=255)
    attachment = models.FileField(_('attachment'), upload_to='ticket-attachment/', blank=True, null=True)
    status = models.CharField(_('status'), max_length=20)
    date_created = models.DateTimeField(_('date created'), auto_now_add=True)
    date_updated = models.DateTimeField(_('date updated'), auto_now=True)
    date_completed = models.DateTimeField(_('date completed'), null=True, blank=True)

    def __str__(self):
        return self.id
    class Meta:
        db_table = 'incident'

# class Followup(models.Model):
#     incident = models.ForeignKey(Incident, related_name='incident', on_delete=models.CASCADE)
#     user = models.ForeignKey(CustomUser, related_name='user', on_delete=models.SET_NULL)
#     message = models.TextField(_('message'))
#     attachment = models.FileField(_('attachment'), upload_to='ticket-attachment/', blank=True, null=True)
#     is_solution = models.BooleanField(default=False)

#     def __str__(self):
#         return self.id
#     class Meta:
#         db_table = 'incident_follow_up'

# class Notification(models.Model):
#     incident = models.ForeignKey(Incident, related_name='incident', on_delete=models.CASCADE)
#     receiver = models.ForeignKey(CustomUser, related_name='receiver', on_delete=models.CASCADE)
#     message = models.TextField(_('message'))
#     is_read = models.BooleanField(default=False)
#     date_created = models.DateTimeField(_('date created'), auto_now_add=True)

#     def __str__(self):
#         return self.id
#     class Meta:
#         db_table = 'notification'