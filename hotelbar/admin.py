from django.contrib import admin
from .models import *

admin.site.register(Supplier)
admin.site.register(Category)
admin.site.register(InventoryItem)
admin.site.register(PurchaseOrder)
admin.site.register(PurchaseOrderLine)
admin.site.register(SalesRecord)