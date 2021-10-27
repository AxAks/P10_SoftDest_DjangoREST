from rest_framework import serializers

from users.models import CustomUser


class SignupSerializer(serializers.ModelSerializer):

    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = CustomUser
        fields = ['username', 'first_name', 'last_name', 'email', 'password', 'password2']
        extra_kwargs = {'password': {'write_only': True}}

    def save(self):
        custom_user = CustomUser(
            username=self.validated_data['username'],
            first_name=self.validated_data['first_name'],
            last_name=self.validated_data['last_name'],
            email=self.validated_data['email'],
        )
        password = self.validated_data['password']
        password2 = self.validated_data['password2']

        if password != password2:
            raise serializers.ValidationError({'password': 'Passwords must match'})
        custom_user.set_password(password)
        custom_user.save()
        return custom_user
