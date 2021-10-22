from django.urls import path

from .views import SignupView, LoginView

urlpatterns = [
    path('signup/', SignupView(), name='signup'),
    path('login/', LoginView(), name='login'),
]
