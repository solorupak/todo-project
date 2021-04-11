import json
import subprocess

from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import resolve, reverse, reverse_lazy
from django.views.generic import View, TemplateView, FormView, ListView, CreateView, UpdateView, DeleteView

from .forms import LoginForm, SignUpForm, DesignationForm
from .mixins import BaseMixin, CustomLoginRequiredMixin, GetDeleteMixin
from .models import Designation 


class DashboardView(CustomLoginRequiredMixin,  BaseMixin, TemplateView):
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

class LoginPageView(FormView):
    template_name = "dashboard/auth/login.html"
    form_class = LoginForm


    def form_valid(self, form):
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user = authenticate(username=username, password=password)
        login(self.request, user)
        if 'next' in self.request.GET:
            return redirect(self.request.GET.get('next'))
        return redirect('sample_app:home')
        

class LogoutView(View):

	def get(self, request):
		logout(request)
		return redirect('sample_app:login')


#Designation CRUD
class DesignationListView(CustomLoginRequiredMixin,ListView):
    model = Designation
    template_name = "dashboard/designations/list.html"
    context_object_name = "object_list"
    # queryset = Designation.objects.filter(deleted_at__isnull=True).order_by('-created_at')

    def get_querset(self):
        return super().get_queryset(deleted_at__isnull=True).order_by('-created_at')

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class DesignationCreateView(CustomLoginRequiredMixin, SuccessMessageMixin, CreateView):
    template_name = "dashboard/designations/form.html"
    form_class= DesignationForm
    model = Designation
    success_url = reverse_lazy('sample_app:designation-list')
    success_message = "Designation Created Successfully"

    def get_querset(self):
        return super().get_queryset(deleted_at__isnull=True).order_by('-created_at')
    
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
    
    def form_valid(self, form):
        return super().form_valid(form)

    def form_invalid(self, form):
        return super().form_valid(form)


class DesignationUpdateView(CustomLoginRequiredMixin, SuccessMessageMixin, UpdateView):
    template_name = "dashboard/designations/form.html"
    model = Designation
    form_class = DesignationForm
    success_url = reverse_lazy('sample_app:designation-list')
    success_message = "Designation Updated Successfully"

    def get_querset(self):
        return super().get_queryset(deleted_at__isnull=True).order_by('-created_at')
    
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
    
    def form_valid(self, form):
        return super().form_valid(form)

    def form_invalid(self, form):
        return super().form_valid(form)


class DesignationDeleteView(CustomLoginRequiredMixin,SuccessMessageMixin, GetDeleteMixin):
    model = Designation
    success_url = reverse_lazy('sample_app:designation-list')
    success_message = "Designation Deleted Successfully"

    def get_querset(self):
        return super().get_queryset(deleted_at__isnull=True).order_by('-created_at')