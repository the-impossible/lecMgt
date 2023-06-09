from django.urls import path
from lecMgt_auth.views import *

app_name = 'auth'

urlpatterns = [
    path('dashboard', DashboardView.as_view(), name="dashboard"),
    path('login', LoginView.as_view(), name="login"),
    path('logout', LogoutView.as_view(), name="logout"),

    path('create_account', CreateAccountPageView.as_view(), name="create_account"),
    path('manage_accounts', ManageAccounts.as_view(), name="manage_accounts"),
    path('delete_account/<str:pk>',
         DeleteAccountView.as_view(), name="delete_account"),
    path('edit_account/<str:pk>', EditAccountView.as_view(), name="edit_account"),

    path('apply_leave', LeaveCreateView.as_view(), name="apply_leave"),
    path('manage_leaves', ManageLeaves.as_view(), name="manage_leaves"),
    path('delete_leave/<str:pk>', DeleteLeaveView.as_view(), name="delete_leave"),
    path('edit_leave/<str:pk>', EditLeaveView.as_view(), name="edit_leave"),

    path('approve_leave/<str:leave_id>/<str:type>',
         ApproveDisapproveLeaveView.as_view(), name="approve_leave"),

    path('create_notice', NoticeCreateView.as_view(), name="create_notice"),
    path('manage_notice', ManageNotice.as_view(), name="manage_notice"),
    path('delete_notice/<str:pk>', DeleteNoticeView.as_view(), name="delete_notice"),
    path('edit_notice/<str:pk>', EditNoticeView.as_view(), name="edit_notice"),

    path('manage_lecturers', ManageLecturerAccounts.as_view(),
         name="manage_lecturers"),
    path('edit_lecturer/<str:pk>',
         EditLecturerProfileView.as_view(), name="edit_lecturer"),

    path('apply_promotion', ApplyPromotionView.as_view(), name="apply_promotion"),
    path('manage_promotion', ManagePromotions.as_view(), name="manage_promotion"),
    path('delete_promotion/<str:pk>',
         DeletePromotionView.as_view(), name="delete_promotion"),
    path('approve_pro/<str:pro_id>',
         ApprovePromotionView.as_view(), name="approve_pro"),
    path('disapprove_pro/<str:pro_id>',
         DisapprovePromotionView.as_view(), name="disapprove_pro"),

    path('profile/<str:pk>', ProfileView.as_view(), name="profile"),
    path('password', ChangePassword.as_view(), name="password"),

]
