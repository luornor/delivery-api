from rest_framework import status,generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny,IsAuthenticated
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
        responses={200: openapi.Response('Successful operation', schema=openapi.Schema(type=openapi.TYPE_OBJECT))},
    )
    def get(self, request, *args, **kwargs):
        api_urls = {
            "Create Delivery": reverse_lazy('create-delivery'),
            "List Deliveries": reverse_lazy('list-deliveries'),
            "Update Delivery": reverse_lazy('update-delivery', args=[1]),
        }
        return Response(api_urls, status=status.HTTP_200_OK)


class DeliveryCreateView(generics.CreateAPIView):
    queryset = Delivery.objects.all()
    serializer_class = DeliverySerializer
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="Create Delivery",
        responses={201: openapi.Response('Created', schema=DeliverySerializer)},
    )

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

          # Fetch the created delivery instance
        delivery = Delivery.objects.get(id=serializer.instance.id)
        

        return Response(
            {
                "message": "Delivery record created successfully",
                "delivery": {
                    'delivery_id':delivery.delivery_id,
                    "order id": delivery.order_id,
                    "delivery provider": delivery.delivery_provider,
                    "status":delivery.status,
                    "current location": delivery.current_location,
                    'estimated_delivery_time':delivery.estimated_delivery_time,
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
        responses={200: openapi.Response('Successful operation', schema=DeliverySerializer)},
    )

    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        delivery = Delivery.objects.get(id=serializer.instance.id)

        return Response(
            {
                "message": "Delivery information retrieved successfully",
                "delivery": {
                    'delivery_id':delivery.delivery_id,
                    "order id": delivery.order_id,
                    "delivery provider": delivery.delivery_provider,
                    "status":delivery.status,
                    "current location": delivery.current_location,
                    'estimated_delivery_time':delivery.estimated_delivery_time,
                    "delivery method": delivery.delivery_method,
                    'created date': delivery.created_at
                }
            },
            status=status.HTTP_200_OK
        )
    
    @swagger_auto_schema(
        operation_summary="Update Delivery",
        responses={200: openapi.Response('Successful operation', schema=DeliverySerializer)},
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
                    'delivery_id':delivery.delivery_id,
                    "order id": delivery.order_id,
                    "delivery provider": delivery.delivery_provider,
                    'tracking number':delivery.tracking_number,
                    "status":delivery.status,
                    "current location": delivery.current_location,
                    'estimated_delivery_time':delivery.estimated_delivery_time,
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
        responses={200: openapi.Response('Successful operation', schema=DeliverySerializer(many=True))},
    )
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        delivery = Delivery.objects.get(id=serializer.instance.id)
        return Response(
            {
                "message": "Delivery information for order retrieved successfully",
                "delivery": {
                    'delivery_id':delivery.delivery_id,
                    "order id": delivery.order_id,
                    "delivery provider": delivery.delivery_provider,
                    'tracking number':delivery.tracking_number,
                    "status":delivery.status,
                    "current location": delivery.current_location,
                    'estimated_delivery_time':delivery.estimated_delivery_time,
                    "delivery method": delivery.delivery_method,
                    'created date': delivery.created_at
                }
            },
            status=status.HTTP_200_OK
        )