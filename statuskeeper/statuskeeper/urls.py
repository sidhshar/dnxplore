from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("status/", include("statusmaster.urls")),
    path("admin/", admin.site.urls),
]