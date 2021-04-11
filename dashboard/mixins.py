import datetime

from django.contrib.auth.mixins import LoginRequiredMixin
# from braces.views import GroupRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import DeleteView
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse

from .models import *


class CustomLoginRequiredMixin(LoginRequiredMixin):
	login_url = reverse_lazy('dashboard:login')

	def dispatch(self,request,*args,**kwargs):
		if self.request.user.is_superuser:
			return super().dispatch(request, *args, **kwargs)
		return self.handle_no_permission()

class GetDeleteMixin(DeleteView):
	def get(self, request, *args, **kwargs):
		if hasattr(self, 'success_message'):
			messages.success(self.request, self.success_message)
		return super().post(request, *args, **kwargs)

class BaseMixin():

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        return context