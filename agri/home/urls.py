from django.contrib import admin
from django.urls import path,include
from home import views
urlpatterns = [
    path('', views.index,name='home'),
    path('results', views.searching,name='results'),
    path('order', views.order,name='order'),
    path('home', views.index,name='home'),
    path('cart', views.cart,name='cart'),
    path('contact', views.contact,name='contact'),
    path('signup', views.signup,name='signup'),
    path('login',views.loginuser,name="login"),
    path('logoutuser', views.logoutuser,name='logoutuser'),
    path('image', views.image,name='image'),
    path('order', views.order,name='order'),
    path('upload', views.uploadImage,name='upload'),
    path('calc', views.calc,name='calc'),
    path('add', views.add,name='add'),
    path('cart_view', views.cart_view,name='cart_view'),
    path('exit', views.exit,name='exit'),
    path('otp', views.otp,name='otp'),
   
]


