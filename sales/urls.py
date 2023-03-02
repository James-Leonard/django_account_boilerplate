from django.urls import path
from . import views

urlpatterns = [
    path('', views.sales_list, name='sales_list'),
    path('sales/add/', views.sales_add, name='sales_add'),
    path('sales/<int:pk>/', views.sales_detail, name='sales_detail'),
    path('sales/<int:pk>/edit/', views.sales_edit, name='sales_edit'),
    path('sales/<int:pk>/delete/', views.sales_delete, name='sales_delete'),
    path('sales_summary_report/', views.sales_report, name='sales_summary_report'),
    # path('sales-report/', views.sales_report, name='sales_report'),
    #path('sales-report/export/', views.export_sales_report, name='export_sales_report'),
]
