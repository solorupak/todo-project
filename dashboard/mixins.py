
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash, get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import DeleteView


User = get_user_model()

class NonDeletedListMixin:
    def get_queryset(self):
        return super().get_queryset().filter(deleted_at__isnull=True)

class GetDeleteMixin:
    def get(self, request, *args, **kwargs):
        if hasattr(self, 'success_message'):
            messages.success(self.request, self.success_message)
        return super().delete(request, *args, **kwargs)

class SuperAdminRequiredMixin:
    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)
        return self.handle_no_permission()

class NonSuperAdminRequiredMixin:
    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)
        return self.handle_no_permission()

class NonLoginRequiredMixin:
    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('dashboard:index')
        return super().dispatch(request, *args, **kwargs)

class CustomLoginRequiredMixin(LoginRequiredMixin):
    login_url = reverse_lazy('dashboard:login')

    def dispatch(self,request,*args,**kwargs):
        if self.request.user.is_superuser or self.request.user.is_active:
            return super().dispatch(request, *args, **kwargs)
        return self.handle_no_permission()

class BaseMixin():
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        return context

class FormControlMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })


class GroupRequiredMixin(object):
    group_required = None

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_superuser or self.request.user.groups.filter(name__in=self.group_required).exists():
            return super().dispatch(request, *args, **kwargs)
        raise PermissionDenied