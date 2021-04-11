from django.contrib.auth import authenticate, login, logout, update_session_auth_hash, get_user_model
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import resolve, reverse, reverse_lazy
from django.views.generic import View, TemplateView, FormView, ListView, CreateView, UpdateView, DeleteView


from .forms import LoginForm, SignUpForm, DesignationForm
from .mixins import BaseMixin, CustomLoginRequiredMixin, GetDeleteMixin, NonDeletedListMixin, NonLoginRequiredMixin
from .models import Designation 

User = get_user_model()

class DashboardView(CustomLoginRequiredMixin,  BaseMixin, TemplateView):
    template_name = 'dashboard/index.html'

# Registration
class SignupView(BaseMixin, NonLoginRequiredMixin, CreateView):
    form_class = SignUpForm
    success_url = reverse_lazy('dashboard:index')
    template_name = 'dashboard/auth/signup.html'

    def form_valid(self, form):
        # saving user
        user = User.objects.create(
            username=form.cleaned_data.get('username'), 
            first_name=form.cleaned_data.get('first_name'), 
            last_name=form.cleaned_data.get('last_name'), 
            email = form.cleaned_data.get('username')
        )
        user.set_password(form.cleaned_data.get('password'))
        user.save()

        # logging in user after registration
        login(self.request, user)
        return redirect(self.success_url)

    def form_invalid(self,form):
        if self.request.is_ajax():
            return JsonResponse({'errors':form.errors}, status=400)
        return super().form_invalid(form)


# Login Logout Views
class LoginPageView(NonLoginRequiredMixin, FormView):
    form_class = LoginForm
    template_name = "dashboard/auth/login.html"

    def form_valid(self, form):
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user = authenticate(username=username, password=password)

        # Remember me
        if self.request.POST.get('remember', None) == None:
            self.request.session.set_expiry(0)

        login(self.request, user)
        if 'next' in self.request.GET:
            return redirect(self.request.GET.get('next'))
        return redirect('dashboard:index')
        
class LogoutView(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect('dashboard:login')


# Designation CRUD
class DesignationListView(CustomLoginRequiredMixin, NonDeletedListMixin, ListView):
    model = Designation
    template_name = "dashboard/designations/list.html"

    def get_querset(self):
        return super().get_queryset().order_by('-created_at')

class DesignationCreateView(CustomLoginRequiredMixin, SuccessMessageMixin, CreateView):
    form_class= DesignationForm
    success_message = "Designation Created Successfully"
    success_url = reverse_lazy('dashboard:designations-list')
    template_name = "dashboard/designations/form.html"

class DesignationUpdateView(CustomLoginRequiredMixin, NonDeletedListMixin, SuccessMessageMixin, UpdateView):
    form_class = DesignationForm
    model = Designation
    success_message = "Designation Updated Successfully"
    success_url = reverse_lazy('dashboard:designations-list')
    template_name = "dashboard/designations/form.html"

class DesignationDeleteView(CustomLoginRequiredMixin, NonDeletedListMixin, SuccessMessageMixin, GetDeleteMixin):
    model = Designation
    success_message = "Designation Deleted Successfully"
    success_url = reverse_lazy('dashboard:designations-list')
