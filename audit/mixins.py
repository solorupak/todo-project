from .utils import store_audit

class AuditCreateMixin:
    def form_valid(self, form):
        store_audit(request=self.request, instance=form.save(), action='CREATE')
        return super().form_valid(form)

class AuditUpdateMixin:
    def form_valid(self, form):
        store_audit(request=self.request, instance=form.save(), action='UPDATE', previous_instance=self.get_object())
        return super().form_valid(form)

class AuditDeleteMixin:
    def delete(self, request, *args, **kwargs):
        store_audit(request=self.request, instance=self.get_object(), action='DELETE', previous_instance=self.get_object())
        return super().delete(request, *args, **kwargs)