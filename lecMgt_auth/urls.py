from django.urls import path
from lecMgt_auth.views import *

app_name = 'auth'

urlpatterns = [
    path('dashboard', DashboardView.as_view(), name="dashboard"),
    path('login', LoginView.as_view(), name="login"),

    path('create_account', CreateAccountPageView.as_view(), name="create_account"),
    path('manage_accounts', ManageAccounts.as_view(), name="manage_accounts"),
]
