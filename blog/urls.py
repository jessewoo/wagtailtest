from django.urls import path
from . import views

# URL patterns for the blog app, URLConf module
urlpatterns = [
    path("hello/", views.say_hello),
]
