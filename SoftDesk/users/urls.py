from django.urls import path
from users.views import CreateUserModelViewSet, AuthenticationAPIView

app_name = "users"

urlpatterns = [
    path('signup/', CreateUserModelViewSet.as_view({
        'post': 'create'
    })),
    path('login/', AuthenticationAPIView.as_view())
]
