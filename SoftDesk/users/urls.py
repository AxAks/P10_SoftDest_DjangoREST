from django.urls import path
from users.views import CreateUserAPIView, AuthenticationAPIView

app_name = "users"

urlpatterns = [
    path('signup/', CreateUserAPIView.as_view()),
    path('login/', AuthenticationAPIView.as_view())
]
