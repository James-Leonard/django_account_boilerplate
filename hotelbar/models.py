from django.db import models


class Supplier(models.Model):
    name = models.CharField(max_length=100)
    contact_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    email = models.EmailField(max_length=254)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class InventoryItem(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    current_quantity = models.PositiveIntegerField()
    reorder_level = models.PositiveIntegerField()
    reorder_quantity = models.PositiveIntegerField()
    last_ordered_date = models.DateField(null=True, blank=True)
    suppliers = models.ManyToManyField(Supplier, related_name='inventory_items')

    def __str__(self):
        return self.name


class PurchaseOrder(models.Model):
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    ordered_date = models.DateField(auto_now_add=True)
    received_date = models.DateField(null=True, blank=True)
    total_cost = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.supplier.name} ({self.ordered_date})"


class PurchaseOrderLine(models.Model):
    item = models.ForeignKey(InventoryItem, on_delete=models.CASCADE)
    order = models.ForeignKey(PurchaseOrder, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    total_cost = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.item.name} ({self.quantity} x {self.price})"


class SalesRecord(models.Model):
    item = models.ForeignKey(InventoryItem, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    sold_to = models.CharField(max_length=100)
    sale_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.item.name} ({self.quantity} x {self.price}) sold to {self.sold_to}"
