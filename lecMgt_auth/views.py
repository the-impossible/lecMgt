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
class DashboardView(LoginRequiredMixin,TemplateView):
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
    template_name = "backend/auth/create_account.html"
    success_message = "Account created successfully!"

    def get_success_url(self):
        return reverse("auth:create_account")


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

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context["form"] = ScheduleTestForm
    #     return context

class DeleteAccountView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = User
    success_message = 'Deleted successfully!'
    success_url = reverse_lazy('auth:manage_accounts')
