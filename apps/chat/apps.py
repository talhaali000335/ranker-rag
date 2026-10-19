from django.apps import AppConfig                          # Django's base class that describes an app


class ChatConfig(AppConfig):                               # settings for the chat app
    default_auto_field = "django.db.models.BigAutoField"   # new rows get big whole-number ids
    name = "apps.chat"                                     # the full import path: folder apps, then chat