# -*- coding: utf-8 -*-

from django import forms
from django.core.exceptions import ValidationError
from django.utils.safestring import mark_safe
from django.utils import timezone

from .models import Order

class OrderForm(forms.ModelForm):
    error_css_class = 'error'
    required_css_class = 'required'

    class Meta:
        model = Order
        fields = (
            'from_person',
            'from_phone_no',
            'from_company',
            'from_street',
            'from_zipcode',
            'from_comment',
            'timeframe_pickup',
            'to_person',
            'to_phone_no',
            'to_company',
            'to_street',
            'to_zipcode',
            'to_comment',
            'timeframe_dropoff',
            'packages_s',
            'packages_m',
            'packages_l',
            'package_detail',
            'customer',
        )

    def clean_timeframe_pickup(self):
        # As the time datatype given by the form is naive in a way that it
        # can't be compared to UTC datetimes, we need to convert the current
        # timestampt to a localtime
        now = timezone.localtime(timezone.now())

        input = self.cleaned_data["timeframe_pickup"]
        given_time = now.replace(hour=input.hour, minute=0, second=0)

        if given_time <= now:
            raise ValidationError("Wir besitzen leider keine Zeitmaschine.")

        time_until = given_time - now
        if time_until.seconds / 60 < 60:
            raise ValidationError("Bitte gewähre uns mindestens 1 Stunde bis \
            zur Abholung, wenn du dieses Bestellformular nutzt. Für \
            zeitkritische Sendungen rufe uns bitte direkt an.")
        return input

    def clean(self):
        super(OrderForm, self).clean()

        data = self.cleaned_data

        errors = []

        # At least one package size must be given
        if not data.get("packages_s") and not data.get("packages_m") and not data.get("packages_l"):
            errors.append(ValidationError("Bitte gib die Größe deiner Sendung an."))

        # Dropoff must be after pickup
        try:
            if data.get("timeframe_pickup") > data.get("timeframe_dropoff"):
                errors.append(ValidationError(
                    mark_safe("Zeitreisen können wir leider nicht. Bitte "
                    "gib einen Auslieferungszeitraum an, der <strong>nach</strong> "
                    "der Abholung liegt.")))
        except TypeError:
            # if clean_timeframe_pickup failed there's a failing comparison
            # against None
            pass

        if errors:
            raise ValidationError(errors)

        return self.cleaned_data

class OrderAdminForm(forms.ModelForm):
    model = Order

    def clean(self):
        if self.cleaned_data.get("status") == 'CONFIRMED' and not self.cleaned_data.get("ecourier_id"):
            raise ValidationError("Der Auftrag kann nicht bestätigt \
                werden, solange keine Tournummer aus eCourier angegeben wurde.")