from django.urls import path
from users.views import CreateUserModelViewSet, AuthenticationAPIView, ListUsersModelViewSet

app_name = "users"

urlpatterns = [
    path('signup', CreateUserModelViewSet.as_view({
        'post': 'create'
    })),
    path('login', AuthenticationAPIView.as_view()),
    path('users', ListUsersModelViewSet.as_view({
        'get': 'list'
    }))  # test à retirer ensuite peut-etre
]
