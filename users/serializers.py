from django.contrib.auth import authenticate

from django.contrib.auth.models import User
from rest_framework import serializers


class LoginSerializer(serializers.Serializer):
   """
   This serializer defines two fields for authentication:
     * username
     * password.
   It will try to authenticate the user with when validated.
   """
   username = serializers.CharField(
       label="Username",
       write_only=True
   )
   password = serializers.CharField(
       label="Password",
       # This will be used when the DRF browsable API is enabled
       style={'input_type': 'password'},
       trim_whitespace=False,
       write_only=True
   )


   def validate(self, attrs):
       # Take username and password from request
       username = attrs.get('username')
       password = attrs.get('password')


       if username and password:
           # Try to authenticate the user using Django auth framework.
           user = authenticate(request=self.context.get('request'),
                               username=username, password=password)
     
           if not user:
                    # If we don't have a regular user, raise a ValidationError
                msg = 'Access denied: wrong username or password. Please try again'
                raise serializers.ValidationError(msg, code='authorization')
       else:
           msg = 'Both "username" and "password" are required.'
           raise serializers.ValidationError(msg, code='authorization')
       # We have a valid user, put it in the serializer's validated_data.
       # It will be used in the view.
       attrs['user'] = user
       return attrs
   

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = [
            'username',
            'last_name',
            'first_name',
            
        ]

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    is_staff = serializers.BooleanField(default=False, write_only=True)
    is_superuser = serializers.BooleanField(default=False, write_only=True)

    class Meta:
        model = User
        fields = ('username','last_name', 'password','is_staff', 'is_superuser')

    def create(self, validated_data):
        user = User.objects.create_user(
            validated_data['username'],
            validated_data['last_name'],
            validated_data['password'],
            is_staff=validated_data.get('is_staff', False),
            is_superuser=validated_data.get('is_superuser', False)
        )
        return user