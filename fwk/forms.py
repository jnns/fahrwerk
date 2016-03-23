# -*- coding: utf-8 -*-

from django import forms
from django.core.exceptions import ValidationError

from .models import Order

class OrderForm(forms.ModelForm):
    error_css_class = 'error'
    required_css_class = 'required'

    class Meta:
        model = Order
        fields = (
            'from_person',
            'from_company',
            'from_street',
            'from_streetnumber',
            'from_zipcode',
            'from_comment',
            'timeframe_pickup',
            'to_person',
            'to_company',
            'to_street',
            'to_streetnumber',
            'to_zipcode',
            'to_comment',
            'timeframe_dropoff',
            'packages_s',
            'packages_m',
            'packages_l',
        )

    def clean(self):
        if self.timeframe_pickup > self.timeframe_dropoff:
            raise ValidationError(
                "Zeitreisen können wir leider nicht. Bitte "
                "gib einen Auslieferungszeitraum an, der nach "
                "der Abholung liegt.")
        return self.cleaned_data