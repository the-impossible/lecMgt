from django.shortcuts import render, redirect, reverse
from django.http import HttpResponseRedirect, Http404, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.urls import reverse_lazy
from lecMgt_auth.models import User
from lecMgt_auth.forms import *

# Create your views here.


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = "backend/dashboard.html"


class LoginView(View):
    def get(self, request):
        return render(request, 'backend/auth/login.html')

    def post(self, request):
        email = request.POST.get('email').strip()
        password = request.POST.get('password').strip()

        if email and password:
            user = authenticate(request, email=email, password=password)

            if user:
                if user.is_active:
                    login(request, user)
                    messages.success(request, f"You are now signed in {user}")

                    nxt = request.GET.get('next', None)
                    if nxt is None:
                        return redirect('auth:dashboard')
                    return redirect(self.request.GET.get('next', None))

                else:
                    messages.warning(
                        request, 'Account not active contact the administrator')
            else:
                messages.error(request, 'Invalid login credentials')
        else:
            messages.error(request, 'All fields are required!!')

        return redirect('auth:login')


class LogoutView(LoginRequiredMixin, View):

    def post(self, request):
        logout(request)
        messages.success(
            request, 'You are successfully logged out, to continue login again')
        return redirect('auth:login')


class CreateAccountPageView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = User
    form_class = AccountCreationForm
    template_name = "backend/auth/create_update_account.html"
    success_message = "Account created successfully!"

    def get_success_url(self):
        return reverse("auth:create_account")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["type"] = 'Create'
        return context

    def form_valid(self, form):
        user_type = form.cleaned_data.get('user_type')
        if user_type == "1":
            form.instance.is_central = True
        elif user_type == "2":
            form.instance.is_dean = True
        elif user_type == "3":
            form.instance.is_hod = True
        elif user_type == "4":
            form.instance.is_dept = True
        elif user_type == "5":
            form.instance.is_staff = True

        form = super().form_valid(form)

        return form


class ManageAccounts(LoginRequiredMixin, ListView):
    template_name = 'backend/auth/manage_accounts.html'

    def get_queryset(self):
        return User.objects.all().order_by('-date_joined')

    def get_success_url(self):
        return reverse("auth:manage_accounts")


class EditAccountView(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = User
    template_name = "backend/auth/create_update_account.html"
    form_class = EditAccountCreationForm
    success_message = 'Account Updated Successfully!'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["type"] = 'Update'
        return context

    def get_form_kwargs(self):
        kwargs = super(EditAccountView, self).get_form_kwargs()
        if hasattr(self, 'object'):
            kwargs.update({'types': self.object})
        return kwargs

    def get_success_url(self):
        return reverse("auth:manage_accounts")

    def form_valid(self, form):
        user_type = form.cleaned_data.get('user_type')

        form.instance.is_central = False
        form.instance.is_dean = False
        form.instance.is_hod = False
        form.instance.is_dept = False
        form.instance.is_is_staff = False

        if user_type == "1":
            form.instance.is_central = True
        elif user_type == "2":
            form.instance.is_dean = True
        elif user_type == "3":
            form.instance.is_hod = True
        elif user_type == "4":
            form.instance.is_dept = True
        elif user_type == "5":
            form.instance.is_staff = True

        form = super().form_valid(form)

        return form


class DeleteAccountView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = User
    success_message = 'Deleted successfully!'
    success_url = reverse_lazy('auth:manage_accounts')


class LeaveCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Leave
    form_class = LeaveApplicationForm
    template_name = "backend/auth/leave/create_update_leave.html"
    success_message = "Leave has been requested successfully!"

    def get_success_url(self):
        return reverse("auth:apply_leave")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["type"] = 'Apply'
        return context

    def form_valid(self, form):
        form.instance.user = self.request.user
        form = super().form_valid(form)

        return form

class ManageLeaves(LoginRequiredMixin, ListView):
    template_name = 'backend/auth/leave/manage_leave.html'

    def get_queryset(self):
        return Leave.objects.all().order_by('-created')

    def get_success_url(self):
        return reverse("auth:manage_leaves")

class DeleteLeaveView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Leave
    success_message = 'Deleted successfully!'
    success_url = reverse_lazy('auth:manage_leaves')

class EditLeaveView(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = Leave
    template_name = "backend/auth/leave/create_update_leave.html"
    form_class = LeaveApplicationForm
    success_message = 'Leave Updated Successfully!'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["type"] = 'Update'
        return context

    def get_success_url(self):
        return reverse("auth:manage_leaves")

class ApproveDisapproveLeaveView(LoginRequiredMixin, View):

    def post(self, request, leave_id, type):
        leave = Leave.objects.get(leave_id=leave_id)
        if type == 'approve':
            leave.dept_approval = True
            messages.success(
            request, 'Leave has been approved')
        else:
            leave.dept_approval = False
            messages.success(
            request, 'Leave has been disapproved')

        leave.save()
        return redirect('auth:manage_leaves')

