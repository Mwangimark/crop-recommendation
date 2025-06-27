from rest_framework import viewsets
from .models import Crop
from .serializers import CropSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated,AllowAny
from users.permission import IsAdmin

class CropViewSet(viewsets.ModelViewSet):
    queryset = Crop.objects.all()
    serializer_class = CropSerializer

    def destroy(self, request, *args, **kwargs):
        crop = self.get_object()
        crop.delete()
        return Response({'message':'crops successfully delete'},status = status.HTTP_200_OK)
    
    def get_permissions(self):
          if self.action in ['create']:
                return [AllowAny()]
          elif self.action == 'list':
                return [IsAuthenticated(),IsAdmin()]
          elif self.action in ['retrieve','update','partial_update','destroy','change_password']:
                return[IsAuthenticated()]
          return [IsAuthenticated( )]