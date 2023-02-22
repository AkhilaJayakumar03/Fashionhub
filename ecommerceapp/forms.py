from django import forms

class shopregform(forms.Form):
    shopname=forms.CharField(max_length=30)
    location=forms.CharField(max_length=30)
    shopid=forms.IntegerField()
    email=forms.EmailField()
    phonenumber=forms.IntegerField()
    password=forms.CharField(max_length=30)
    confirmpassword=forms.CharField(max_length=30)

class shoplogform(forms.Form):
    shopname=forms.CharField(max_length=30)
    password = forms.CharField(max_length=30)

class fileupform(forms.Form):
    productname=forms.CharField(max_length=30)
    productprice=forms.IntegerField()
    description=forms.CharField(max_length=30)
    productimage=forms.ImageField()

class cardforms(forms.Form):
    cardnumber=forms.IntegerField()
    holdername=forms.CharField(max_length=30)
    expire=forms.CharField(max_length=30)
    ccv=forms.IntegerField()
