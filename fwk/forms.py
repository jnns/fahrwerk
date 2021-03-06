# -*- coding: utf-8 -*-

# expect all string literals to be unicode because I'm too lazy to prepend u''
# to all my strings and ugettext breaks otherwise.
from __future__ import unicode_literals

import logging

from django import forms
from django.core.exceptions import ValidationError
from django.utils.safestring import mark_safe
from django.utils import timezone
from django.utils.translation import ugettext as _

from constance import config

from .models import Order

logger = logging.getLogger(__name__)


class OrderConfirmation(forms.Form):
    pass


class OrderForm(forms.ModelForm):
    error_css_class = 'error'
    required_css_class = 'required'

    # Store values in object so they mustn't be retreived multiple times
    # Screw that, this generates an error while running migrate on an empty database.
    #MIN_POSTCODE = config.FWK_MIN_POSTCODE
    #MAX_POSTCODE = config.FWK_MAX_POSTCODE

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
            'customer_email'
        )

    def clean_timeframe_pickup(self):
        input = self.cleaned_data["timeframe_pickup"]

        # don't do any special validation if it's not a time window
        if input in ['ASAP', 'LOW', 'CUSTOM']:
            return input

        # As the time datatype given by the form is naive in a way that it
        # can't be compared to UTC datetimes, we need to convert the current
        # timestampt to a localtime
        now = timezone.localtime(timezone.now())

        try:
            desired_time = now.replace(hour=int(input), minute=0, second=0)
        except TypeError:
            raise ValidationError(_("Bitte einen korrekten Wert angeben."))

        if desired_time <= now:
            logger.info("Customer waited too long with submitting the form. \
                No time travel possible.")
            raise ValidationError(_("Wir besitzen leider keine Zeitmaschine."))

        if (desired_time - now).seconds / 60 < 30:
            logger.info("Customer tried to order pickup too early.")
            raise ValidationError(_("Bitte gewähre uns mindestens 30 Minuten bis \
            zur Abholung, wenn du dieses Bestellformular nutzt. Für \
            zeitkritische Sendungen rufe uns bitte direkt an."))
        return input

    def clean_to_zipcode(self):
        value = self.cleaned_data["to_zipcode"]
        if not config.FWK_MIN_POSTCODE <= value <= config.FWK_MAX_POSTCODE:
            logger.info("Customer tried to order delivery out of region.")
            raise ValidationError(_(
                "Dieser Ort liegt außerhalb unseres regulären Zustellgebietes. \
                Ruf uns doch an, damit wir über Transportmöglichkeiten \
                dorthin sprechen können: %s" % config.FWK_PHONE_NO))
        return value

    def clean_from_zipcode(self):
        value = self.cleaned_data["from_zipcode"]
        if not config.FWK_MIN_POSTCODE <= value <= config.FWK_MAX_POSTCODE:
            logger.info("Customer tried to order pickup from out of region.")
            raise ValidationError(_(
                "Dieser Ort liegt außerhalb unseres regulären Abholgebietes. \
                Ruf uns doch an, damit wir über Transportmöglichkeiten von \
                dort aus sprechen können: %s " % config.FWK_PHONE_NO))
        return value


    def clean(self):
        super(OrderForm, self).clean()

        data = self.cleaned_data
        errors = []

        # At least one package size must be given
        if not data.get("packages_s") and not data.get("packages_m") and not data.get("packages_l"):
            logger.info("Customer didn't supply package details.")
            errors.append(ValidationError(_("Bitte gib die Größe deiner Sendung an.")))

        # Dropoff must be after pickup
        pickup_time = data.get("timeframe_pickup")
        dropoff_time = data.get("timeframe_dropoff")

        if all([str(s).isdigit() for s in [pickup_time, dropoff_time]]) and pickup_time > dropoff_time:
            logger.info("Customer wants us to travel back in time.")
            errors.append(ValidationError(_(
                mark_safe("Zeitreisen können wir leider nicht. Bitte "
                "gib einen Auslieferungszeitraum an, der <strong>nach</strong> "
                "der Abholung liegt."))))

        # if custom time windows are selected, ask user to supply more
        # information
        if self.cleaned_data.get("timeframe_pickup") == 'CUSTOM' \
        and not self.cleaned_data["from_comment"].strip():
            logger.info("Customer wants custom pickup but didn't supply enough info..")
            errors.append(
                ValidationError({'from_comment':
                    _("Du hast eine spezifische Abholzeit ausgewählt. Bitte \
                    erläutere dies näher für uns.")}))

        if self.cleaned_data.get("timeframe_dropoff") == 'CUSTOM' \
        and not self.cleaned_data["to_comment"].strip():
            logger.info("Customer wants custom dropoff but didn't supply enough info.")
            errors.append(
                ValidationError({'to_comment':
                    _("Du hast eine spezifische Auslieferungszeit ausgewählt. \
                    Bitte erläutere dies näher für uns.")}))



        if errors:
            raise ValidationError(errors)

        # Recalculate everything based on current data in case the user made
        # changes to the form data after the price has been calculated.
        self.instance.get_directions()
        self.instance.calculate_price()

        return self.cleaned_data

class OrderAdminForm(forms.ModelForm):
    model = Order

    def clean(self):
        if self.cleaned_data.get("status") == 'CONFIRMED' and not self.cleaned_data.get("ecourier_id"):
            raise ValidationError(_("Der Auftrag kann nicht bestätigt \
                werden, solange keine Tournummer aus eCourier angegeben wurde."))
