# users/views.py
from rest_framework.decorators import action
from rest_framework import viewsets
from .models import User
from .serializers import UserSerializer
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.hashers import check_password,make_password
from .utils import email_verification_token
from django.utils.http import urlsafe_base64_decode
from django.shortcuts import redirect
from django.http import HttpResponse
from rest_framework.decorators import api_view
from .serializers import ChangePasswordSerializer
from rest_framework.permissions import IsAuthenticated,AllowAny
from .permission import IsAdmin


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.filter(is_deleted=False)
    serializer_class = UserSerializer
    

    def destroy(self, request, *args, **kwargs):
        """
        Soft delete: override destroy method to set is_deleted=True
        """
        user = self.get_object()
        user.is_deleted = True
        user.save()
        return Response({'message':'User deleted successfuly'},status=status.HTTP_204_NO_CONTENT)
    
    @action(detail =True, methods = ['post'],url_path = 'change-password')
    def change_password(self, request, pk=None):
        user = self.get_object()
        serializer = ChangePasswordSerializer(data=request.data)

        if serializer.is_valid():
            old_password = serializer.validated_data['old_password']
            new_password = serializer.validated_data['new_password']

            if not user.check_password(old_password):
                return Response({'old_password': 'Wrong password'}, status=status.HTTP_400_BAD_REQUEST)

            user.set_password(new_password)
            user.save()
            return Response({'status': 'Password updated successfully'}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
        # confirming_authentication
    def get_permissions(self):
          if self.action in ['create']:
                return [AllowAny()]
          elif self.action == 'list':
                return [IsAuthenticated(),IsAdmin()]
          elif self.action in ['retrieve','update','partial_update','destroy','change_password']:
                return[IsAuthenticated()]
          return [IsAuthenticated( )]
    


@api_view(['GET'])
def verify_email(request,uidb64,token):
    try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = User.objects.get(pk=uid)
    except(TypeError,ValueError,OverflowError,User.DoesNotExist):
            return HttpResponse('Invalid link',status=400)
        
    if email_verification_token.check_token(user,token):
            user.is_verified = True
            user.save()
            return HttpResponse('Email successfully verified!',status= 200)
        
    else:
            return HttpResponse('Invalid or expired token',status = 400)
       
