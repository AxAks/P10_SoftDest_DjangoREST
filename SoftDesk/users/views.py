import jwt
from django.contrib.auth import user_logged_in
from django.contrib.auth.hashers import check_password
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_jwt.serializers import jwt_payload_handler

from SoftDesk import settings
from users.models import CustomUser
from users.serializers import UserSerializer


class CreateUserAPIView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = UserSerializer

    def post(self, request):
        user = request.data
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class AuthenticationAPIView(APIView):  # peut etre à revoir car pas de serializer + pas sur: jwt au lieu de django_jwt
    permission_classes = (AllowAny,)
    serializer_class = UserSerializer  # pas utilisé ici

    def post(self, request):

        try:
            username = request.data['username']
            password = request.data['password']

            user = CustomUser.objects.get(username=username)
            if user and check_password(password, user.password):
                try:
                    payload = jwt_payload_handler(user)
                    token = jwt.encode(payload, settings.SECRET_KEY)
                    user_details = {'name': f"{user.first_name} {user.last_name}", 'token': token}
                    user_logged_in.send(sender=user.__class__,
                                        request=request, user=user)
                    return Response(user_details, status=status.HTTP_200_OK)

                except Exception as e:
                    raise e
            else:
                res = {
                    'error': 'can not authenticate with the given credentials or the account has been deactivated'}
                return Response(res, status=status.HTTP_403_FORBIDDEN)
        except KeyError:
            res = {'error': 'please provide valid username and password'}
            return Response(res)
