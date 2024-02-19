from django.shortcuts import render
# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .models import User
from rest_framework.exceptions import AuthenticationFailed
from .serializers import UserSerializer
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken, TokenError


class RegisterView(APIView):
    def post(self, request):
        serializer = UserSerializer(data = request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

class LoginView(APIView):
     
#    permission_classes = (IsAuthenticated, )

   def get(self, request):
       content = {'message': 'Welcome to the JWT uthentication page using React Js and Django!'}
       return Response(content)
   
   def post(self,request):
     print(request.data)
     email = request.data["email"]
     password = request.data["password"]
     
     print("Received from React", email, password)
     
     try:
          user = User.objects.get(email = email)
     except User.DoesNotExist:
          raise AuthenticationFailed("Account does  not exist")

     if user is None:
          raise AuthenticationFailed("User does not exist")
     if not user.check_password(password):
          raise AuthenticationFailed("Incorrect Password")
     
     access_token = str(AccessToken.for_user(user))
     refresh_token = str(RefreshToken.for_user(user))
     return Response({
          "access_token" : access_token,
          "refresh_token" : refresh_token
     })
   
class LogoutView(APIView):
     permission_classes = (IsAuthenticated,)
     def post(self, request):
          
          try:
               refresh_token = request.data["refresh_token"]
               token = RefreshToken(refresh_token)
               token.blacklist()
               return Response(status=status.HTTP_205_RESET_CONTENT)
          except Exception as e:
               return Response(status=status.HTTP_400_BAD_REQUEST)