from django.contrib import admin          # the admin site
from django.urls import path              # builds web addresses
from .health import health                # our health page

urlpatterns = [                           # the address book
    path("admin/", admin.site.urls),      # /admin/ opens the admin screen
    path("health/", health),              # /health/ runs our health view
]