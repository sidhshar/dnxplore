from django.contrib import admin
from django.urls import include, path

from statusmaster.api import api

urlpatterns = [
    path("status/", include("statusmaster.urls")),
    path("admin/", admin.site.urls),
    path("api/", api.urls),
]