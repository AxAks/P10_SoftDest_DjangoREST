import jwt
from django.contrib.auth import user_logged_in
from django.contrib.auth.hashers import check_password
from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework_jwt.serializers import jwt_payload_handler

from SoftDesk import settings
from users.models import CustomUser
from users.serializers import UserSerializer, UserLoginSerializer


class CreateUserModelViewSet(ModelViewSet):
    """
    Endpoint to create a user
    """
    permission_classes = (AllowAny,)
    serializer_class = UserSerializer


class AuthenticationAPIView(APIView):
    """
    Endpoint to Signup and get authentication Token
    """
    permission_classes = (AllowAny,)
    serializer_class = UserLoginSerializer

    @staticmethod
    def post(request, *args, **kwargs):
        """
        Enables the user to send their infos to login
        """
        try:
            username = request.data['username']
            password = request.data['password']

            user = get_object_or_404(CustomUser.objects.filter(username=username))  # error non catché si pas de match !
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


class ListUsersModelViewSet(ModelViewSet):
    """
    Enables an authenticated user to list all other registered users
    """
    permission_classes = (IsAuthenticated,)
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
