from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class DateTimeModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, auto_now=False,)
    updated_at = models.DateTimeField(auto_now_add=False, auto_now=True,)
    deleted_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        abstract = True

    def delete(self):
        self.deleted_at = timezone.now()
        super().save()


class Designation(DateTimeModel):
    name = models.CharField(max_length=100)
    position = models.CharField(max_length=140)

    def __str__(self):
        return self.name