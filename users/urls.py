from django.urls import path,include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet
from .views import verify_email
from rest_framework_simplejwt.views import (
    TokenObtainPairView
)


router = DefaultRouter()
router.register(r'users',UserViewSet)

urlpatterns = [
    path('',include(router.urls)),
    path('verify-email/<uidb64>/<token>/',verify_email, name='verify-email'),
    path('token/',TokenObtainPairView.as_view(),name='token_obtain_pair')
]