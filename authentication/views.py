from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password, check_password
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from .models import User
import json

# Create your views here.

@api_view(['POST'])
def register(request):
    deserialize = json.loads(request.body)
    hash_password = make_password(deserialize['password'])
    user = User(email=deserialize['email'], password=hash_password)
    if not (User.objects.filter(email=deserialize['email']).exists()):
        user.save()
        return JsonResponse({'message': 'User created successfully'}, status=status.HTTP_201_CREATED)
    else:
        return JsonResponse({'message': 'User already exists'}, status=status.HTTP_400_BAD_REQUEST)