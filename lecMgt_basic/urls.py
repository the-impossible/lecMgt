from django.urls import path

from lecMgt_basic.views import *

app_name = "basic"

urlpatterns = [
    path("", HomePage.as_view(), name="home"),
]
