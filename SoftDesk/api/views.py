from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view

from .serializers import SignupSerializer


@api_view(['POST', ])
def signup_view(request):
    serializer = SignupSerializer(data=request.data)
    data = {}
    if serializer.is_valid():
        custom_user = serializer.save()
        data['response'] = "successfully registered a new user"
        data['username'] = custom_user.username
        data['first_name'] = custom_user.first_name
        data['last_name'] = custom_user.last_name
        data['email'] = custom_user.email
        data['password'] = custom_user.password
    else:
        data = serializer.errors
    return Response(data)
