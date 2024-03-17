from django import forms
from django.contrib.auth.models import User

from app.models import Comment, Product


class CommentForm(forms.ModelForm):
    user = forms.ModelChoiceField(queryset=User.objects.all(), required=True, widget=forms.HiddenInput())
    product = forms.ModelChoiceField(queryset=Product.objects.all(), required=True, widget=forms.HiddenInput())
    comment = forms.CharField(max_length=500, widget=forms.Textarea, required=True)

    class Meta:
        model = Comment
        fields = ('user', 'product', 'comment')
