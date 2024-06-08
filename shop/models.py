from django.db import models
from accounts.models import CustomUser
from django.utils import timezone
from decimal import Decimal

# Modèle pour les catégories de produits
class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name
    
# Modèle pour les produits
class Product(models.Model):
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    digital = models.BooleanField(default=False)
    image = models.ImageField(upload_to='products/', blank=True)
    date_added = models.DateTimeField(default=timezone.now)
    stock = models.PositiveIntegerField()
    available = models.BooleanField(default=True)

    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['-date_added']

    @property
    def image_url(self):
        if self.image and hasattr(self.image, 'url'):
            return self.image.url
        return ''
    
# Modèle panier
class Cart(models.Model):
    user = models.OneToOneField(CustomUser, related_name='cart', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    date_commande = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False, null=True, blank=True)
    transaction_id = models.CharField(max_length=200, null=True, blank=True)
    status = models.CharField(max_length=200, null=True, blank=True)
    total_trans = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return f"Cart of {self.user.username}"
    
    @property
    def get_cart_total(self):
        items = self.items.all()
        total = sum([item.get_total for item in items])
        return total

    @property
    def get_cart_items(self):
        items = self.items.all()  # Modifier cette ligne
        total = sum([item.quantity for item in items])
        return total


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='cart_items', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.quantity} of {self.product.name}"

    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total

class AddressShipping(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, blank=True, null=True)
    cart = models.ForeignKey(Cart, on_delete=models.SET_NULL, blank=True, null=True)
    address = models.CharField(max_length=100, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    zipcode = models.CharField(max_length=100, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.username}'s address"
