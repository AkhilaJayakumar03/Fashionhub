import datetime
from datetime import timedelta
from django.contrib.auth import authenticate
from django.core.mail import send_mail
from ecommercesite.settings import EMAIL_HOST_USER
from django.shortcuts import render,redirect
from django.http import HttpResponse
from .forms import *
from .models import*
import os
from django.contrib.auth.models import User
from django.contrib import messages
import uuid
from django.contrib.auth import logout


# Create your views here.

def about(request):
    return render(request,"about.html")

def contact(request):
    return render(request,"contact.html")

def home(request):
    return render(request,"home.html")


def register(request):
    return render(request,"register.html")

def index(request):
    return render(request,"index.html")

def shoplogin(request):
    if request.method == 'POST':
        a = shoplogform(request.POST)
        if a.is_valid():
            sn = a.cleaned_data["shopname"]
            ps = a.cleaned_data["password"]
            request.session['shopname']=sn#to make a variable global
            b = shopregmodel.objects.all()  # fetchall
            for i in b:
                if sn == i.shopname and ps == i.password:
                    request.session['id']=i.id
                    return redirect(shopprofile)
            else:
                messages.success(request, "Username or passsword wrong")
        else:
            messages.success(request, "Please enter password")
    return render(request,"shoplogin.html")

def shopregister(request):
    if request.method == 'POST':
        a = shopregform(request.POST)
        if a.is_valid():
            sn = a.cleaned_data["shopname"]
            ln = a.cleaned_data["location"]
            si = a.cleaned_data["shopid"]
            em=a.cleaned_data["email"]
            ph=a.cleaned_data["phonenumber"]
            ps = a.cleaned_data["password"]
            cp = a.cleaned_data["confirmpassword"]
            if ps == cp:
                b = shopregmodel(shopname=sn,location=ln,shopid=si,email=em,phonenumber=ph,password=ps)
                if shopregmodel.objects.filter(shopname=sn).first():
                    messages.success(request, "shop already registered...")
                    return redirect(shopregister)
                elif shopregmodel.objects.filter(shopid=si).first():
                    messages.success(request, "shop already registered...")
                    return redirect(shopregister)
                b.save()
                messages.success(request, "Registration success..Now you can login")
                return redirect(shoplogin)
            else:
                messages.success(request,"password doesn't match")
        else:
            messages.success(request,"registration failed")
    return render(request,"shopregister.html")

def fileupload(request):
    if request.method == 'POST':
        a = fileupform(request.POST, request.FILES)
        id = request.session['id']
        if a.is_valid():
            pn=a.cleaned_data["productname"]
            pr=a.cleaned_data["productprice"]
            ds=a.cleaned_data["description"]
            pm=a.cleaned_data["productimage"]
            b=fileupmodel(shopid=id,productname=pn,productprice=pr,description=ds,productimage=pm)
            b.save()
            messages.success(request,"product upload successfully.....")
        else:
            messages.success(request,"product upload failed.....")
    return render(request,"fileupload.html")

def shopprofile(request):
    shopname = request.session['shopname']
    return render(request,"shopprofile.html",{'shopname':shopname})

def productdisplay(request):
    shpid=request.session['id']
    a=fileupmodel.objects.all()
    pdtnm=[]
    pdtpr=[]
    pdtds=[]
    pdtim=[]
    pdtid=[]
    shopid=[]
    for i in a:
        sid=i.shopid
        shopid.append(sid)
        id=i.id
        pdtid.append(id)
        pm = i.productimage
        pdtim.append(str(pm).split('/')[-1])
        pn=i.productname
        pdtnm.append(pn)
        pr=i.productprice
        pdtpr.append(pr)
        ds=i.description
        pdtds.append(ds)
    mylist=zip(pdtim,pdtnm,pdtpr,pdtds,pdtid,shopid)
    return render(request, "productdisplay.html", {'mylist': mylist,'shpid':shpid})

#model.objects.all()-->fetch all data
#model.objects.get(id=id)
def productdelete(request,id):
    a=fileupmodel.objects.get(id=id)
    a.delete()
    messages.success(request, "product deleted..")
    return redirect(productdisplay)

def productedit(request,id):
    a=fileupmodel.objects.get(id=id)
    im=str(a.productimage).split('/')[-1]
    if request.method=='POST':
        if len(request.FILES): #to check the input of new file
            if len(a.productimage)>0:#old file
                os.remove(a.productimage.path)
            a.productimage=request.FILES["productimage"]
        a.productname=request.POST.get("productname")
        a.productprice=request.POST.get("productprice")
        a.description=request.POST.get("description")
        a.save()
        messages.success(request, "product updated..")
        return redirect(productdisplay)
    return render(request,'productedit.html',{'a':a,'im':im})

