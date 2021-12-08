from django.urls import path
from users.views import CreateUserModelViewSet, AuthenticationAPIView, PersonalInfosModelViewSet

app_name = "users"

urlpatterns = [
    path('signup/', CreateUserModelViewSet.as_view({
        'post': 'create'
    })),
    path('login/', AuthenticationAPIView.as_view()),
    path('my_infos/', PersonalInfosModelViewSet.as_view(
        {
            'get': 'retrieve',
            'put': 'update',
        }
    ))
]
