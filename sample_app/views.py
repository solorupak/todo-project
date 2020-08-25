import json
import subprocess

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib.auth.views import (PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView)
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import render_to_string
from django.urls import resolve, reverse, reverse_lazy
from django.views.generic import *

from .forms import *
from .mixins import *
from .models import * 


class DashboardView(LoginRequiredMixin,  BaseMixin, TemplateView):
    template_name = 'dashboard/layouts/home.html'

class SignupPage(BaseMixin, CreateView):
    template_name = 'dashboard/layouts/signup.html'
    form_class = SignUpForm
    success_url = reverse_lazy('edu:home')

    def form_valid(self, form):
        username = form.cleaned_data.get('username')
        name = form.cleaned_data.get('name')
        position =form.cleaned_data.get('position')
        level = form.cleaned_data.get('level')
        email = form.cleaned_data.get('email')
        user = Candidate.objects.create(username=username, name=name, position=position, level=level, email = email)
        user.set_password(form.cleaned_data.get('password'))
        user.ip_address = get_ip(self.request)
        user.save()
        user = authenticate(username=username, password=form.cleaned_data.get('password'))
        login(self.request, user)
        return HttpResponseRedirect('/exam/list/')
    

    def form_invalid(self,form):
        print("form invalid")
        if self.request.is_ajax():
            return JsonResponse({'errors':form.errors},status=400)
        return super().form_invalid(form)

#Login Logout Views

class LoginPage(TemplateView):
    template_name = "dashboard/layouts/login.html"

    def get(self, request):
        form = LoginForm()
        return render(request, self.template_name, {'form': form})


    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            form = LoginForm()
            if user is not None:
                if user.is_active:
                    login(request, user)
                if 'next' in self.request.GET:
                    return HttpResponseRedirect(self.next_page)
                if self.request.user.is_superuser:
                    return HttpResponseRedirect('/designation/list/')
                else:
                    return HttpResponseRedirect('/designation/list/')
            else:
                return render(request, self.template_name, 
            {'form':form,'user': username,'error': 'Incorrect username or password'})


class LogoutView(View):

	def get(self, request):
		logout(request)
		return HttpResponseRedirect('/accounts/login/')


class DesignationList(CustomLoginRequiredMixin,ListView):
    template_name = "dashboard/designation/designation_list.html"
    context_object_name = "object_list"
    queryset = Designation.objects.filter(deleted_at__isnull=True).order_by('-created_at')


class DesignationCreate(CustomLoginRequiredMixin, SuccessMessageMixin, CreateView):
    template_name = "dashboard/designation/designation_form.html"
    form_class= DesignationForm
    model = Designation
    success_url = reverse_lazy('sample_app:designation-list')
    success_message = "Designation Created Successfully"


class DesignationDelete(CustomLoginRequiredMixin,SuccessMessageMixin, DeleteMixin):
    template_name = "dashboard/designation/designation_delete.html"
    model = Designation
    form_class = DesignationDeleteForm
    success_url = reverse_lazy('sample_app:designation-list')
    success_message = "Designation Deleted Successfully"


class DesignationUpdate(CustomLoginRequiredMixin, SuccessMessageMixin, UpdateView):
    template_name = "dashboard/designation/designation_form.html"
    model = Designation
    form_class = DesignationForm
    success_url = reverse_lazy('sample_app:designation-list')
    success_message = "Designation Updated Successfully"