from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from users.forms import UserForm, UserInformationForm, EditProfileForm
from users.models import UserInformation


def register(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserForm()
    return render(request, 'register.html', {"form": form})


@login_required(login_url='login')
def profile(request):
    username = request.user.username
    email = request.user.email
    first_name = request.user.first_name
    last_name = request.user.last_name
    if UserInformation.objects.filter(user=request.user).exists():
        phone = request.user.userinformation.phone
        address = request.user.userinformation.delivery_address
    else:
        phone = ''
        address = ''
    name = first_name + ' ' + last_name
    data = {'username': username, 'email': email, 'name': name, 'phone': phone, 'address': address}
    return render(request, 'profile.html', data)


@login_required(login_url='login')
def billingAddress(request):
    if request.method == "POST":
        form = UserInformationForm(request.POST)
        if form.is_valid():
            phone = form.cleaned_data['phone']
            address = form.cleaned_data['delivery_address']
            user = request.user
            form_data = UserInformation(user=user, phone=phone, delivery_address=address)
            form_data.save()
            return redirect('profile')
    else:
        form = UserInformationForm()

    return render(request, 'billing_address.html', {"form": form})


@login_required(login_url='login')
def edit_billing_address(request):
    if request.method == "POST":
        form = UserInformationForm(request.POST)
        if form.is_valid():
            phone = form.cleaned_data['phone']
            address = form.cleaned_data['delivery_address']
            UserInformation.objects.filter(user=request.user).update(phone=phone, delivery_address=address)
            return redirect('profile')
    else:
        userinfo = get_object_or_404(UserInformation, user=request.user)
        phone = userinfo.phone
        address = userinfo.delivery_address
        form = UserInformationForm(initial={'phone': phone, 'delivery_address': address})

    return render(request, 'billing_address.html', {"form": form})


@login_required(login_url='login')
def edit_profile(request):
    if request.method == "POST":
        form = EditProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = EditProfileForm(instance=request.user)
    return render(request, 'edit_profile.html', {"form": form})
