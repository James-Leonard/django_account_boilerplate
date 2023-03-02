from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import *
from .forms import *

# CATEGORY   #########################
@login_required
def category_list(request):
    categories = Category.objects.all()
    return render(request, 'hotelbar/category_list.html', {'categories': categories, 'section': 'category_list'})


@login_required
def category_detail(request, pk):
    category = get_object_or_404(Category, pk=pk)
    return render(request, 'hotelbar/category_detail.html', {'category': category})

@login_required
def category_create(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('category_list')
    else:
        form = CategoryForm()
    return render(request, 'hotelbar/category_create.html', {'form': form})

@login_required
def category_edit(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return redirect('category_list')
    else:
        form = CategoryForm(instance=category)
    return render(request, 'hotelbar/category_edit.html', {'form': form})

@login_required
def category_delete(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        category.delete()
        return redirect('category_list')
    return render(request, 'hotelbar/category_confirm_delete.html', {'category': category})

#### END CATEGORY ###################







# @login_required
# def sales_record_list(request):
#     sales_records = SalesRecord.objects.all()
#     return render(request, 'sales_record_list.html', {'sales_records': sales_records})

# @login_required
# def sales_record_detail(request, pk):
#     sales_record = get_object_or_404(SalesRecord, pk=pk)
#     return render(request, 'sales_record_detail.html', {'sales_record': sales_record})

# @login_required
# def sales_record_create(request):
#     if request.method == 'POST':
#         form = SalesRecordForm(request.POST)
#         if form.is_valid():
#             sales_record = form.save(commit=False)
#             sales_record.sold_by = request.user
#             sales_record.save()
#             messages.success(request, 'Sales record created successfully!')
#             return redirect('sales_record_detail', pk=sales_record.pk)
#     else:
#         form = SalesRecordForm()
#     return render(request, 'sales_record_form.html', {'form': form})

# @login_required
# def sales_record_update(request, pk):
#     sales_record = get_object_or_404(SalesRecord, pk=pk)
#     if request.method == 'POST':
#         form = SalesRecordForm(request.POST, instance=sales_record)
#         if form.is_valid():
#             sales_record = form.save()
#             messages.success(request, 'Sales record updated successfully!')
#             return redirect('sales_record_detail', pk=sales_record.pk)
#     else:
#         form = SalesRecordForm(instance=sales_record)
#     return render(request, 'sales_record_form.html', {'form': form})

# @login_required
# def sales_record_delete(request, pk):
#     sales_record = get_object_or_404(SalesRecord, pk=pk)
#     sales_record.delete()
#     messages.success(request, 'Sales record deleted successfully!')
#     return redirect('sales_record_list')

