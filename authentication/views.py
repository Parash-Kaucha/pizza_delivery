from telnetlib import STATUS
from django.shortcuts import render
from rest_framework import generics
from rest_framework.response import Response
from .models import User
from . import serializers
from drf_yasg.utils import swagger_auto_schema

# Create your views here.
class HelloAuthView(generics.GenericAPIView):
    @swagger_auto_schema(operation_summary="Hello User")
    def get(self, request):
        return Response(data={"message":"Hello Auth"})

class UserCreateView(generics.GenericAPIView):
    
    serializer_class = serializers.UserCreationSerializer
    @swagger_auto_schema(operation_summary="Create user account")
    def post(self, request):
        data = request.data

        serializer = self.serializer_class(data=data)

        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data)

        return Response(data=serializer.errors)