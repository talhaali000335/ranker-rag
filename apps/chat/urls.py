from django.urls import path          # tool for building web addresses
from . import views                   # the views we just wrote

urlpatterns = [                       # this app's address book
    path("", views.chat_page, name="chat-page"),            # the home page "/" shows the chat page
    path("api/chat/", views.chat_api, name="chat-api"),     # "/api/chat/" receives questions
]