from .views import *
from django.urls import path

from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required


urlpatterns = [
    path("calendario/", CalendarioTemplateView.as_view(), name="calendario"),
]
