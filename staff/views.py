from django.shortcuts import render,redirect,HttpResponse
from .forms import RegistrationForm,UserUpdateForm,ProfileUpdateForm,FoodOrderForm,PaymentForm,FoodCartForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Customer,Food,OrderFood,FoodCart
from django.views.generic import ListView
from django import forms

def home(request):
    return render(request,'index.html')


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Registered successfully. You can login now 😉.")
            return redirect('staff-login')
    else:
        form = RegistrationForm()
        context = {'form':form}
        return render(request,'staff_register.html',context)


@login_required
def profile(request):
    if request.method=='POST':
        u_form = UserUpdateForm(request.POST,instance=Customer.objects.get(id=request.user.id))
        p_form = ProfileUpdateForm(request.POST,request.FILES,instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, "Profile is updated successfully 😘.")
            return redirect('staff-profile')
    else:
        u_form = UserUpdateForm(instance=Customer.objects.get(id=request.user.id))
        p_form = ProfileUpdateForm(instance=request.user.profile)
    context = {
            "user_form" : u_form,
            "profile_form" : p_form
    }
    return render(request,'profile.html',context)


def foodList(request):
    form = FoodOrderForm()
    food = Food.objects.all()
    context = { 'food' : food , 'form' : form }
    return render(request,'food.html',context)
    
@login_required 
def add_to_cart(request,id):
    if request.method == 'POST':
        food_to_add = Food.objects.get(id=id)
        food_order_form = FoodOrderForm(request.POST)
        food_cart_qs,created = FoodCart.objects.get_or_create(customer=request.user,ordered = False)
        if food_order_form.is_valid():
            author = food_order_form.save(commit=False)
            author.customer = request.user
            author.food = food_to_add
            author.save()
            order_food = food_cart_qs.food_to_order.filter(food=food_to_add).first()
            food_added = OrderFood.objects.all().last()
            if food_cart_qs.food_to_order.filter(food=food_to_add).exists():
                order_food.quantity += food_added.quantity
                messages.success(request, f"{food_added.quantity} {food_to_add} is added to the FoodCart successfully 😇.")
                order_food.save()
            else:
                messages.success(request, f"{food_added.quantity} {food_to_add} is added to the FoodCart successfully 🥳.")
                food_cart_qs.food_to_order.add(food_added)
    return redirect('food-list')


@login_required 
def shoppingCart(request):
    food_order = FoodCart.objects.filter(customer=request.user,ordered=False).last()
    if food_order != None:
        total_price = food_order.calculate_total_price()
        ordered_food = food_order.food_to_order.filter(ordered = False)
        if request.method == 'GET':
            payment_form = PaymentForm(initial={'customer':request.user,'total_price':total_price,'food_cart':food_order})
            payment_form.fields['customer'].widget = forms.HiddenInput()
            payment_form.fields['food_cart'].widget = forms.HiddenInput()
            context = {
                'payment_form':payment_form,
                'ordered_food' : ordered_food,
                'food_order':food_order,
                'total_price':total_price}
            return render(request,'order_food.html',context)
        else:
            payment_form = PaymentForm(request.POST)
            messages.success(request, f"Foods added to the Order List 😍. You may cancel within 2 hours 😤.")
            if payment_form.is_valid():
                for ordered_foods in ordered_food:
                    ordered_foods.ordered = True
                    ordered_foods.save()
                food_order.ordered = True
                food_order.save()   
                payment_form.save()
                return redirect('order-list')
    else:
        messages.success(request, "No foods in th food-cart yet 😔. Please add foods to the food-cart 😋.")
        return redirect(request.META['HTTP_REFERER'])

            
@login_required
def orderList(request):
    orderedFoodList = OrderFood.objects.filter(customer=request.user,ordered=True)
    context = {'food_list':orderedFoodList}
    return render(request,'order_list.html',context)


@login_required
def deleteOrder(request,id):
    orderedFoodList = OrderFood.objects.get(id=id)
    orderedFoodList.delete()
    messages.success(request, f"{orderedFoodList.quantity} {orderedFoodList.food.food_name} is cancelled successfully 😩.")
    return redirect(request.META['HTTP_REFERER'])

@login_required
def searchOrderedList(request):
    if request.method == 'GET':
        search = request.GET.get('search')
        searchOrderList = Food.objects.filter(food_name__icontains = search)
        context = {'food' : searchOrderList}
        return render(request,'search.html',context)