from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from app.forms import ProductForm
from app.models import Product, Rent


@login_required(login_url='/login/')
@staff_member_required()
def dashboard(request):
    product = Product.objects.all()
    return render(request, 'db_index.html', {"product": product})


@login_required(login_url='/login/')
@staff_member_required()
def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)  # request.FILES is for image
        if form.is_valid():
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
    rent.save()
    return redirect('return_request')


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
