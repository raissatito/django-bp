from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password, check_password
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from rest_framework.permissions import IsAuthenticated
from .models import User
from .serializers import *
from .wrapper import validate_serializer
import json, datetime


# Use the wrapper and serializer class as its parameter to validate the request data
@api_view(["POST"])
@validate_serializer(RegisterSerializer)
def register(request, data):
    hash_password = make_password(data["password"])
    user = User(email=data["email"], password=hash_password)
    if not (User.objects.filter(email=data["email"]).exists()):
        user.save()
        return JsonResponse({"message": "User created successfully"}, status=status.HTTP_201_CREATED)
    else:
        return JsonResponse({"message": "User already exists"}, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(["POST"])
@validate_serializer(LoginSerializer)
def login(request, data):
    user = User.objects.get(email=data["email"])
    user = authenticate(request, email=data["email"], password=data["password"])
    if user is not None:
        refresh = RefreshToken.for_user(user)
        access = refresh.access_token
        return JsonResponse({"refreshToken": str(refresh), "accessToken": str(access)}, status=status.HTTP_200_OK)
    else:
        return JsonResponse({"message": "Invalid password"}, status=status.HTTP_401_UNAUTHORIZED)
    
@api_view(['POST'])
@validate_serializer(LogoutSerializer)
@permission_classes([IsAuthenticated])
def logout(request, data):
    try:
        refresh_token = data['token']
        RefreshToken(refresh_token).blacklist()
        return JsonResponse({'message': 'Logout successful'}, status=status.HTTP_200_OK)
    except TokenError as e:
        return JsonResponse({'message': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def tes_auth(request):
    user_email = request.user.email
    return JsonResponse({"message": f"Authenticated, Hi {user_email}"}, status=status.HTTP_200_OK)