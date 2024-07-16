from django.urls import path
from .views import RootAPIView,DeliveryCreateView, DeliveryDetailView, OrderDeliveriesListView

urlpatterns = [
    path('', RootAPIView.as_view(), name='root-api'),
    path('deliveries/', DeliveryCreateView.as_view(), name='delivery-create'),
    path('deliveries/<str:delivery_id>/', DeliveryDetailView.as_view(), name='delivery-detail'),
    path('orders/<int:orderId>/deliveries/', OrderDeliveriesListView.as_view(), name='order-deliveries'),
]

