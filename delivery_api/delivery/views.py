from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.urls import reverse_lazy
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from .models import Delivery
from .serializers import DeliverySerializer

# Create your views here.

class RootAPIView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_summary="Root API Endpoint",
        operation_description="Provides links to all available endpoints in the Delivery API.",
        responses={200: openapi.Response('Successful operation', schema=openapi.Schema(type=openapi.TYPE_OBJECT))},
        tags=['General']
    )
    def get(self, request, *args, **kwargs):
        api_urls = {
            "Create Delivery": request.build_absolute_uri(reverse_lazy('create-delivery')),
            "Delivery Detail": request.build_absolute_uri(reverse_lazy('delivery-detail', args=[1])),
            "Order Deliveries": request.build_absolute_uri(reverse_lazy('order-deliveries', args=[1])),
        }
        return Response(api_urls, status=status.HTTP_200_OK)


class DeliveryCreateView(generics.CreateAPIView):
    queryset = Delivery.objects.all()
    serializer_class = DeliverySerializer
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="Create Delivery",
        operation_description="Endpoint to create a new delivery record.",
        request_body=DeliverySerializer,
        responses={
            201: openapi.Response('Created', schema=DeliverySerializer),
            400: 'Bad Request - Invalid data',
            500: 'Internal Server Error'
        },
        tags=['Delivery']
    )
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        delivery = Delivery.objects.get(id=serializer.instance.id)
        
        return Response(
            {
                "message": "Delivery record created successfully",
                "delivery": {
                    'delivery_id': delivery.delivery_id,
                    "order id": delivery.order_id,
                    "delivery provider": delivery.delivery_provider,
                    "status": delivery.status,
                    "current location": delivery.current_location,
                    'estimated_delivery_time': delivery.estimated_delivery_time,
                    "delivery method": delivery.delivery_method,
                    'created date': delivery.created_at
                }
            },
            status=status.HTTP_201_CREATED
        )


class DeliveryDetailView(generics.RetrieveUpdateAPIView):
    queryset = Delivery.objects.all()
    serializer_class = DeliverySerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'delivery_id'

    @swagger_auto_schema(
        operation_summary="Retrieve Delivery",
        operation_description="Retrieve detailed information of a specific delivery by its delivery ID.",
        responses={
            200: openapi.Response('Successful operation', schema=DeliverySerializer),
            404: "Delivery not found"
        },
        tags=['Delivery']
    )
    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        delivery = Delivery.objects.get(id=serializer.instance.id)

        return Response(
            {
                "message": "Delivery information retrieved successfully",
                "delivery": {
                    'delivery_id': delivery.delivery_id,
                    "order id": delivery.order_id,
                    "delivery provider": delivery.delivery_provider,
                    "status": delivery.status,
                    "current location": delivery.current_location,
                    'estimated_delivery_time': delivery.estimated_delivery_time,
                    "delivery method": delivery.delivery_method,
                    'created date': delivery.created_at
                }
            },
            status=status.HTTP_200_OK
        )

    @swagger_auto_schema(
        operation_summary="Update Delivery",
        operation_description="Update the details of an existing delivery.",
        request_body=DeliverySerializer,
        responses={
            200: openapi.Response('Successful operation', schema=DeliverySerializer),
            400: "Invalid input",
            404: "Delivery not found"
        },
        tags=['Delivery']
    )
    def put(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        data = {
            'order_id': instance.order_id, 
            'delivery_provider': instance.delivery_provider, 
            'status': request.data.get('status')
        }
        serializer = self.get_serializer(instance, data=data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        delivery = Delivery.objects.get(id=serializer.instance.id)

        return Response(
            {
                "message": "Delivery status updated successfully",
                "delivery": {
                    'delivery_id': delivery.delivery_id,
                    "order id": delivery.order_id,
                    "delivery provider": delivery.delivery_provider,
                    'tracking number': delivery.tracking_number,
                    "status": delivery.status,
                    "current location": delivery.current_location,
                    'estimated_delivery_time': delivery.estimated_delivery_time,
                    "delivery method": delivery.delivery_method,
                    'created date': delivery.created_at
                }
            },
            status=status.HTTP_200_OK
        )

    @swagger_auto_schema(
        operation_summary="Partial Update Delivery",
        operation_description="Partially update the details of an existing delivery.",
        request_body=DeliverySerializer,
        responses={
            200: openapi.Response('Successful operation', schema=DeliverySerializer),
            400: "Invalid input",
            404: "Delivery not found"
        },
        tags=['Delivery']
    )
    def patch(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        delivery = Delivery.objects.get(id=serializer.instance.id)

        return Response(
            {
                "message": "Delivery status partially updated successfully",
                "delivery": {
                    'delivery_id': delivery.delivery_id,
                    "order id": delivery.order_id,
                    "delivery provider": delivery.delivery_provider,
                    'tracking number': delivery.tracking_number,
                    "status": delivery.status,
                    "current location": delivery.current_location,
                    'estimated_delivery_time': delivery.estimated_delivery_time,
                    "delivery method": delivery.delivery_method,
                    'created date': delivery.created_at
                }
            },
            status=status.HTTP_200_OK
        )


class OrderDeliveriesListView(generics.ListAPIView):
    serializer_class = DeliverySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        order_id = self.kwargs['orderId']
        return Delivery.objects.filter(order_id=order_id)

    @swagger_auto_schema(
        operation_summary="List Deliveries for Order",
        operation_description="Retrieve a list of deliveries associated with a specific order ID.",
        responses={
            200: openapi.Response('Successful operation', schema=DeliverySerializer(many=True)),
            404: "Order not found"
        },
        tags=['Delivery']
    )
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(
            {
                "message": "Delivery information for order retrieved successfully",
                "deliveries": serializer.data
            },
            status=status.HTTP_200_OK
        )
