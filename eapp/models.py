from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=20)
    middle_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    address = models.CharField(max_length=30)
    join_on = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return (self.first_name)


class Category(models.Model):
    title = models.CharField(max_length=20)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.title


class Product(models.Model):
    name = models.CharField(max_length=100)
    desc = models.TextField()
    price = models.IntegerField()
    slug = models.SlugField(unique=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    warranty = models.CharField(max_length=100, null=True, blank=True)
    count_view = models.PositiveIntegerField(default=0)
    return_policy = models.CharField(max_length=200, null=True, blank=True)
    image = models.ImageField(upload_to='product' )

    def __str__(self):
        return (self.name)


class Cart(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    total = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return ('Cart: ' + str(self.id))

class CartProduct(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    rate = models.PositiveIntegerField()
    quantity = models.PositiveIntegerField()
    subtotal = models.PositiveIntegerField()

    def __str__(self):
       return ('Cart: ' + str(self.cart.id))

ORDER_STATUS = (
    ('Order Received', 'Order Received'),
    ('Order Processing', 'Order Processing'),
    ('On the way', 'On the way'),
    ('Order Complete', 'Order Complete'),
    ('Order Canceled', 'Order Canceled')
)


class Order(models.Model):
    cart = models.OneToOneField(Cart, on_delete=models.CASCADE)
    order_by = models.CharField(max_length=100)
    shipping_address = models.CharField(max_length=200)
    mobile = models.CharField(max_length=10)
    email = models.EmailField(null=True, blank=True)
    subtotal = models.PositiveIntegerField()
    discount = models.PositiveIntegerField()
    total = models.PositiveIntegerField()
    order_status = models.CharField(max_length=50, choices=ORDER_STATUS)
    created_at = models.DateTimeField(auto_now_add=True)

    # def __str__(self):
    #     return 'Order: ' + str(self.id)
