from django.db import models
from django.contrib.auth.models import User

class Client(models.Model):
    name = models.CharField(max_length=255)
    company_name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    password = models.CharField(max_length=200)
    phone = models.BigIntegerField()
    address = models.CharField(max_length=255)

class Purchase(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    address = models.CharField(max_length=200, null=False)
    city = models.CharField(max_length=200, null=False)
    state = models.CharField(max_length=200, null=False)
    zipcode = models.CharField(max_length=200, null=False)
    country = models.CharField(max_length=200, null=False)
    image = models.FileField(null=True)
    product = models.CharField(max_length=200, null=False)
    price = models.FloatField()
    quantity = models.IntegerField(default=0, null=True, blank=True)
    items = models.IntegerField(default=0, null=True, blank=True)
    total = models.FloatField()
    date_added = models.DateTimeField(auto_now_add=True)

class Product_looking_for(models.Model):
    company_name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    company_type = models.CharField(max_length=200, null=False)
    product = models.CharField(max_length=200, null=False)
    licence_number = models.CharField(max_length=200, null=False)
    licence_document = models.FileField(upload_to='documents')
    address = models.CharField(max_length=200, null=False)
    city = models.CharField(max_length=200, null=False)
    state = models.CharField(max_length=200, null=False)
    pin = models.CharField(max_length=200, null=False)
    country = models.CharField(max_length=200, null=False)
    message = models.CharField(max_length=200, null=False)
    boolean=models.BooleanField(default=False)

class Specific_product(models.Model):
    email=models.EmailField(max_length=255)
    product = models.CharField(max_length=255)
    reason = models.CharField(max_length=255)
    quantity = models.PositiveIntegerField()
    duration = models.PositiveIntegerField()
    quality = models.CharField(max_length=255)
    boolean = models.BooleanField(default=False)
    solution = models.CharField(max_length=255, null=True)
    date_add = models.DateField(auto_now_add=True)

class Prediction_output(models.Model):
    product = models.ForeignKey(Specific_product, on_delete=models.SET_NULL, null=True)
    prediction = models.CharField(max_length=200, null=False)
    date_added = models.DateTimeField(auto_now_add=True)

class Customer(models.Model):
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=200)
    price = models.FloatField()
    digital = models.BooleanField(default=False, null=True, blank=True)
    image = models.ImageField(null=True, blank=True)

    def __str__(self):
        return self.name

    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url


class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False)
    transaction_id = models.CharField(max_length=100, null=True)

    def __str__(self):
        return str(self.id)

    @property
    def shipping(self):
        shipping = False
        orderitems = self.orderitem_set.all()
        for i in orderitems:
            if i.product.digital == False:
                shipping = True
        return shipping

    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        return total

    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total


class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total


class ShippingAddress(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    address = models.CharField(max_length=200, null=False)
    city = models.CharField(max_length=200, null=False)
    state = models.CharField(max_length=200, null=False)
    zipcode = models.CharField(max_length=200, null=False)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.address

class Pay_slips(models.Model):
    company_name = models.CharField(max_length=200,null=False)
    email=models.EmailField(max_length=255)
    product = models.CharField(max_length=200,null=False)
    amount = models.CharField(max_length=200)
    boolean = models.BooleanField(default=False)