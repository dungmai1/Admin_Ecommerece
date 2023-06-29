from django.contrib import admin
from django.urls import path
from myapp import views

app_name = 'myapp'

urlpatterns = [
    path('', views.home),
    path('products/', views.products, name='products'),
    path('addnewproduct/', views.addnewproduct, name='addnewproduct'),
    path('deleteproduct/<str:id>/<str:category_value>', views.deleteproduct, name='deleteproduct'),
    path('updateproducts/<str:id>/<str:Category>', views.updateproducts, name='updateproducts'),
    path('users/', views.users, name='users'),
    path('AddressUser/<str:id>', views.AddressUser, name='AddressUser'),
    path('addnewuser/', views.addnewuser, name='addnewuser'),
    path('order/', views.order, name='order'),
    path('processing/', views.processing, name='processing'),
    path('viewOrderProcessing/<str:id>/<str:iduser>', views.viewOrderProcessing, name='viewOrderProcessing'),
    path('shipping/', views.shipping, name='shipping'),
    path('delivered', views.delivered, name='delivered'),
    path('canceled/', views.canceled, name='canceled'),
    path('signin/', views.signin, name='signin'),
    path('Category/', views.Category, name='Category'),
    path('addCategory/', views.addCategory, name='addCategory'),
    path('UpdateCategory/<str:id>', views.UpdateCategory, name='UpdateCategory'),
    path('EditStatus/<str:id>/<str:iduser>', views.EditStatus, name='EditStatus'),
    path('CreateOrder/', views.CreateOrder, name='CreateOrder'),
]

