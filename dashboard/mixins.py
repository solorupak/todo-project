from django.contrib.auth import authenticate, login, logout, update_session_auth_hash, get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import DeleteView

User = get_user_model()

class NonDeletedListMixin:
	def get_querset(self):
		return super().get_querset(deleted_at__isnull=True)

class GetDeleteMixin(DeleteView):
	def get(self, request, *args, **kwargs):
		if hasattr(self, 'success_message'):
			messages.success(self.request, self.success_message)
		return super().post(request, *args, **kwargs)

class NonLoginRequiredMixin:
    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated and User.objects.filter(username=self.request.user.username, is_active=True).exists():
            return redirect('dashboard:index')
        return super().dispatch(request, *args, **kwargs)

class CustomLoginRequiredMixin(LoginRequiredMixin):
	login_url = reverse_lazy('dashboard:login')

	def dispatch(self,request,*args,**kwargs):
		if self.request.user.is_superuser:
			return super().dispatch(request, *args, **kwargs)
		return self.handle_no_permission()

class BaseMixin():
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        return context