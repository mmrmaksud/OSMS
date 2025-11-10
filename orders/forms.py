# orders/forms.py
from django import forms

class CheckoutForm(forms.Form):
    customer_name = forms.CharField(max_length=120, label="Name")
    mobile = forms.CharField(max_length=20, label="Mobile")
    email = forms.EmailField(required=False, label="Email (Optional)")
    address = forms.CharField(widget=forms.Textarea(attrs={"rows": 3}), label="Address")
