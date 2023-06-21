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
        elif user_type == "6":
            LecturerProfile.objects.create(user_id=form.instance.user_id)

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


class NoticeCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Notice
    form_class = NoticeForm
    template_name = "backend/auth/notice/create_update_notice.html"
    success_message = "Notice posted successfully!"

    def get_success_url(self):
        return reverse("auth:create_notice")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["type"] = 'Create'
        return context

    def form_valid(self, form):
        form.instance.posted_by = self.request.user
        form = super().form_valid(form)

        return form


class ManageNotice(LoginRequiredMixin, ListView):
    template_name = 'backend/auth/notice/manage_notice.html'

    def get_queryset(self):
        return Notice.objects.all().order_by('-created')

    def get_success_url(self):
        return reverse("auth:manage_notice")


class EditNoticeView(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = Notice
    template_name = "backend/auth/notice/create_update_notice.html"
    form_class = NoticeForm
    success_message = 'Notice Updated Successfully!'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["type"] = 'Update'
        return context

    def get_success_url(self):
        return reverse("auth:manage_notice")


class ManageLecturerAccounts(LoginRequiredMixin, ListView):
    template_name = 'backend/auth/manage_accounts.html'

    def get_queryset(self):
        return User.objects.filter(department=self.request.user.department, is_dept=False).order_by('-date_joined')

    def get_success_url(self):
        return reverse("auth:manage_accounts")


class EditLecturerProfileView(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = LecturerProfile
    template_name = "backend/auth/update_lecturer_profile.html"
    form_class = UpdateLecturerProfileForm
    success_message = 'Profile updated Updated Successfully!'

    def get_object(self):
        user = User.objects.get(user_id=self.kwargs['pk'])
        profile = LecturerProfile.objects.get(user_id=user.user_id)

        return profile

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["type"] = 'Update'
        return context

    def get_success_url(self):
        return reverse("auth:manage_lecturers")


class ApplyPromotionView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Promotion
    form_class = PromotionForm
    template_name = "backend/auth/promotion/apply_promotion.html"
    success_message = "Promotion application successfully!"

    def get_success_url(self):
        return reverse("auth:manage_promotion")

    def form_valid(self, form):
        # Get lecturer details
        user = User.objects.get(email=self.request.user)
        profile = LecturerProfile.objects.get(user_id=user.user_id)

        if profile.position.position_grade > form.instance.position.position_grade:
            messages.error(
                self.request, "Current position is higher than applying position")
            form = super().form_invalid(form)
            return form

        else:

            # get applying position grade
            if profile.position.position_title == form.instance.position.position_title:

                messages.error(self.request, "Already at current position")
                form = super().form_invalid(form)

                return form

            elif profile.grade_point >= form.instance.position.position_grade:
                form.instance.lecturer = profile

                promotion = Promotion.objects.filter(
                    lecturer=profile, is_pending=True).exists()

                if promotion:
                    messages.error(
                        self.request, "Your have a pending promotion application")
                    form = super().form_invalid(form)

                    return form

                form = super().form_valid(form)
                return form

            else:
                messages.error(
                    self.request, "Your grade point is lesser than the position grade point")
                form = super().form_invalid(form)

                return form


class ManagePromotions(LoginRequiredMixin, ListView):
    template_name = 'backend/auth/promotion/manage_promotion.html'

    def get_queryset(self):
        if self.request.user.is_dept:
            return Promotion.objects.filter(dept_approval=False).order_by('-date_applied')

        if self.request.user.is_hod:
            return Promotion.objects.filter(hod_approval=False).order_by('-date_applied')

        if self.request.user.is_dean:
            return Promotion.objects.filter(dean_approval=False).order_by('-date_applied')

        if self.request.user.is_central:
            return Promotion.objects.filter(central_approval=False).order_by('-date_applied')

        if self.request.user.is_staff:
            return Promotion.objects.all().order_by('-date_applied')

        user = User.objects.get(email=self.request.user)
        profile = LecturerProfile.objects.get(user_id=user.user_id)
        return Promotion.objects.filter(lecturer=profile).order_by('-date_applied')

    def get_success_url(self):
        return reverse("auth:manage_promotion")


class DeletePromotionView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Promotion
    success_message = 'Deleted successfully!'
    success_url = reverse_lazy('auth:manage_promotion')


class ApprovePromotionView(LoginRequiredMixin, View):

    def get(self, request, pro_id):
        pro = Promotion.objects.get(pro_id=pro_id)
        if request.user.is_dept:
            pro.dept_approval = True
        elif request.user.is_hod:
            pro.hod_approval = True
        elif request.user.is_dean:
            pro.dean_approval = True
        elif request.user.is_central:
            pro.central_approval = True
            pro.is_pending = False
            # upgrade lecturer
            lec = LecturerProfile.objects.get(
                profile_id=pro.lecturer.profile_id)
            lec.position = pro.position
            lec.save()
        else:
            messages.error(
                request, 'You are not authorized')
            return redirect('auth:manage_promotion')

        messages.success(
            request, 'promotion has been approved')
        pro.save()

        return redirect('auth:manage_promotion')
