from django.apps import apps
from django.db import models
from django.db.models.fields import DateTimeField
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


class Enquery(DateTimeModel):
    client_name = models.CharField(max_length=255)
    contact = models.CharField(max_length=255)
    event_dates = models.CharField(max_length=255)
    services = models.CharField(max_length=255)
    reference_no = models.CharField(max_length=255)
    followup_1 = models.DateTimeField(null=True, blank=True)
    followup_2 = models.DateTimeField(null=True, blank=True)
    followup_3 = models.DateTimeField(null=True, blank=True)
    is_booked = models.BooleanField(default=False, null=True, blank=True)
    is_cancelled = models.BooleanField(default=False, null=True, blank=True)

    class Meta:
        verbose_name = ('Enquery')
        verbose_name_plural = ('Enqueries')
        ordering = ['client_name']

    def __str__(self):
        return self.client_name


class Ticket(DateTimeModel):
    bill_no = models.PositiveBigIntegerField(default=0, unique=True)
    client_name = models.CharField(max_length=255)
    events = models.CharField(max_length=255)
    date = models.DateTimeField()
    assigned_to = models.CharField(max_length=255)
    assigned_time = models.DateTimeField()
    accepted_time = models.DateTimeField()
    completed_time = models.DateTimeField(null=True, blank=True)
    pending_time = models.DateTimeField(null=True, blank=True)
    is_completed = models.BooleanField(default=True)
    copied_to = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        verbose_name = ('Ticket')
        verbose_name_plural = ('Tickets')
        ordering = ['bill_no']

    def __str__(self):
        return self.bill_no
