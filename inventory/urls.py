from django.urls import path
from .views import *

urlpatterns = [
    path('supplier/', supplier_list, name='supplier_list'),
    path('supplier/create/', supplier_create, name='supplier_create'),
    path('supplier/<int:pk>/', supplier_detail, name='supplier_detail'),
    path('supplier/<int:pk>/edit/', supplier_edit, name='supplier_edit'),
    path('supplier/<int:pk>/delete/', supplier_delete, name='supplier_delete'),




    path('', inventory_list, name='inventory_list'),
    path('inventory/<int:pk>/', inventory_detail, name='inventory_detail'),
    path('inventory/new/', inventory_create, name='inventory_create'),
    path('inventory/<int:pk>/inventory_update/', inventory_update, name='inventory_update'),
    path('inventory/<int:pk>/delete/', inventory_delete, name='inventory_delete'),


    path('purchase_order/', purchase_order_list, name='purchase_order_list'),
    path('purchase_order/<int:pk>/', purchase_order_detail, name='purchase_order_detail'),
    path('purchase_order/new/', purchase_order_create, name='purchase_order_create'),
    path('purchase_order/<int:pk>/edit/', purchase_order_update, name='purchase_order_update'),
    path('purchase_order/<int:pk>/delete/', purchase_order_delete, name='purchase_order_delete'),


    # path('sales_record/', sales_record_list, name='sales_record_list'),
    # path('sales_record/<int:pk>/', sales_record_detail, name='sales_record_detail'),
    # path('sales_record/new/', sales_record_create, name='sales_record_create'),
    # path('sales_record/<int:pk>/edit/', sales_record_update, name='sales_record_update'),
    # path('sales_record/<int:pk>/delete/', sales_record_delete, name='sales_record_delete'),

]
