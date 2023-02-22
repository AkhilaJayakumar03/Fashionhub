from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class shopregmodel(models.Model):
    shopname=models.CharField(max_length=30)
    location=models.CharField(max_length=30)
    shopid=models.IntegerField()
    email=models.EmailField()
    phonenumber=models.IntegerField()
    password=models.CharField(max_length=30)
    def __str__(self):
        return self.shopname


class fileupmodel(models.Model):
    shopid=models.IntegerField()
    productname = models.CharField(max_length=30)
    productprice = models.IntegerField()
    description = models.CharField(max_length=100)
    productimage = models.ImageField(upload_to='ecommerceapp/static')
    def __str__(self):
        return self.productname

class profile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    auth_token=models.CharField(max_length=100)
    is_verified=models.BooleanField(default=False)
    created_at=models.DateTimeField(auto_now_add=True)
    # def __str__(self):
    #     return self.User

class cart(models.Model):
    productname = models.CharField(max_length=30)
    productprice = models.IntegerField()
    description = models.CharField(max_length=100)
    productimage = models.ImageField(upload_to='ecommerceapp/static')
    userid = models.IntegerField()
    def __str__(self):
        return self.productname


class wishlist(models.Model):
    productname = models.CharField(max_length=30)
    productprice = models.IntegerField()
    description = models.CharField(max_length=100)
    productimage = models.ImageField(upload_to='ecommerceapp/static')
    userid=models.IntegerField()
    def __str__(self):
        return self.productname


class buy(models.Model):
    productname = models.CharField(max_length=30)
    productprice = models.IntegerField()
    description = models.CharField(max_length=100)
    productimage = models.ImageField(upload_to='ecommerceapp/static')
    quantity = models.IntegerField()
    def __str__(self):
        return self.productname


class cardmodels(models.Model):
    cardnumber=models.IntegerField()
    holdername=models.CharField(max_length=30)
    expire=models.CharField(max_length=30)
    ccv=models.IntegerField()
    def __str__(self):
        return self.holdername


class shopnotify(models.Model):
    content=models.CharField(max_length=200)
    date=models.DateField(auto_now_add=True)
    def __str__(self):
        return self.content


class usernotify(models.Model):
    content = models.CharField(max_length=200)
    date = models.DateField(auto_now_add=True)
    def __str__(self):
        return self.content

#__str__ : the str method returns a human readable or informal string representation of an object






