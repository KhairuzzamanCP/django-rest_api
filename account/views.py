from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from account.serializers import UserRegistrationSerializers,UserLoginSerializer,UserProfileSerialzer,UserChangePasswordSerializer,SendPasswordResetSerializer,UserPasswordResetSerializer
from django.contrib.auth import authenticate
from account.renderers import UserRenderer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated

# Generate tokens manually
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


class UserRegistrationView(APIView):
    renderer_classes = [UserRenderer]
    def post(self, request,format =None):
       serializer = UserRegistrationSerializers(data= request.data)
       if serializer.is_valid(raise_exception=True):
           user = serializer.save()
           token = get_tokens_for_user(user)
           return Response({'token':token, 'maessage':'Registration Sucessful'}, status= status.HTTP_201_CREATED)
       
    
       return Response(serializer.errors, status= status.HTTP_400_BAD_REQUEST)
    
 
    

class UserLoginView(APIView):
    renderer_classes = [UserRenderer]
    def post(self, request, format=None):
        serializer = UserLoginSerializer(data=request.data)
        
        if serializer.is_valid(raise_exception=True):
            email = serializer.validated_data.get('email')
            password = serializer.validated_data.get('password')
            
            user = authenticate(request, email=email, password=password)
            
            if user is not None:
                # Authentication successful
                token = get_tokens_for_user(user)
                return Response({'token':token, 'message': 'Login Successful'}, status=status.HTTP_200_OK)
            else:
                # Authentication failed
                return Response({'errors': {'non_field_errors': ['Email or Password not Valid']}}, status=status.HTTP_404_NOT_FOUND)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


class UserProfileView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]
    def get(self,request, format=None):
        serializer = UserProfileSerialzer(request.user)
        return Response(serializer.data , status= status.HTTP_200_OK)
    


class UserChangePasswordView(APIView):
     renderer_classes = [UserRenderer]
     permission_classes = [IsAuthenticated]
     def post(self,request, format=None):
        serializer = UserChangePasswordSerializer(data=request.data, context = {'user':request.user})
        if serializer.is_valid(raise_exception=True):
            return Response({'message': 'Password Change Successfully'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
     

class SendPasswordResetEmailView(APIView):
    renderer_classes =[UserRenderer]
    def post(self,request,format=None):
       serializer = SendPasswordResetSerializer(data= request.data)
       if serializer.is_valid(raise_exception=True):
           return Response({'messages':'Password Reset Link Send.Please cheak your Email'}, status= status.HTTP_200_OK)
       return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserPasswordResetView(APIView):
    renderer_classes = [UserRenderer]
    def post(self,request,uid,token,format=None):
        serializer = UserPasswordResetSerializer(data= request.data,context=({'uid':uid, 'token':token}))
        if serializer.is_valid(raise_exception=True):
            return Response({'messages':'Password Reset Successfully'}, status= status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

             
         



