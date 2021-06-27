from django.apps import apps
from django.db import models
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
        else:
            super().delete()


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
        verbose_name = 'Designation'
        verbose_name_plural = 'Designations' 

    def __str__(self):
        return self.name

