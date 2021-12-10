from django.conf.urls import url
from django.urls import path
from users.views import CreateUserModelViewSet, AuthenticationAPIView, PersonalInfosModelViewSet
from rest_framework_jwt.views import refresh_jwt_token

app_name = "users"

urlpatterns = [
    path('signup/', CreateUserModelViewSet.as_view({
        'post': 'create'
    })),
    path('login/', AuthenticationAPIView.as_view()),
    url('token_refresh/', refresh_jwt_token),
    path('my_infos/', PersonalInfosModelViewSet.as_view(
        {
            'get': 'retrieve',
            'put': 'update',
        }
    ))
]
