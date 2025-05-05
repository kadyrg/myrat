from django.contrib.auth import authenticate
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.tokens import RefreshToken

from .models import User
from .serializers import ProfileSerializer, LoginSerializer


class UserViewSet(viewsets.GenericViewSet):
    queryset = User.objects.all().order_by('date_joined')
    
    @action(methods=['post'], detail=False, url_path='login')
    def login(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        email = request.data.get('email')
        password = request.data.get('password')
        user = User.objects.filter(email=email).first()
        if serializer.is_valid():
            if email and not password:
                return Response({"detail": "Password must be set"}, status=status.HTTP_400_BAD_REQUEST)
            if password and not email:
                return Response({"detail": "Email must be set"}, status=status.HTTP_400_BAD_REQUEST)
            if email and password:
                    if not user:
                        return Response({'message': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
                    try:
                        user = authenticate(email=email, password=password)
                        access_token = RefreshToken.for_user(user).access_token
                        return Response({'access': str(access_token),
                                         'email': user.email,
                                         'username': f"{ user.first_name} {user.last_name}"},
                                        status=status.HTTP_200_OK)
                    except:
                        return Response({"detail": "Something went wrong"}, status=status.HTTP_400_BAD_REQUEST)
                    
    @action(methods=['get'], detail=False, url_path='me')
    def profile(self, request, *args, **kwargs):
        if request.method == 'GET':
            user = self.request.user
            serializer = self.get_serializer(user)
            return Response(serializer.data)


    def get_permissions(self):
        if self.action == "profile":
            return [IsAuthenticated()]
        return [AllowAny()]
    def get_serializer_class(self, *args, **kwargs):
        if self.action == "profile":
            return ProfileSerializer
        if self.action == "login":
            return LoginSerializer
