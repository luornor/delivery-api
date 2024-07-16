from django.contrib import admin
from .models import Delivery
# Register your models here.

class DeliveryAdmin(admin.ModelAdmin):
    list_display = ('delivery_id','order_id','status', 'current_location','created_at','estimated_delivery_time')
    list_filter = ('status', 'delivery_provider', 'created_at', 'updated_at')
    search_fields = ('id','order_id','delivery_provider')
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'updated_at')

admin.site.register(Delivery,DeliveryAdmin)

