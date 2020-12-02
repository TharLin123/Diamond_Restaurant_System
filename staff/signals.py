from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Profile,Customer,CustomerPayment,Delivery

@receiver(post_save,sender=Customer)
def create_profile(sender,instance,created,**kwargs):
    if created:
        Profile.objects.create(user=instance)

post_save.connect(create_profile,sender=User)

@receiver(post_save,sender=CustomerPayment)
def create_delivery(sender,instance,created,**kwargs):
    if created:
        Delivery.objects.create(customer=instance.customer,food_to_deliver=instance.food_cart)


