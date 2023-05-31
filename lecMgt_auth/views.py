from django.shortcuts import render, redirect, reverse
from django.http import HttpResponseRedirect, Http404, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.urls import reverse_lazy

# Create your views here.
class DashboardView(TemplateView):
    template_name = "backend/dashboard.html"

class LoginView(TemplateView):
    template_name = "backend/login.html"

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
