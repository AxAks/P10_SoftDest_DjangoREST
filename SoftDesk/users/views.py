from django.contrib.auth import authenticate, login
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.views import APIView

from users.serializers import CreateUserSerializer, LoginSerializer


class CreateUserAPIView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        user = request.data
        serializer = CreateUserSerializer(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['POST', ])
def login_view(request):
    serializer = LoginSerializer(data=request.data)
    data = {}
    if serializer.is_valid():
        data['username'] = serializer['username'].value
        data['password'] = serializer['password'].value
        user = authenticate(request, username=data['username'], password=data['password'])
        data['response'] = f"successfully logged in as {user}"
        if not user:
            login(request, user)

        else:
            pass
    else:
        data = serializer.errors
    return Response(data)
