import re
from django.db import models
from django.core.validators import MinValueValidator
from django.conf import settings
from uuid import uuid4
from django.contrib.auth.models import AbstractUser
from store.validator import validate_file_size


class User(AbstractUser):
    email = models.EmailField(unique=True)


class Promotion(models.Model):
    description = models.CharField(max_length=255)
    discount = models.FloatField()


class Address(models.Model):
    street = models.CharField(max_length=255)
    house_info = models.CharField(max_length=255)
    city = models.IntegerField()
    state = models.IntegerField()
    lat = models.IntegerField()
    len = models.IntegerField()


class Collection(models.Model):
    title = models.CharField(max_length=255)
    featured_product = models.ForeignKey(
        'Product', on_delete=models.SET_NULL, null=True, related_name='+')

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['title']


class Store(models.Model):
    STORE_DELIVERED = 1
    EXPRESS_DELIVERED = 2
    DELIVERED_CHOICES = [
        (STORE_DELIVERED, 'S'),
        (EXPRESS_DELIVERED, 'E')
    ]
    title = models.CharField(max_length=255)
    logo = models.ImageField(null=True, upload_to='store/images', validators=[validate_file_size])
    collection = models.ForeignKey(Collection, on_delete=models.PROTECT)
    rate = models.FloatField(default=0)
    deliver_type = models.CharField(
        max_length=1, choices=DELIVERED_CHOICES, default=EXPRESS_DELIVERED)
    work_duration = models.CharField(max_length=255)
    limit_price = models.DecimalField(max_digits=9, decimal_places=2, validators=[MinValueValidator(10)])
    address = models.ForeignKey(Address, on_delete=models.PROTECT, related_name="store", null=True)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)


class Product(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField()
    description = models.TextField()
    unit_price = models.DecimalField(
        max_digits=9,
        decimal_places=2,
        validators=[MinValueValidator(10)]
    )
    inventory = models.IntegerField()
    last_update = models.DateTimeField(auto_now=True)
    collection = models.ForeignKey(Collection, on_delete=models.PROTECT)
    promotions = models.ManyToManyField(Promotion, blank=True)
    discount = models.IntegerField(null=True)
    store = models.ForeignKey(Store, on_delete=models.PROTECT, related_name="products", null=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['title']


class ProductImages(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to='store/images', validators=[validate_file_size])


class Customer(models.Model):
    MEMBERSHIP_BRONZE = 'B'
    MEMBERSHIP_SILVER = 'S'
    MEMBERSHIP_GOLD = 'G'

    MEMBERSHIP_CHOICES = [
        (MEMBERSHIP_BRONZE, 'Bronze'),
        (MEMBERSHIP_SILVER, 'Silver'),
        (MEMBERSHIP_GOLD, 'Gold'),
    ]
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    phone = models.CharField(max_length=255)
    birth_date = models.DateField(null=True)
    membership = models.CharField(
        max_length=1, choices=MEMBERSHIP_CHOICES, default=MEMBERSHIP_BRONZE)

    def __str__(self):
        return self.user.last_name

    def first_name(self):
        return self.user.first_name

    def last_name(self):
        return self.user.last_name

    class Meta:
        ordering = ['user__last_name']
        permissions = [
            ('view_history', 'can view history'),
        ]


class Order(models.Model):
    PAYMENT_STATUS_PENDING = 'P'
    PAYMENT_STATUS_COMPLETE = 'C'
    PAYMENT_STATUS_FAILED = 'F'
    PAYMENT_STATUS_CHOICES = [
        (PAYMENT_STATUS_PENDING, 'Pending'),
        (PAYMENT_STATUS_COMPLETE, 'Complete'),
        (PAYMENT_STATUS_FAILED, 'Failed')
    ]

    placed_at = models.DateTimeField(auto_now_add=True)
    payment_status = models.CharField(
        max_length=1, choices=PAYMENT_STATUS_CHOICES, default=PAYMENT_STATUS_PENDING)
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT)

    def __str__(self):
        return self.placed_at

    class Meta:
        ordering = ['placed_at']
        permissions = [
            ('cancel_order', 'can cancel order')
        ]


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.PROTECT, related_name="item")
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.PositiveSmallIntegerField()
    unit_price = models.DecimalField(max_digits=6, decimal_places=2)


class Cart(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4)
    created_at = models.DateTimeField(auto_now_add=True)


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField()

    class Meta:
        unique_together = [['cart', 'product']]


class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="review")
    name = models.CharField(max_length=255)
    description = models.TextField()
    date = models.DateField(auto_now_add=True)
