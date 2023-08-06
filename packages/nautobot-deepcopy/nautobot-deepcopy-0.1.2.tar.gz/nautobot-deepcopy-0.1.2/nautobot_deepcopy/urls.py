from __future__ import unicode_literals

from django.urls import path

from . import views

app_name = "nautobot_deepcopy"
urlpatterns = [
    path(r"copy/<uuid:pk>/add/", views.CopyView.as_view(), name="copy"),
]
