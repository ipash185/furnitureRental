from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from datetime import date

from app.forms import ProductForm, ThresholdForm
from app.models import Product, Rent, Profit, Notifications, Threshold

from decimal import Decimal

from .home import check_update_threshold, alert_below_threshold


# def set_threshold(request):
#     if request.method == 'POST':
#         form = ThresholdForm(request.POST)
#         if form.is_valid():
#             threshold_sofa = form.cleaned_data['threshold_sofa']
#             threshold_chair = form.cleaned_data['threshold_chair']
#             threshold_table = form.cleaned_data['threshold_table']
#             threshold_bed = form.cleaned_data['threshold_bed']
            
#             # Update or create the Threshold model instance
#             threshold, _ = Threshold.objects.get_or_create(pk=1)  # Assuming there's only one instance
#             threshold.threshold_sofa = threshold_sofa
#             threshold.threshold_chair = threshold_chair
#             threshold.threshold_table = threshold_table
#             threshold.threshold_bed = threshold_bed
#             print(threshold.threshold_bed, threshold.threshold_table, threshold.threshold_chair, threshold.threshold_sofa)
#             threshold.save()

#             return redirect('dashboard')  # Redirect to a success page or any other page
#         else:
#             print(form.errors)
#     else:
#         form = ThresholdForm()
#         # print("invalid form")
    
#     return redirect('dashboard')

@login_required(login_url='/login/')
@staff_member_required()
def dashboard(request):
    threshold, _ = Threshold.objects.get_or_create(pk=1)  # Assuming there's only one instance
    if request.method == 'POST':
        form = ThresholdForm(request.POST)
        if form.is_valid():
            threshold_sofa = form.cleaned_data['threshold_sofa']
            threshold_chair = form.cleaned_data['threshold_chair']
            threshold_table = form.cleaned_data['threshold_table']
            threshold_bed = form.cleaned_data['threshold_bed']
            
            # Update or create the Threshold model instance
            threshold.threshold_sofa = threshold_sofa
            threshold.threshold_chair = threshold_chair
            threshold.threshold_table = threshold_table
            threshold.threshold_bed = threshold_bed
            print(threshold.threshold_bed, threshold.threshold_table, threshold.threshold_chair, threshold.threshold_sofa)
            threshold.save()

            return redirect('dashboard')  # Redirect to a success page or any other page
        else:
            print(form.errors)
            return redirect('dashboard')
    else:
        form = ThresholdForm(initial={'threshold_sofa': threshold.threshold_sofa, 'threshold_chair': threshold.threshold_chair, 'threshold_table': threshold.threshold_table, 'threshold_bed': threshold.threshold_bed})
    product = Product.objects.all()
    
    if Profit.objects.count() == 0:
        Profit.objects.create(investment=0, revenue = 0)
    
    ref = Profit.objects.first()
    investment = ref.investment
    revenue = ref.revenue
    
    return render(request, 'db_index.html', {"product": product, "investment": investment, "revenue": revenue, "form": form})

@login_required(login_url='/login/')
@staff_member_required()
def view_notifications(request):
    
    notifications = Notifications.objects.all()
    
    return render(request, 'notifications.html', {"notifications": notifications})

@login_required(login_url='/login/')
@staff_member_required()
def delete_notification(request, notification_id):
    
    notification = Notifications.objects.get(id=notification_id)
    notification.delete()

    return redirect('view_notifications')


@login_required(login_url='/login/')
@staff_member_required()
def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)  # request.FILES is for image
        if form.is_valid():
            
            new_investment = Profit.objects.all().first()
            new_investment.investment += form.cleaned_data['investment']
            new_investment.save()
            
            form.save()
            return redirect('dashboard')

    else:
        form = ProductForm()

    return render(request, 'add_product.html', {"form": form})


@login_required(login_url='/login/')
@staff_member_required()
def delete_product(request, product_id):
    product = Product.objects.get(id=product_id)
    product.delete()
    return redirect('dashboard')


