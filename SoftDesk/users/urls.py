from django.urls import path
from users.views import CreateUserAPIView, AuthenticationAPIView, ListUsersAPIView

app_name = "users"

urlpatterns = [
    path('signup', CreateUserAPIView.as_view()),
    path('login', AuthenticationAPIView.as_view()),
    path('users', ListUsersAPIView.as_view({'get': 'list'}))  # test à retirer ensuite peut-etre
]
