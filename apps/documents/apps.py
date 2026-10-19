from django.apps import AppConfig                          # Django's base class that describes an app


class DocumentsConfig(AppConfig):                          # settings for the documents app
    default_auto_field = "django.db.models.BigAutoField"   # new rows get big whole-number ids
    name = "apps.documents"                                # the full import path: folder apps, then documents