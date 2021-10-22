from rest_framework.generics import CreateAPIView, ListAPIView


class SignupView(CreateAPIView):
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class LoginView(ListAPIView):
    def post(self, request, *args, **kwargs):
        print('hello')
        return self.list(request, *args, **kwargs)

