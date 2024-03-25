from datetime import date, timedelta

from django.core.exceptions import ValidationError
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.postgres.search import SearchVector
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template.loader import get_template
from django.conf import settings

from app.decorators import user_information_required
from app.forms import RentForm
from app.forms.comment import CommentForm
from app.forms import ThresholdForm
from app.models import Product, Rent, Comment, Profit, Threshold, Notifications
from io import BytesIO
from xhtml2pdf import pisa
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from decimal import Decimal

def alert_below_threshold(category):
    try:
        # Create a notification message based on the provided category
        notification_message = f"The available number of category : {category} products has fallen below the threshold."

        # Create a new instance of Notifications with the notification message
        notification_instance = Notifications(notification=notification_message)

        # Save the new instance to the database
        notification_instance.save()

        # Send an email with the notification message to the specified recipient email

        YOUR_GOOGLE_EMAIL = 'ashu.anshul12@gmail.com'  # The email you setup to send the email using app password
        YOUR_GOOGLE_EMAIL_APP_PASSWORD = 'acbvynsmlayocfba'  # The app password you generated

        smtpserver = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        smtpserver.ehlo()
        smtpserver.login(YOUR_GOOGLE_EMAIL, YOUR_GOOGLE_EMAIL_APP_PASSWORD)

        # Test send mail
        sent_from = YOUR_GOOGLE_EMAIL
        sent_to = ["raajadas.rd@gmail.com", "ashu.anshul12@gmail.com", "theantiksur@gmail.com"]
        # sent_to = ["ashu.anshul12@gmail.com"]
        subject = "Notification: Product Threshold Alert"
        body = notification_message

        msg = MIMEMultipart()
        msg['From'] = sent_from
        msg['To'] = ", ".join(sent_to)
        msg['Subject'] = subject

        msg.attach(MIMEText(body, 'plain'))

        smtpserver.sendmail(sent_from, sent_to, msg.as_string())

        smtpserver.close()

        # Optionally, print the category for debugging purposes
        # print(category)
        # print(notification_message)

    except ValidationError as e:
        # Handle validation errors (e.g., if the notification message is invalid)
        print(f"Validation error: {e}")

    except Exception as e:
        # Handle other exceptions (e.g., SMTP errors)
        print(f"An error occurred: {e}")

def check_update_threshold(category, action):
    threshold = Threshold.objects.first()  # As there's only one instance of Threshold
    print(threshold)
    if category == 'sofa':
        threshold.available_sofa += 1*action
        if threshold.available_sofa < threshold.threshold_sofa:
            alert_below_threshold(category)
    elif category == 'chair':
        threshold.available_chair += 1*action
        if threshold.available_chair < threshold.threshold_chair:
            alert_below_threshold(category)
    elif category == 'table':
        threshold.available_table += 1*action
        if threshold.available_table < threshold.threshold_table:
            alert_below_threshold(category)
    elif category == 'bed':
        threshold.available_bed += 1*action
        if threshold.available_bed < threshold.threshold_bed:
            alert_below_threshold(category)
    threshold.save()
    

def home(request):
    products = Product.objects.filter(available=True).order_by('?')
    new_products = Product.objects.filter(available=True).order_by('created_at')[:5]
    
    context = {
        'products': products,
        'new_products': new_products
    }
    
    return render(request, 'index.html', context)


def products_detail(request, product_id):
    product = Product.objects.get(id=product_id)
    all_products = Product.objects.filter(available=True).order_by('?')[:5]
    comments = Comment.objects.filter(product=product_id)

    if request.method == 'POST':
        form = CommentForm(request.POST, initial={'product': product, 'user': request.user.pk})
        if request.user:
            if form.is_valid():
                form.save()
                return redirect('product_detail', product_id)
        else:
            redirect('login')
    else:
        form = CommentForm(initial={'product': product, 'user': request.user.pk})

    context = {
        'product': product,
        'all_products': all_products,
        'form': form,
        'comments': comments
    }
    return render(request, 'products_detail.html', context)


@login_required(login_url='login')
@user_information_required
def rent(request, product_id):
    request_product = Product.objects.get(id=product_id)
    if request.method == 'POST':
        form = RentForm(request.POST, initial={'product': request_product, 'user': request.user.pk})
        if form.is_valid():
            rents = form.save(commit=False)
            rents.rental_day = int((rents.end_date - rents.start_date).days)
            rents.total_price = rents.rental_day * request_product.price

            # Update the count of available products in the Threshold model
            # second argument to denote whether to increase or decrease that count
            check_update_threshold(request_product.category, -1)
            request_product.available = False
            request_product.save()
            rents.save()
            return redirect('index')
        else:
            messages.error(request, form.errors)
    else:
        product = request_product.pk
        user = request.user.pk

        form = RentForm(initial={'product': product, 'user': user, 'start_date': date.today() + timedelta(1),
                                 'end_date': date.today() + timedelta(2)})

    return render(request, 'rent_form.html', {'form': form, 'product': request_product})


@login_required(login_url='login')
def my_rent_products(request):
    rents = Rent.objects.filter(user=request.user).order_by('created_at')
    return render(request, 'my_rent_products.html', {'rents': rents})


@login_required(login_url='login')
def cancel_rent(request, rent_id):
    rents = Rent.objects.get(id=rent_id)
    product = rents.product
    product.available = True
    check_update_threshold(product.category, 1)
    product.save()
    rents.delete()
    return redirect('my_rent_products')


@login_required(login_url='login')
def return_request(request, rent_id):
    rents = Rent.objects.get(id=rent_id)
    rents.status = 'returned'
    rents.save()
    return redirect('my_rent_products')

@login_required(login_url='login')
def product_damaged(request, rent_id):
    rents = Rent.objects.get(id=rent_id)
    rents.status = 'damaged'
    rents.product.available = False
    rents.product.duration += max(rents.rental_day, int((date.today() - rents.start_date).days))
    
    cost = rents.product.investment * Decimal(0.1) * Decimal(rents.product.duration / 365)
    ref = Profit.objects.first()
    ref.investment -= cost
    
    ref.save()
    rents.save()
    return redirect('my_rent_products')

def search(request):
    query = request.GET.get('query')
    if not query:
        return redirect('index')
    else:
        products = Product.objects.annotate(search=SearchVector('name', 'brand')).filter(search=query)
    context = {
        'products': products,
        'query': query
    }
    return render(request, 'search.html', context)


@login_required(login_url='login')
def delete_comment(request, comment_id):
    user = request.user
    comment = Comment.objects.get(id=comment_id, user=user)
    comment.delete()
    return redirect('product_detail', comment.product.id)


@login_required(login_url='login')
def billing(request, product_id):
    rent_prod = Rent.objects.get(id=product_id)
    price = rent_prod.total_price
    context = {
        'rent': rent_prod,
        'price': price,
    }
    return render(request, 'billing.html', context)


def render_to_pdf(template_src, context_dict=None):
    if context_dict is None:
        context_dict = {}
    template = get_template(template_src)
    html = template.render(context_dict)
    result = BytesIO()

    # This part will create the pdf.
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None

def virtual(request):
    return render(request, 'virtual.html')
