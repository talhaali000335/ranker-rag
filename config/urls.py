from django.contrib import admin            # the admin site
from django.urls import path, include       # include = hand a group of addresses to another file
from .health import health                  # our health page

urlpatterns = [                             # the main address book
    path("admin/", admin.site.urls),        # /admin/
    path("health/", health),                # /health/
    path("", include("apps.chat.urls")),    # everything else goes to the chat app's address book
]