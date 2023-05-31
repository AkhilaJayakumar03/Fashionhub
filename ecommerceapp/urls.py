from django.urls import path
from.views import *

urlpatterns=[
    path('about/',about),
    path('contact/',contact),
    path('home/',home),
    path('index/',index),
    path('shoplogin/',shoplogin),
    path('shopregister/',shopregister),
    path('userlogin/',userlogin),
    path('userregister/',userregister),
    path('fileupload/',fileupload),
    path('shopprofile/',shopprofile),
    path('productdisplay/',productdisplay),
    path('delete/<int:id>',productdelete),
    path('edit/<int:id>',productedit),
    path('viewallproducts/',viewallproducts),
    path('userinter/',userinter),
    path('success/',success),
    path('verify/<auth_token>',verify),
    path('viewproduct/',viewproduct),
    path('addtocart/<int:id>',addtocart),
    path('addtowishlist/<int:id>',addtowishlist),
    path('wishdisplay/',wishdisplay),
    path('cartdisplay/',cartdisplay),
    path('cartitemremove/<int:id>',cartitemremove),
    path('wishitemremove/<int:id>',wishitemremove),
    path('cartbuy/<int:id>',cartbuy),
    path('payment/',payment),
    path('usernotification/',usernotification),
    path('shopnotification/',shopnotification),
    path('wishlisttocart/<int:id>',wishlisttocart),
    path('logout/',user_logout),
    path('shoplogout/',shop_logout)







    ]