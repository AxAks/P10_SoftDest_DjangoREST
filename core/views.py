from rest_framework import generics


class SignupView(generics.CreateAPIView):
    pass


class LoginView(generics.ListAPIView):
    pass
