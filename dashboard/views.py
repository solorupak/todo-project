from django.conf import settings as conf_settings
from django.core.mail import send_mail
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash, get_user_model
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import resolve, reverse, reverse_lazy
from django.utils.crypto import get_random_string
from django.views.generic import View, TemplateView, FormView, ListView, CreateView, UpdateView, DeleteView


from .forms import ChangePasswordForm, LoginForm, SignUpForm, DesignationForm, UserForm
from .mixins import BaseMixin, AuditCreateMixin, AuditUpdateMixin, AuditDeleteMixin, CustomLoginRequiredMixin, GetDeleteMixin, NonDeletedListMixin, NonLoginRequiredMixin, NonSuperAdminRequiredMixin, SuperAdminRequiredMixin
from .models import AuditTrail, Designation 
from .audits import store_audit

User = get_user_model()

class DashboardView(CustomLoginRequiredMixin,  BaseMixin, TemplateView):
    template_name = 'dashboard/index.html'

# Git Pull View
class GitPullView(CustomLoginRequiredMixin, SuperAdminRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        import subprocess
        process = subprocess.Popen(['./pull.sh'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        returncode = process.wait()
        output = ''
        output += process.stdout.read().decode("utf-8")
        output += '\nReturned with status {0}'.format(returncode)
        response = HttpResponse(output)
        response['Content-Type'] = 'text'
        return response

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
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(username=username, password=password)

        # Remember me
        if self.request.POST.get('remember', None) == None:
            self.request.session.set_expiry(0)

        login(self.request, user)
        store_audit(request= self.request, instance=self.request.user, action='LOGIN')

        if 'next' in self.request.GET:
            return redirect(self.request.GET.get('next'))
        return redirect('dashboard:index')
        
class LogoutView(CustomLoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        store_audit(request= self.request, instance=self.request.user, action='LOGOUT')
        logout(request)
        return redirect('dashboard:login')

# Password Reset
class ChangePasswordView(CustomLoginRequiredMixin, SuccessMessageMixin, FormView):
    form_class = ChangePasswordForm
    template_name = "dashboard/auth/change_password.html"
    success_message = "Password Has Been Changed"
    success_url = reverse_lazy('dashboard:index')

    def get_form(self):
        form = super().get_form()
        form.set_user(self.request.user)
        return form

    def form_valid(self, form):
        account = User.objects.filter(username=self.request.user).first()
        account.set_password(form.cleaned_data.get('confirm_password'))
        account.save(update_fields=['password'])
        user = authenticate(username=self.request.user, password=form.cleaned_data.get('confirm_password'))
        login(self.request, user)
        return super().form_valid(form)


# Designation CRUD
class DesignationListView(CustomLoginRequiredMixin, NonDeletedListMixin, ListView):
    model = Designation
    template_name = "dashboard/designations/list.html"
    paginate_by = 100

    def get_queryset(self):
        return super().get_queryset().order_by('-created_at')

class DesignationCreateView(CustomLoginRequiredMixin, SuccessMessageMixin, AuditCreateMixin, CreateView):
    form_class= DesignationForm
    success_message = "Designation Created Successfully"
    success_url = reverse_lazy('dashboard:designations-list')
    template_name = "dashboard/designations/form.html"

class DesignationUpdateView(CustomLoginRequiredMixin, NonDeletedListMixin, SuccessMessageMixin, AuditUpdateMixin, UpdateView):
    form_class = DesignationForm
    model = Designation
    success_message = "Designation Updated Successfully"
    success_url = reverse_lazy('dashboard:designations-list')
    template_name = "dashboard/designations/form.html"

class DesignationDeleteView(CustomLoginRequiredMixin, NonDeletedListMixin, SuccessMessageMixin, GetDeleteMixin, AuditDeleteMixin, DeleteView):
    model = Designation
    success_message = "Designation Deleted Successfully"
    success_url = reverse_lazy('dashboard:designations-list')


# User CRUD
class UserListView(CustomLoginRequiredMixin, SuperAdminRequiredMixin, ListView):
    model = User
    template_name = "dashboard/users/list.html"
    paginate_by = 100

    def get_queryset(self):
        return super().get_queryset().exclude(username=self.request.user)

class UserCreateView(CustomLoginRequiredMixin, SuperAdminRequiredMixin, SuccessMessageMixin, AuditCreateMixin, CreateView):
    form_class= UserForm
    success_message = "User Created Successfully"
    success_url = reverse_lazy('dashboard:users-list')
    template_name = "dashboard/users/form.html"

    def get_success_url(self):
        return reverse('dashboard:users-password-reset', kwargs={'pk': self.object.pk })

class UserUpdateView(CustomLoginRequiredMixin, SuperAdminRequiredMixin, SuccessMessageMixin, AuditUpdateMixin, UpdateView):
    form_class = UserForm
    model = User
    success_message = "User Updated Successfully"
    success_url = reverse_lazy('dashboard:users-list')
    template_name = "dashboard/users/form.html"

class UserStatusView(CustomLoginRequiredMixin, SuperAdminRequiredMixin, SuccessMessageMixin, View):
    model = User
    success_message = "User's Status Has Been Changed"
    success_url = reverse_lazy('dashboard:users-list')

    def get(self, request, *args, **kwargs):
        user_id = self.kwargs['pk']
        if user_id:
            account = User.objects.filter(pk=user_id).first()
            if account.is_active == True:
                account.is_active = False
            else:
                account.is_active = True
            account.save(update_fields=['is_active'])
        return redirect(self.success_url)


# Password Reset
class UserPasswordResetView(CustomLoginRequiredMixin, SuperAdminRequiredMixin, SuccessMessageMixin, View):
    model = User
    success_url = reverse_lazy("dashboard:users-list")
    success_message = "Password has been sent to the user's email."

    def get(self, request, *args, **kwargs):
        user_pk = self.kwargs["pk"]
        account = User.objects.filter(pk=user_pk).first()
        password = get_random_string(length=6)
        account.set_password(password)
        msg = (
            "You can login into the Dashboard with the following credentials.\n\n" + "Username: " + account.username + " \n" + "Password: " + password
        )
        send_mail("Dashboard Credentials", msg, conf_settings.EMAIL_HOST_USER, [account.email], fail_silently=True)
        account.save(update_fields=["password"])

        messages.success(self.request, self.success_message)
        return redirect(self.success_url)

# AuditTrail List
class AuditTrailListView(CustomLoginRequiredMixin, SuperAdminRequiredMixin, ListView):
    model = AuditTrail
    paginate_by = 100
    template_name = 'dashboard/audittrails/list.html'
    
    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.order_by('-created_at')
