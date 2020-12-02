from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('register/', views.register, name='staff-register'),
    path('profile/',views.profile,name='staff-profile'),
    path('addtocart/<int:id>',views.add_to_cart,name='add-to-cart'),
    path('delete/<int:id>',views.deleteOrder,name='delete-order'),
    path('orderlist/',views.orderList,name='order-list'),
    path('shoppingCart/', views.shoppingCart, name= "shopping-cart"),
    path('login/',auth_views.LoginView.as_view(template_name='login1.html'), name = 'staff-login'),
    path('food/', views.foodList, name= "food-list"),
    path('search/', views.searchOrderedList, name = 'search-order'),
    path('logout/',auth_views.LogoutView.as_view(template_name='logout.html'), name = 'logout')
]