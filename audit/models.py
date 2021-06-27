from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()

# Audit Log which records transactions
class AuditTrail(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    model_type = models.CharField('Model Type', max_length=255)
    object_id = models.IntegerField('Model Id')
    object_str = models.CharField('Model Str', max_length=255)
    action = models.CharField(max_length=255)
    ip = models.GenericIPAddressField(null=True)
    instance = models.TextField(null=True)
    previous_instance = models.TextField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-id',)

    def __str__(self):
        return str(self.model_type) 
        