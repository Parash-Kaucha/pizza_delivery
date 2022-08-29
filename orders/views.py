from telnetlib import STATUS
from django.shortcuts import render, get_object_or_404
from rest_framework import generics
from rest_framework.response import Response
from orders.models import Order, User
from . import serializers
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated, IsAdminUser
from rest_framework import status
from django.contrib.auth import get_user_model
from drf_yasg.utils import swagger_auto_schema

User = get_user_model()

# Create your views here.
class HelloOrderView(generics.GenericAPIView):
    @swagger_auto_schema(operation_summary="Hello Orders")
    def get(self, request):
        return Response(data={"message":"Hello Orders"})

class OrderCreateListView(generics.GenericAPIView):
    serializer_class = serializers.OrderCreationSerializer
    queryset = Order.objects.all()
    permission_classes = [IsAuthenticated]
    @swagger_auto_schema(operation_summary="View orders")
    def get(self, request):

        orders = Order.objects.all()

        serializer = self.serializer_class(instance=orders, many=True)

        return Response(data=serializer.data)
    @swagger_auto_schema(operation_summary="Create an order")
    def post(self, request):
        
        data = request.data

        serializer = self.serializer_class(data=data)

        user = request.user



        if serializer.is_valid():
            serializer.save(customer=user)

            return Response(data=serializer.data)

        return Response(data=serializer.errors)

class OrderDetailView(generics.GenericAPIView):
    serializer_class = serializers.OrderDetailSerializer
    permission_classes = [IsAdminUser]
    @swagger_auto_schema(operation_summary="Get specific Order")
    def get(self, request, order_id):
        
        order = get_object_or_404(Order, pk=order_id)

        serializer = self.serializer_class(instance=order)

        return Response(data=serializer.data)

    @swagger_auto_schema(operation_summary="Update an Order")
    def put(self, request, order_id):
        data = request.data

        order = get_object_or_404(Order, pk=order_id)

        serializer = self.serializer_class(data=data, instance=order)

        if serializer.is_valid():
            serializer.save()

            return Response(data=serializer.data)

        return Response(data=serializer.errors)

    @swagger_auto_schema(operation_summary="Delete an order")
    def delete(self, request, order_id):
        order = get_object_or_404(Order, pk=order_id)

        order.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)

class UpdateOrderStatus(generics.GenericAPIView):
    serializer_class = serializers.OrderStatusUpdateSerializer
    permission_classes = [IsAdminUser]
    
    @swagger_auto_schema(operation_summary="Update an specific order status")
    def put(self, request, order_id):
        
        order = get_object_or_404(Order, pk=order_id)

        data = request.data

        serializer = self.serializer_class(data=data, instance=order)

        if serializer.is_valid():
            serializer.save()

            return Response(data=serializer.data, status=status.HTTP_200_OK)

        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserOrdersView(generics.GenericAPIView):
    serializer_class = serializers.OrderDetailSerializer
    @swagger_auto_schema(operation_summary="Get orders of an specific user")
    def get(self, request, user_id):
        user = User.objects.get(pk=user_id)

        orders = Order.objects.all().filter(customer=user)

        serializer = self.serializer_class(instance=orders, many=True)

        return Response(data=serializer.data, status=status.HTTP_200_OK)

class UserOrderDetail(generics.GenericAPIView):
    serializer_class = serializers.OrderDetailSerializer


    @swagger_auto_schema(operation_summary="Get an specific order of a specified user")
    def get(self, request, user_id, order_id):
        user = User.objects.get(pk=user_id)

        order = Order.objects.all().filter(customer=user).get(pk=order_id)

        serializer = self.serializer_class(instance=order)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
