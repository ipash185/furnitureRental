from datetime import date

from django import forms
from django.contrib.auth.models import User

from app.models import Product
from app.models import Rent


class RentForm(forms.ModelForm):
    user = forms.ModelChoiceField(queryset=User.objects.all(), required=True, widget=forms.HiddenInput())
    product = forms.ModelChoiceField(queryset=Product.objects.all(), required=True, widget=forms.HiddenInput())
    status = forms.ChoiceField(choices=Rent.Status.choices, widget=forms.HiddenInput(), initial=Rent.Status.pending)
    rental_day = forms.IntegerField(widget=forms.HiddenInput(), required=False)
    total_price = forms.IntegerField(widget=forms.HiddenInput(), required=False)
    is_returned = forms.BooleanField(widget=forms.HiddenInput(), required=False)
    start_date = forms.DateField(widget=forms.SelectDateWidget(years=range(2024, 2030)))
    end_date = forms.DateField(widget=forms.SelectDateWidget(years=range(2024, 2030)))

    class Meta:
        model = Rent
        fields = ['user', 'product', 'start_date', 'end_date',
                  'status', 'rental_day', 'total_price', 'is_returned']

    def clean(self):
        super(RentForm, self).clean()
        start_date = self.cleaned_data.get('start_date')
        end_date = self.cleaned_data.get('end_date')
        qty = self.cleaned_data.get('quantity')
        if start_date <= date.today() or start_date == date.today():
            self.errors['start_date'] = self.error_class(['Rent Start Date cannot be Today or Previous Day'])
        elif end_date == start_date or end_date <= start_date:
            self.errors['end_date'] = self.error_class(['Rent End Date cannot be Rent start date'])

        return self.cleaned_data
