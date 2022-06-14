from django.urls import path

from .views import LoginView


urlpatterns = [
    path(r'', LoginView.as_view()),
]
