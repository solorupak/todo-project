from django.contrib.auth import get_user_model
from django.db import models
from dashboard.models import DateTimeModel

User = get_user_model()

# Create your models here.


class Task(DateTimeModel):
    user = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True)
    title = models.CharField(
        default="Untitled", null=True, blank=True, max_length=255)
    description = models.TextField(null=True, blank=True)
    last_date = models.DateTimeField()
    is_completed = models.BooleanField(default=False, null=True, blank=True)
    is_important = models.BooleanField(default=False)
    is_missed = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Task'
        verbose_name_plural = 'Tasks'

    def __str__(self):
        return self.title
