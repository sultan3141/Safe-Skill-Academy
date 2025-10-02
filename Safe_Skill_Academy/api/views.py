from django.shortcuts import render
from api import serializer as api_serializer
from rest_framework_simplejwt.views import TokenObtainPairView
from userauths.models import User, Profile
from rest_framework import generics, response
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = api_serializer.MyTokenObtainPairSerializer

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = api_serializer.RegisterSerializer
    permission_classes = [AllowAny]  

def generate_random_otp(length=6):
    otp = ''.join([str(random.randint(0, 9)) for _ in range(length)])
    return otp

class PasswordRestEmailVerifyView(generics.GenericAPIView):
     permission_classes = [AllowAny]
     serializer_class = api_serializer.UserSerializer
     def get_object(self):
         email=self.kwargs['email']

         user=User.objects.filter(email=email).first()
         if user:

            uuid64=user.pk
            refresh=RefreshToken.for_user(user)
            refresh_token=str(refresh.access_token)

            user.refresh_token=refresh_token
            user.otp=generate_random_otp()
            user.save()

            link=f"http://localhost:5173/create-new-password/?otp={user.otp}&uuidb64={uuid64}=refresh_token{refresh_token}"
            print("link======",link)
         return user   
class PasswordChangeView(generics.GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = api_serializer.UserSerializer

    def create(self, request, *args, **kwargs):
        uuidb64=request.data['uuidb64']
        otp=request.data['otp']
        password=request.data['password']
        
        user=User.objects.get(id=uuidb64,otp=otp)
        if user:
           user.set_password(password)
           user.otp=''
           user.save()

           return Response({"message": "Password changed successfully"}, status=status.HTTP_201_CREATED)
        else:
           return Response({"message": "User Does Not Exists"}, status=status.HTTP_400_BAD_REQUEST)
