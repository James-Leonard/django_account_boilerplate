from django import forms
from django.forms import BaseModelFormSet
from .models import Category, InventoryItem, Supplier, PurchaseOrder, PurchaseOrderLine, SalesRecord
from django.forms import inlineformset_factory


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ('name',)


class InventoryItemForm(forms.ModelForm):
    class Meta:
        model = InventoryItem
        fields = ('name', 'category', 'price', 'current_quantity', 'reorder_level', 'reorder_quantity', 'last_ordered_date')


class SupplierForm(forms.ModelForm):
    class Meta:
        model = Supplier
        fields = ['name', 'contact_name', 'phone', 'email']

 
    name = forms.CharField(label='Supplier Name', max_length=255, required=True)
    contact_name = forms.CharField(label='Contact Name', max_length=255, required=True)
    email = forms.EmailField(label='Contact Email', required=True)
    phone = forms.CharField(label='Contact Phone', max_length=20, required=False)


class PurchaseOrderForm(forms.ModelForm):
    class Meta:
        model = PurchaseOrder
        fields = ['supplier', 'total_cost']
        widgets = {
            'supplier': forms.Select(attrs={'class': 'form-control'}),
            'total_cost': forms.NumberInput(attrs={'class': 'form-control'}),
        }


class PurchaseOrderLineForm(forms.ModelForm):
    class Meta:
        model = PurchaseOrderLine
        fields = ['item', 'quantity', 'price', 'total_cost']
        widgets = {
            'item': forms.Select(attrs={'class': 'form-control'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'total_cost': forms.NumberInput(attrs={'class': 'form-control'}),
        }

PurchaseOrderLineFormSet = inlineformset_factory(
    PurchaseOrder, PurchaseOrderLine, form=PurchaseOrderLineForm, extra=1, can_delete=True
)


class SalesRecordForm(forms.ModelForm):
    class Meta:
        model = SalesRecord
        fields = ('item', 'quantity', 'price', 'sold_to')


class SalesRecordForm(forms.ModelForm):
    class Meta:
        model = SalesRecord
        fields = ['item', 'quantity', 'price','sold_to']
