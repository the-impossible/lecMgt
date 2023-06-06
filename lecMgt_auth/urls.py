from django.urls import path
from lecMgt_auth.views import *

app_name = 'auth'

urlpatterns = [
    path('dashboard', DashboardView.as_view(), name="dashboard"),
    path('login', LoginView.as_view(), name="login"),
    path('logout', LogoutView.as_view(), name="logout"),

    path('create_account', CreateAccountPageView.as_view(), name="create_account"),
    path('manage_accounts', ManageAccounts.as_view(), name="manage_accounts"),
    path('delete_account/<str:pk>', DeleteAccountView.as_view(), name="delete_account"),
    path('edit_account/<str:pk>', EditAccountView.as_view(), name="edit_account"),

    path('apply_leave', LeaveCreateView.as_view(), name="apply_leave"),
    path('manage_leaves', ManageLeaves.as_view(), name="manage_leaves"),
    path('delete_leave/<str:pk>', DeleteLeaveView.as_view(), name="delete_leave"),
    path('edit_leave/<str:pk>', EditLeaveView.as_view(), name="edit_leave"),

    path('approve_leave/<str:leave_id>/<str:type>', ApproveDisapproveLeaveView.as_view(), name="approve_leave"),

    path('create_notice', NoticeCreateView.as_view(), name="create_notice"),
    path('manage_notice', ManageNotice.as_view(), name="manage_notice"),
    path('edit_notice/<str:pk>', EditNoticeView.as_view(), name="edit_notice"),
]
