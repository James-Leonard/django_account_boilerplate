from django.urls import path
from . import views

urlpatterns = [
    ########
    path('categories/', views.category_list, name='category_list'),
    path('categories/create/', views.category_create, name='category_create'),
    path('categories/add<int:pk>/', views.category_detail, name='category_detail'),
    path('categories/edit<int:pk>/edit/', views.category_edit, name='category_edit'),
    path('categories/delete<int:pk>/delete/', views.category_delete, name='category_confirm_delete'),
    #######
]
