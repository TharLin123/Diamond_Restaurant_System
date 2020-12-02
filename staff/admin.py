from django.contrib import admin
from .models import Supplier,Food,OrderFood,Profile,Staff,CustomerPayment,FoodCart,Customer,Delivery

admin.site.register(Supplier)
admin.site.register(Food)
admin.site.register(OrderFood)
admin.site.register(Profile)
admin.site.register(Staff)
admin.site.register(Customer)
admin.site.register(CustomerPayment)
admin.site.register(Delivery)
admin.site.register(FoodCart)
