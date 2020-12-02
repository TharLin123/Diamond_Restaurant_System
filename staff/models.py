from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver




class Supplier(models.Model): 
    supplier_name = models.CharField(max_length=30)
    phone_number = models.CharField(max_length=20)
    email = models.EmailField(max_length=20)
    address = models.CharField(max_length=30)

    class Meta:
        verbose_name = "Supplier"
        verbose_name_plural = "Suppliers"

    def __str__(self):
        return self.supplier_name


class Food(models.Model):
    food_types = (('D','Dietary'),('VF','Vegetable and Fruits'),('K','Korean Food'),('C','Chinese Food'),('T','Taiwan Food'))
    food_quality = (('E','Excellent'),('G','Good'),('N','Normal'),('B','Bad'),('VB','Very Bad'))
    food_supplier = models.ForeignKey(Supplier,on_delete=models.CASCADE)
    food_name = models.CharField(max_length=30)
    food_type = models.CharField(choices=food_types,max_length=20)
    image = models.ImageField(default = 'default.jpg',upload_to = 'food_pictures')
    price = models.IntegerField()
    quality = models.CharField(choices= food_quality,max_length=20)

    def __str__(self):
        return self.food_name


class OrderFood(models.Model):
    customer = models.ForeignKey(User,verbose_name='Ordered By',on_delete=models.CASCADE,null=True)
    food = models.ForeignKey(Food,on_delete=models.CASCADE,null=True)
    quantity = models.IntegerField(default=1)
    ordered = models.BooleanField(default=False)

    def calculate_price(self):
        return food.price * self.quantity

    def __str__(self):
        return f'{self.food} = {self.quantity}'  

class FoodCart(models.Model):
    customer = models.ForeignKey(User,verbose_name='Ordered By',on_delete=models.CASCADE)
    food_to_order = models.ManyToManyField(OrderFood)
    purchased_date = models.DateField(auto_now_add=True,editable=True)
    purchased_time = models.TimeField(auto_now_add=True,editable=True)
    ordered = models.BooleanField(default=False)

    def calculate_total_price(self):
        totalPrice = self.food_to_order.filter(ordered=False)
        finalPrice = []
        for total in totalPrice:
            finalPrice.append(total.food.price * total.quantity)
        return sum(finalPrice)

    def __str__(self):
        return f'{self.customer} ordered on {self.purchased_date} at {self.purchased_time}'


class Customer(User):
    genders=(('M','Male'),('F','Female'))
    name = models.CharField(max_length=20,verbose_name='Name')
    dob = models.DateField(verbose_name='Date of Birth')
    phone_number = models.CharField(max_length=20,verbose_name='Phone Number')
    address = models.CharField(max_length=20,verbose_name='Address')
    gender = models.CharField(choices=genders,max_length=20)

    def __str__(self):
        return self.name


class CustomerPayment(models.Model):
    payment_methods=(('M','Master'),('F','Visa'),('F','Paypal'),('F','Cash'),('F','Transfer'))
    customer = models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    total_price = models.IntegerField(default=1)
    food_cart = models.OneToOneField(FoodCart,on_delete=models.CASCADE,null=True)
    payment_method = models.CharField(choices=payment_methods,max_length=20)
    name_on_card = models.CharField(max_length=30)
    card_number = models.CharField(max_length=30)

    def __str__(self):
        return f'{self.customer} made a payment'


class Profile(models.Model):
    user = models.OneToOneField(User,on_delete= models.CASCADE)
    image = models.ImageField(default = 'staff_pictures/default.jpg',upload_to = 'staff_pictures')

    def __str__(self):
        return f"{self.user.username}'s' Profile"


class Staff(models.Model):
    genders=(('M','Male'),('F','Female'))
    name = models.CharField(max_length=20,verbose_name='Name')
    dob = models.DateField(verbose_name='Date of Birth')
    phone_number = models.CharField(max_length=20,verbose_name='Phone Number')
    address = models.CharField(max_length=20,verbose_name='Address')
    gender = models.CharField(choices=genders,max_length=20)

    def __str__(self):
        return self.name

class Delivery(models.Model):
    food_to_deliver = models.OneToOneField(FoodCart,on_delete=models.CASCADE,null=True)
    staff_to_deliver = models.ForeignKey(Staff,on_delete=models.CASCADE,null=True)
    customer = models.ForeignKey(User,on_delete= models.CASCADE)
    delivered = models.BooleanField(default=False)
    deliver_request_date = models.DateField(auto_now_add=True,editable=True)
    deliver_request_time = models.TimeField(auto_now_add=True,editable=True)

    def __str__(self):
        if self.delivered == False:
            return f'{self.customer} requested a delivery.'
        else:
            return f'{self.customer} order is completed.'