def viewallproducts(request):
    shpid = request.session['id']
    a = fileupmodel.objects.all()
    pdtnm = []
    pdtpr = []
    pdtds = []
    pdtim = []
    pdtid = []
    shopid = []
    for i in a:
        sid = i.shopid
        shopid.append(sid)
        id = i.id
        pdtid.append(id)
        pm = i.productimage
        pdtim.append(str(pm).split('/')[-1])
        pn = i.productname
        pdtnm.append(pn)
        pr = i.productprice
        pdtpr.append(pr)
        ds = i.description
        pdtds.append(ds)
    mylist = zip(pdtim, pdtnm, pdtpr, pdtds, pdtid, shopid)
    return render(request, "viewallproducts.html", {'mylist': mylist, 'shpid': shpid})



def userregister(request):
    if request.method=='POST':
        username=request.POST.get('username')
        email=request.POST.get('email')
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        password = request.POST.get('password')
        #checking whether the username exists
        if User.objects.filter(username=username).first():#the filter method is used to filter your search and allows you to return
         #only the rows that matches the search term
          #it will get first object from filter query.
            messages.success(request,'username already taken')
           #message.success:is a framework that allows you to store messages in one request and retrive them in the request page
            return redirect(userregister)
        if User.objects.filter(email=email).first():
            messages.success(request,'email already exists')
            return redirect(userregister)
        user_obj=User(username=username,email=email,first_name=firstname,last_name=lastname)
        user_obj.set_password(password)
        user_obj.save()
        #import uuid
        #uuid module:uuid that stands for universally unique identifiers
        #uuid4():that generates random uuid
        auth_token=str(uuid.uuid4())#vd3fr65237e68923re67dgy334r76
        profile_obj=profile.objects.create(user=user_obj,auth_token=auth_token)
        profile_obj.save()
        #user defined function
        send_mail_regis(email,auth_token)#mail sending function
        return render(request,"success.html")
    return render(request,"userregister.html")


def send_mail_regis(email,auth_token):
    subject="Your account has been verified"
    message=f'click the link to verify your account http://127.0.0.1:8000/ecommerceapp/verify/{auth_token}'
    #f formatter:the expressions are replaced by values
    email_from=EMAIL_HOST_USER#from
    recipient=[email]#to
    #inbuilt function
    send_mail(subject,message,email_from,recipient)


def verify(request,auth_token):
    profile_obj=profile.objects.filter(auth_token=auth_token).first()
    if profile_obj:
        if profile_obj.is_verified:
           messages.success(request,"your account is already verified")
           return redirect(userlogin)
        profile_obj.is_verified=True
        profile_obj.save()
        messages.success(request,"your account has been verified")
        return redirect(userlogin)
    else:
        messages.success(request,"user not found")
        return redirect(userlogin)


def userlogin(request):
    if 'id' in request.session:
        return redirect(userinter)
    if request.method=='POST':
        username=request.POST.get('username')
        password=request.POST.get('password')
        request.session['username']=username
        user_obj=User.objects.filter(username=username).first()
        if user_obj is None:
            messages.success(request,"user not found")
            return redirect(userlogin)
        profile_obj=profile.objects.filter(user=user_obj).first()
        if not profile_obj.is_verified:
            messages.success(request, "profile not verified check your mail")
            return redirect(userlogin)
        user=authenticate(username=username,password=password)
        if user is None:
            messages.success(request,'wrong password or username')
            return redirect(userlogin)
        request.session['id'] = user_obj.id
        return redirect(userinter)
    return render(request,"userlogin.html")


def userinter(request):
    if 'id' in request.session:
        username=request.session['username']
        b=request.session['id']
        return render(request,"userinterface.html",{'username':username,'b':b})
    return redirect(userlogin)

def success(request):
    return render(request,"success.html")


def viewproduct(request):
    a = fileupmodel.objects.all()
    pdtnm = []
    pdtpr = []
    pdtds = []
    pdtim = []
    pdtid = []
    for i in a:
        id = i.id
        pdtid.append(id)
        pm = i.productimage
        pdtim.append(str(pm).split('/')[-1])
        pn = i.productname
        pdtnm.append(pn)
        pr = i.productprice
        pdtpr.append(pr)
        ds = i.description
        pdtds.append(ds)
    mylist = zip(pdtim, pdtnm, pdtpr, pdtds, pdtid)
    return render(request,"viewproducts.html",{'mylist':mylist})

def addtocart(request,id):
    c=request.session['id']
    a = fileupmodel.objects.get(id=id)
    if cart.objects.filter(userid=c,productname=a.productname):
        return render(request,"itemalreadyincart.html")
    b = cart(userid=c,productname=a.productname,productprice=a.productprice,description=a.description,productimage=a.productimage)
    messages.success(request,"item added to cart successfully....")
    b.save()
    return redirect(viewproduct)


