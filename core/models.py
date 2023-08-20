from django.contrib.auth.models import User
from django.db import models
import uuid

class Manufacturer(models.Model):
    name = models.CharField(max_length=100)
    address = models.TextField()
    contact_info = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Medicine(models.Model):
    manufacturer = models.ForeignKey(Manufacturer, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    production_date = models.DateField()
    expiration_date = models.DateField()
    is_expired=models.BooleanField(default=False)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity_in_stock = models.PositiveIntegerField()
    dosage = models.CharField(max_length=50, blank=True)
    active_ingredients = models.TextField(blank=True)
    storage_instructions = models.TextField(blank=True)
    usage_instructions = models.TextField(blank=True)
    precautions = models.TextField(blank=True)
    side_effects = models.TextField(blank=True)
    image = models.ImageField(upload_to='medicine_images/', blank=True, null=True)
    is_prescription_required = models.BooleanField(default=False)
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Order(models.Model):
    delivery_status = (
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
        ('active', 'Active')
    )
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    items = models.ManyToManyField(Medicine)
    order_date = models.DateField(auto_now_add=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=delivery_status)
    isPaid = models.BooleanField(default=False)
    invoice_serial = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return self.customer.email

    def save(self, *args, **kwargs):
        self.invoice_serial = uuid.uuid4()
        super(Order, self).save(*args, **kwargs)

# class OrderItem(models.Model):
#     order = models.ForeignKey(Order, on_delete=models.CASCADE)
#     medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE)
#     quantity = models.PositiveIntegerField()
#     subtotal = models.DecimalField(max_digits=10, decimal_places=2)


