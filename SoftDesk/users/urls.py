from django.urls import path
from users.views import CreateUserAPIView, login_view

app_name = "users"

urlpatterns = [
    path('signup', CreateUserAPIView.as_view()),
    path('login', login_view, name="login")
]