def cartdisplay(request):
    if 'id' in request.session:
        usid = request.session['id']
        a = cart.objects.all()
        pdtnm = []
        pdtpr = []
        pdtds = []
        pdtim = []
        pdtid = []
        userid = []
        for i in a:
            uid = i.userid
            userid.append(uid)
            id = i.id
            pdtid.append(id)
            pm = i.productimage
            pdtim.append(str(pm).split('/')[-1])
            pn = i.productname
            pdtnm.append(pn)
            pr = i.productprice
            pdtpr.append(pr)
            ds = i.description
            pdtds.append(ds)
        mylist = zip(pdtim, pdtnm, pdtpr, pdtds, pdtid, userid)
        return render(request, "cartdisplay.html", {'mylist': mylist, 'usid': usid})
    return redirect(userlogin)


def addtowishlist(request,id):
    o = request.session['id']
    a = fileupmodel.objects.get(id=id)
    if wishlist.objects.filter(userid=o,productname=a.productname):
        return render(request,"itemalreadyinwishlist.html")
    b = wishlist(userid=o,productname=a.productname, productprice=a.productprice, description=a.description,productimage=a.productimage)
    b.save()
    messages.success(request,"item added to wishlist successfully....")
    return redirect(viewproduct)

def wishdisplay(request):
    usid = request.session['id']
    a = wishlist.objects.all()
    pdtnm = []
    pdtpr = []
    pdtds = []
    pdtim = []
    pdtid = []
    userid=[]
    for i in a:
        uid = i.userid
        userid.append(uid)
        id = i.id
        pdtid.append(id)
        pm = i.productimage
        pdtim.append(str(pm).split('/')[-1])
        pn = i.productname
        pdtnm.append(pn)
        pr = i.productprice
        pdtpr.append(pr)
        ds = i.description
        pdtds.append(ds)
    mylist = zip(pdtim, pdtnm, pdtpr, pdtds, pdtid,userid)
    return render(request, "wishlistdisplay.html", {'mylist': mylist,'usid':usid})


def wishlisttocart(request,id):
    o = request.session['id']
    a = wishlist.objects.get(id=id)
    if cart.objects.filter(userid=o,productname=a.productname):
        return render(request,"itemalreadyincart.html")
    b = cart(userid=o, productname=a.productname, productprice=a.productprice, description=a.description,productimage=a.productimage)
    b.save()
    messages.success(request,"item added to cart successfully....")
    return redirect(wishdisplay)


def cartitemremove(request,id):
    a = cart.objects.get(id=id)
    a.delete()
    messages.success(request, "item removed from cart")
    return redirect(cartdisplay)

def wishitemremove(request,id):
    a = wishlist.objects.get(id=id)
    a.delete()
    messages.success(request,"item removed from wishlist")
    return redirect(wishdisplay)

def cartbuy(request,id):
    a=cart.objects.get(id=id)
    im = str(a.productimage).split('/')[-1]
    if request.method=='POST':
        pn=request.POST.get('productname')
        pr=request.POST.get('productprice')
        ds=request.POST.get('description')
        qt=request.POST.get('quantity')
        b=buy(productname=pn,productprice=pr,description=ds,quantity=qt)
        b.save()
        total=int(pr) * int(qt)
        return render(request,"finalbill.html",{'pn': pn,'pr': pr,'ds': ds,'qt': qt,'total': total,'im':im})
    return render(request,"buy.html",{'a':a,'im':im})


def payment(request):
    if request.method=='POST':
        cardnumber = request.POST.get('cardnumber')
        holdername = request.POST.get('holdername')
        expire = request.POST.get('expire')
        ccv = request.POST.get('ccv')
        b = cardmodels(cardnumber=cardnumber,holdername=holdername,expire=expire,ccv=ccv)
        b.save()
        c=datetime.date.today()
        d=c+timedelta(15)
        return render(request, "orderplaced.html",{'d':d})
    return render(request,"payment.html")


def usernotification(request):
    a=usernotify.objects.all()
    cn=[]
    dt=[]
    usid=[]
    for i in a:
        content=i.content
        cn.append(content)
        date = i.date
        dt.append(date)
        id=i.id
        usid.append(id)
    mylist=zip(cn,dt,usid)
    return render(request,"usernoti.html",{'mylist':mylist})


def shopnotification(request):
    a=shopnotify.objects.all()
    cn=[]
    dt=[]
    usid=[]
    for i in a:
        content=i.content
        cn.append(content)
        date = i.date
        dt.append(date)
        id=i.id
        usid.append(id)
    mylist=zip(cn,dt,usid)
    return render(request,"shopnoti.html",{'mylist':mylist})


def user_logout(request):
    if 'id' in request.session:
        request.session.flush()
        logout(request)
    return render(request,"index.html")

def shop_logout(request):
    return render(request,"index.html")



