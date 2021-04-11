from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class DateTimeModel(models.Model):
    created_at = models.DateTimeField(
        auto_now_add=True,
        auto_now=False,
    )
    updated_at = models.DateTimeField(
        auto_now_add=False,
        auto_now=True,
    )
    deleted_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        abstract = True

    def delete(self, hard=False):
        if not hard:
            self.deleted_at = timezone.now()
            super().save()
        return super().delete()


class Designation(DateTimeModel):
    name = models.CharField(max_length=255)
    position = models.CharField(max_length=255)
    gender = models.CharField(max_length=255, choices=(
        ('FEMALE', 'FEMALE'),
        ('MALE', 'MALE'),
        ('OTHERS', 'OTHERS'),
    ))
    date_of_birth = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["name"]
        verbose_name = 'designation'
        verbose_name_plural = 'designations' 


    def __str__(self):
        return self.name