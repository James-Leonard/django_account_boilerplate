from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.forms.models import inlineformset_factory, formset_factory
from datetime import datetime


from hotelbar.models import *
from hotelbar.forms import *




@login_required
def purchase_order_list(request):
    purchase_orders = PurchaseOrder.objects.all()
    return render(request, 'inventory/purchase_order_list.html', {'purchase_orders': purchase_orders})


@login_required
def purchase_order_detail(request, pk):
    purchase_order = get_object_or_404(PurchaseOrder, pk=pk)
    return render(request, 'inventory/purchase_order_detail.html', {'purchase_order': purchase_order})

def purchase_order_create(request):
    PurchaseOrderLineFormSet = formset_factory(PurchaseOrderLineForm, extra=1)
    if request.method == 'POST':
        form = PurchaseOrderForm(request.POST)
        formset = PurchaseOrderLineFormSet(request.POST)

        if form.is_valid() and formset.is_valid():
            # Create the Purchase Order object
            purchase_order = form.save(commit=False)
            purchase_order.total_cost = 0
            purchase_order.save()

            # Create the Purchase Order Line objects
            for form in formset:
                if form.is_valid():
                    purchase_order_line = form.save(commit=False)
                    purchase_order_line.order = purchase_order
                    purchase_order_line.total_cost = purchase_order_line.quantity * purchase_order_line.price
                    purchase_order_line.save()

                    # Add the line item cost to the total cost of the purchase order
                    purchase_order.total_cost += purchase_order_line.total_cost

            # Save the updated total cost of the purchase order
            purchase_order.save()

            return redirect(reverse('purchase_order_detail', kwargs={'pk': purchase_order.pk}))
    else:
        form = PurchaseOrderForm()
        formset = PurchaseOrderLineFormSet()

    context = {
        'form': form,
        'formset': formset,
    }

    return render(request, 'inventory/purchase_order_create.html', context)



def purchase_order_update(request, pk):
    PurchaseOrderLineFormSet = inlineformset_factory(PurchaseOrder, PurchaseOrderLine, form=PurchaseOrderLineForm, extra=5, can_delete=True)

    purchase_order = get_object_or_404(PurchaseOrder, pk=pk)
    if request.method == 'POST':
        form = PurchaseOrderForm(request.POST, instance=purchase_order)
        formset = PurchaseOrderLineFormSet(request.POST, instance=purchase_order)
        if form.is_valid() and formset.is_valid():
            purchase_order = form.save(commit=False)
            purchase_order.total_cost = 0
            purchase_order.save()
            formset.save()
            purchase_order_lines = formset.save(commit=False)
            for line in purchase_order_lines:
                line.order = purchase_order
                line.total_cost = line.price * line.quantity
                line.save()
                purchase_order.total_cost += line.total_cost
            purchase_order.save()
            messages.success(request, 'Purchase order updated successfully.')
            return redirect('purchase_order_detail', pk=purchase_order.pk)
    else:
        form = PurchaseOrderForm(instance=purchase_order)
        formset = PurchaseOrderLineFormSet(instance=purchase_order)
    return render(request, 'inventory/purchase_order_update.html', {'form': form, 'formset': formset, 'purchase_order': purchase_order})

def purchase_order_delete(request, pk):
    purchase_order = get_object_or_404(PurchaseOrder, pk=pk)
    if request.method == 'POST':
        purchase_order.delete()
        messages.success(request, 'Purchase order deleted successfully.')
        return redirect('purchase_order_list')
    return render(request, 'inventory/purchase_order_delete.html', {'purchase_order': purchase_order})


#####################################



def inventory_list(request):
    items = InventoryItem.objects.all()
     # Get current page number from query parameter
    page = request.GET.get('page', 1)

    # Create a paginator object with 10 items per page
    paginator = Paginator(items, 10)
  # Get the requested page object
    try:
        page_obj = paginator.page(page)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)
    return render(request, 'inventory/inventory_list.html', {'items': page_obj, 'section': 'inventory_list', })

def inventory_detail(request, pk):
    item = get_object_or_404(InventoryItem, pk=pk)
    return render(request, 'inventory/inventory_detail.html', {'item': item})

def inventory_create(request):
    if request.method == 'POST':
        form = InventoryItemForm(request.POST)
        if form.is_valid():
            item = form.save()
            messages.success(request, 'Inventory item created successfully.')
            return redirect('inventory_detail', pk=item.pk)
    else:
        form = InventoryItemForm()

    categories = Category.objects.all()
    suppliers = Supplier.objects.all()
    context = {'form': form, 'categories': categories, 'suppliers': suppliers}
    return render(request, 'inventory/inventory_create.html', context)

def inventory_update(request, pk):
    item = get_object_or_404(InventoryItem, pk=pk)

    if request.method == 'POST':
         # Handle form submission
        form = InventoryItemForm(request.POST, instance=item)
        if form.is_valid():
            item = form.save()
            return redirect('inventory_detail', pk=item.pk)
    else:
        form = InventoryItemForm(instance=item)

    categories = Category.objects.all()
    suppliers = Supplier.objects.all()

    return render(request, 'inventory/inventory_update.html', {'form': form, 'categories': categories, 'suppliers': suppliers})


def inventory_delete(request, pk):
    item = get_object_or_404(InventoryItem, pk=pk)

    if request.method == 'POST':
        item.delete()
        return HttpResponseRedirect(reverse('inventory_list'))

    return render(request, 'inventory/inventory_confirm_delete.html', {'item': item})










































@login_required
def supplier_list(request):
    suppliers = Supplier.objects.all()
    context = {'suppliers': suppliers, 'section': 'supplier_list'}
    return render(request, 'inventory/supplier_list.html', context)

@login_required
def supplier_detail(request, pk):
    supplier = get_object_or_404(Supplier, pk=pk)
    context = {'supplier': supplier}
    return render(request, 'inventory/supplier_detail.html', context)

@login_required
def supplier_create(request):
    if request.method == 'POST':
        form = SupplierForm(request.POST)
        if form.is_valid():
            supplier = form.save(commit=False)
            supplier.save()
            return redirect('supplier_detail', pk=supplier.pk)
        else:
            print(form.errors)

    else:
        form = SupplierForm()
    
    context = {
        'form': form
    }
    return render(request, 'inventory/supplier_create.html', context)

@login_required
def supplier_edit(request, pk):
    supplier = get_object_or_404(Supplier, pk=pk)
    form = SupplierForm(request.POST or None, instance=supplier)
    if form.is_valid():
        form.save()
        messages.success(request, 'Supplier has been updated successfully!')
        return redirect('supplier_list')
    context = {'form': form, 'supplier': supplier}
    return render(request, 'inventory/supplier_edit.html', context)

@login_required
def supplier_delete(request, pk):
    supplier = get_object_or_404(Supplier, pk=pk)
    if request.method == 'POST':
        supplier.delete()
        messages.success(request, 'Supplier has been deleted successfully!')
        return redirect('supplier_list')
    context = {'supplier': supplier}
    return render(request, 'inventory/supplier_confirm_delete.html', context)
