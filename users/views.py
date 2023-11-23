import webbrowser
from django.contrib.auth import login, logout
from django.shortcuts import redirect
from rest_framework import permissions
from rest_framework import views, status
from rest_framework.response import Response
from rest_framework import serializers
from . import serializers
from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view, permission_classes
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt,csrf_protect
from django.contrib.auth import login
from django.contrib.messages import error, success
from django.views.decorators.csrf import ensure_csrf_cookie
from . import serializers
from users.serializers import LoginSerializer

import users

class LoginView(views.APIView):
  
   permission_classes = (permissions.AllowAny,)

    
   def post(self, request, format=None):
       serializer = LoginSerializer(data=self.request.data,context={ 'request': self.request })
    
       serializer.is_valid(raise_exception=True)
       user = serializer.validated_data['user']
       password = serializer.validated_data['password']
       print(user)
       print(password)
       login(request, user,password)
       return Response(None, status=status.HTTP_202_ACCEPTED)



class LogoutView(views.APIView):
    permission_classes = (permissions.AllowAny,)
    def get(self, request, format=None):
        logout(request)
        response = Response(None, status=status.HTTP_204_NO_CONTENT)
        response.set_cookie('sessionid',max_age=1,samesite='None')
        response.set_cookie('csrftoken',max_age=1,samesite='None')
        return response

class ProfileView(generics.RetrieveAPIView):
    serializer_class = serializers.LoginSerializer

    def get_object(self):
        return self.request.user
    





from rest_framework.views import APIView

from rest_framework.decorators import api_view
from rest_framework.response import Response
from users.serializers import serializers ,RegisterSerializer
from django.contrib.auth.models import User
import json

  
   

class RegisterView(views.APIView):
    def post(self, request):
        
        serializer = RegisterSerializer(data=request.data)
        print(serializer,'serrrrrrr')
        if serializer.is_valid():
            is_superuser=serializer.validated_data.get('is_superuser', False)
            print(is_superuser,'superrrrrrrr')
            user = User.objects.create_user(
                serializer.validated_data['username'],
                serializer.validated_data['last_name'],
                serializer.validated_data['password'],
                is_staff=serializer.validated_data.get('is_staff', False),
                is_superuser=serializer.validated_data.get('is_superuser', False)
              
                
            )
           

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)