@login_required(login_url='/login/')
@staff_member_required()
def edit_product(request, product_id):
    product = Product.objects.get(id=product_id)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)  # request.FILES is for image
        if form.is_valid():
            name = form.cleaned_data['name']
            description = form.cleaned_data['description']
            price = form.cleaned_data['price']
            image = form.cleaned_data['image']  # bug
            brand = form.cleaned_data['brand']
            available = form.cleaned_data['available']

            Product.objects.filter(id=product_id).update(name=name, description=description, price=price, image=image,
                                                         brand=brand, available=available)
            return redirect('dashboard')

    else:
        form = ProductForm(instance=product)

    return render(request, 'add_product.html', {"form": form})


@login_required(login_url='login')
@staff_member_required()
def pending_rent_requests(request):
    rent_request = Rent.objects.filter(status='pending').order_by('created_at')

    context = {
        'rent_request': rent_request
    }
    return render(request, 'pending_rent_requests.html', context)


@login_required(login_url='login')
@staff_member_required()
def accept_rent_request(request, rent_id):
    rent = Rent.objects.get(id=rent_id)
    rent.status = 'rented'
    rent.save()
    return redirect('pending_rent_requests')


@login_required(login_url='login')
@staff_member_required()
def reject_rent_request(request, rent_id):
    rent = Rent.objects.get(id=rent_id)
    rent.status = 'rejected'
    rent.product.available = True
    check_update_threshold(rent.product.category, 1)
    rent.product.save()
    rent.save()
    return redirect('pending_rent_requests')


@login_required(login_url='login')
@staff_member_required()
def delivery_rented_products(request):
    products = Rent.objects.filter(status='rented', is_rented=False).order_by('created_at')

    context = {
        'rented_products': products
    }
    return render(request, 'deliver_rented_products.html', context)


@login_required(login_url='login')
@staff_member_required()
def delivered_rented_products(request, rent_id):
    rent = Rent.objects.get(id=rent_id)
    rent.is_rented = True
    rent.save()
    return redirect('delivery_rented_products')


@login_required(login_url='login')
@staff_member_required()
def rented_products(request):
    rented_product = Rent.objects.filter(is_rented=True).order_by('created_at')

    context = {
        'rented_product': rented_product
    }
    return render(request, 'rented_products.html', context)


@login_required(login_url='login')
@staff_member_required()
def accept_return_request(request, rent_id):
    rent = Rent.objects.get(id=rent_id)
    rent.is_returned = True
    
    time_used = min(1,int((date.today() - rent.start_date).days))
    print(time_used)
    rent.product.duration += time_used
    rent.total_price = rent.product.price * time_used
    
    if time_used > rent.rental_day:
        rent.total_price += (time_used - rent.rental_day) * rent.product.price * Decimal(1.1)
        
    ref = Profit.objects.first()
    ref.revenue += rent.total_price
    ref.save()
    
    if rent.product.duration > 365:
        rent.product.price -= rent.product.price * Decimal(0.1)
    
    rent.product.available = True
    check_update_threshold(rent.product.category, 1)
    rent.product.save()
    rent.save()
    return redirect('dashboard')


@login_required(login_url='login')
@staff_member_required()
def all_rent_request(request):
    rent_request = Rent.objects.filter(status='returned', is_returned=False).order_by('created_at')

    context = {
        'rent_request': rent_request
    }
    return render(request, 'all_rent_request.html', context)


@login_required(login_url='login')
@staff_member_required()
def return_product(request):
    return_furniture = Rent.objects.filter(is_returned=True).order_by('created_at')

    context = {
        'return_furniture': return_furniture
    }
    return render(request, 'return_product.html', context)


@login_required(login_url='login')
@staff_member_required()
def activity(request):
    all_rent = Rent.objects.all().order_by('created_at')

    context = {
        'all_rent': all_rent
    }
    return render(request, 'all_rent_activity.html', context)
