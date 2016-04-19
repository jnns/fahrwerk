# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import json
import logging
from datetime import time
from decimal import Decimal

from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.core.urlresolvers import reverse
from django.db import models
from django.template.loader import render_to_string
from django.utils import timezone

from hashids import Hashids

from .maps import geocode, directions

logger = logging.getLogger(__name__)

hashids = Hashids(
    min_length=4,
    salt="fwx1312Ac4b",
    # 0,o,l, and 1 are purposefully left out of the alphabet
    alphabet='abcdefghijkmnpqrstuvwxyz23456789')


def validate_phone_no(value):
    error = ValidationError("Bitte gib eine korrekte Telefonnummer ein.")
    number = "".join(
        [s for s in value if s.isdigit()]
    )
    if not 7 <= len(number) <= 15:
        raise error
    if value[0] != "+" and number[0] != "0":
        raise error


STATUS_CHOICES = (
    # The order object is newly created but the client has not yet submitted
    # the form completely. The object has only been created to calculate
    # prices in the backend.
    ('UNFINISHED', '0. unfertig'),

    # The order object is complete but the dispatcher has not yet taken action.
    ('NEW', '1. neu'),

    # The dispatcher confirmed the information with the client.
    ('CONFIRMED', '2. bestätigt'),

    # The package has been picked up by the courier.
    ('PICKED_UP', '3. abgeholt'),

    # The package has been delivered by the courier.
    ('DELIVERED', '4. ausgeliefert'),

    # The order has been canceled because of s reasons.
    ('CANCELED', 'x. storniert'),
)

PAYMENT_CHOICES = (
    ('PICKUP', 'Abholung'),
    ('DROPOFF', 'Auslieferung'),
)

# Keep field definitions clean because this gets repeated a lot
DECIMAL_KWARGS = {'max_digits': 4, 'decimal_places': 2}


class Rate(models.Model):
    """
    This model represents a delivery rate for different modes of
    transportation or particular transportation options.

    Think cargo- or electric car rates.
    """

    # Rates. Hard defined here. I'm not sure yet wether they should be stored in
    # the database or not but some constants are needed one way or the other
    # because they're needed in the rate calculation method.
    RATE_BIKE = 1
    RATE_CARGO = 2
    RATE_PKW = 3
    RATE_KOMBI = 4
    RATE_TRANSPORTER = 5

    name = models.CharField(max_length=30, unique=True)
    price_base =  models.DecimalField('Grundpreis',
        help_text="Der Grundpreis für eine Abholung bzw. den ersten Kilometer.",
        **DECIMAL_KWARGS)
    price_per_km = models.DecimalField('Preis pro Km',
        help_text="Der Preis pro gefahrenen Kilometer.",
        **DECIMAL_KWARGS)
    price_priority = models.DecimalField('Zuschlag',
        help_text='Wird derzeit noch nicht verwendet',
        null=True,
        editable=False,
        **DECIMAL_KWARGS)
    price_service = models.DecimalField('Servicezeit 5 Min',
        **DECIMAL_KWARGS)
    tax = models.DecimalField('MwSt.',
        default=1.19,
        blank=True,
        help_text='Optional; standardmäßig 19 %.',
        **DECIMAL_KWARGS)

    class Meta:
        verbose_name = 'Tarif'
        verbose_name_plural = 'Tarife'
        ordering = ["price_base"]

    def __unicode__(self):
        return self.name

    def price(self, distance=None):
        distance = max(round(Decimal(distance)), 1)

        # German "netto" price
        net = self.price_base + self.price_per_km * Decimal(distance) - self.price_per_km + self.price_service

        # German "brutto" price
        gross = net * self.tax
        price = round(gross, 2)

        logger.info("Price calculated (for %s km): %s EUR" % (distance, price))

        return price



class Order(models.Model):
    """
    A model which stores all orders that are submitted via the online form.
    They are stored and not just send via email to be able to log them, change
    the status, delete them.

    In the future, they will eventually be transferable to eCourier via API.
    """
    HOUR_CHOICES = (
        ('Allgemein', (
            ('ASAP', 'schnellstmöglich'),
            ('CUSTOM', 'spezifisch (bitte Bemerkung hinterlassen)'),
            ('LOW', 'entspannt ("im Laufe des Tages", "während Öffnungszeiten", …)'),
        )),
        ('Konkretes Zeitfenster', (
            ('8', ' 8:00 –  9:00 Uhr'),
            ('9', ' 9:00 – 10:00 Uhr'),
            ('10', '10:00 – 11:00 Uhr'),
            ('11', '11:00 – 12:00 Uhr'),
            ('12', '12:00 – 13:00 Uhr'),
            ('13', '13:00 – 14:00 Uhr'),
            ('14', '14:00 – 15:00 Uhr'),
            ('15', '15:00 – 16:00 Uhr'),
            ('16', '16:00 – 17:00 Uhr'),
            ('17', '17:00 – 18:00 Uhr'),
            ('18', '18:00 – 19:00 Uhr'),
            ('19', '19:00 – 20:00 Uhr'),
        )),
    )

    # Pickup information
    from_person = models.CharField("Ansprechpartner_in", max_length=40)
    from_company = models.CharField("Firma", max_length=40, blank=True)
    from_phone_no = models.CharField("Telefonnummer", max_length=15, validators=[validate_phone_no])
    from_street = models.CharField("Straße und Hausnummer", max_length=30)
    from_zipcode = models.PositiveSmallIntegerField("PLZ")
    from_comment = models.CharField("Bemerkung", max_length=40, blank=True,
        help_text='Gebäude, Stockwerk, o.Ä.')
    timeframe_pickup = models.CharField(max_length=8, verbose_name="Zeitfenster Abholung **", choices=HOUR_CHOICES)

    # Drop-off information
    to_person = models.CharField("Ansprechpartner_in", max_length=40)
    to_company = models.CharField("Firma", max_length=40, blank=True)
    to_phone_no = models.CharField("Telefonnummer", max_length=15, validators=[validate_phone_no])
    to_street = models.CharField("Straße und Hausnummer", max_length=30)
    to_zipcode = models.PositiveSmallIntegerField("PLZ")
    to_comment = models.CharField("Bemerkung", max_length=40, blank=True,
        help_text='Gebäude, Stockwerk, o.Ä.')
    timeframe_dropoff = models.CharField(max_length=8, verbose_name="Zeitfenster Auslieferung **", choices=HOUR_CHOICES)

    # Delivery details
    distance = models.PositiveSmallIntegerField("Distanz", null=True)
    price = models.DecimalField('Preis',
        help_text="Der Preis dieses Auftrags inkl. Mehrwertsteuer. Wird automatisch anhand \
        des Tarifs und der Strecke berechnet, kann aber überschrieben werden.",
        null=True, blank=True,
        **DECIMAL_KWARGS
        )
    rate = models.ForeignKey('fwk.rate', verbose_name="Tarif",
        null=True, blank=True,
        help_text="Der Tarif wird automatisch anhand der Packstücke berechnet, kann \
        aber überschrieben werden.")

    # Package sizes
    package_detail = models.CharField("Was wird transportiert?", max_length=40, blank=True)
    packages_s = models.PositiveSmallIntegerField("Packstücke klein", default=0)
    packages_m = models.PositiveSmallIntegerField("Packstücke mittel", default=0)
    packages_l = models.PositiveSmallIntegerField("Packstücke groß", default=0)

    # Meta information
    ecourier_id = models.PositiveIntegerField("Tournummer", blank=True, null=True,
        help_text='Sobald diese Tour in eCourier übernommen wurde, sollte hier die \
        entsprechende Tournummer hinterlegt sein. Der Status `bestätigt` kann nur \
        dann erteilt werden, wenn eine Tournummer angegeben wurde.')
    status = models.CharField(max_length=10,
        choices=STATUS_CHOICES,
        default=STATUS_CHOICES[0][0],
        blank=True)
    ordered = models.DateTimeField("Bestelldatum", auto_now_add=True)
    delivered = models.DateTimeField("Auslieferungsdatum", blank=True, null=True)
    ip_addr = models.GenericIPAddressField("IP-Adresse", blank=True, null=True)
    customer = models.CharField("Barzahlung bei", max_length=8, choices=PAYMENT_CHOICES,
        default=PAYMENT_CHOICES[0][0])

    # Other
    directions_json = models.TextField("Maps API JSON result", blank=True)



    class Meta:
        verbose_name = "Bestellung"
        verbose_name_plural = "Bestellungen"
        ordering = ["-ordered"]

    def __init__(self, *args, **kwargs):
        super(Order, self).__init__(*args, **kwargs)

        address_info = [
            self.from_street, self.from_zipcode,
            self.to_street, self.to_zipcode
        ]
        if not self.distance and all(address_info):
            try:
                self.get_directions()
            except:
                pass

    def __unicode__(self):
        _from = getattr(self, "from_street", "?")
        _to = getattr(self, "to_street", "?")
        return "%s → %s" % (_from, _to)



    def pickup_short(self):
        return "%s %s" % (self.from_street, self.from_zipcode)

    def dropoff_short(self):
        return "%s %s" % (self.to_street, self.to_zipcode)

    def distance_display(self):
        return "%s  km" % self.distance

    def get_hash_id(self):
        return hashids.encode(self.id)

    def get_absolute_url(self):
        return reverse("order_status", kwargs={'id': self.get_hash_id()})

    def geocode(self, street, zipcode):
        query = "%s, %s" % (street, zipcode)
        return geocode(query)

    def get_directions(self):
        origin = self.geocode(self.from_street, self.from_zipcode)
        destination = self.geocode(self.to_street, self.to_zipcode)
        self.directions_json = directions(origin, destination)

        distance_in_m = json.loads(self.directions_json)['properties']['distance']
        self.distance = Decimal.from_float(round(distance_in_m / 1000.0))
        logger.info("Route has been calculated for %s" % self)

    def calculate_price(self):
        if not self.rate:
            self.rate = Rate.objects.get(pk=self.calculate_rate())
        logger.info("Price has been calculated for %s" % self)
        return self.rate.price(self.distance)

    def calculate_rate(self):
        """
        Returns the rate for the current order, i.e. which means of
        transportation are apropriate to deliver the packages.

        This code relies on database content being available. I doubt this is
        considered best-practice but at the moment it suits the needs best so
        I don't bother for now.
        """

        # Django takes care of type-conversion when data is submitted via a
        # form but when this function is called through the API we must check
        # manually for the correct type.
        def force_int(s):
            try:
                return int(s)
            except TypeError:
                return None

        S = force_int(self.packages_s)
        M = force_int(self.packages_m)
        L = force_int(self.packages_l)

        logger.info("Rate has been calculated for %s" % self)

        # Package sizes as I would define them are as follows:
        #
        # S:
        #   very small objects in the size of a keychain, a small (!) dentists
        #   bag or an envelope
        # M:
        #   objects of the size of a 'Leitz' binder
        #
        # L:
        #   objects the size of moving boxes and the like

        if L > 5:
            return Rate.RATE_TRANSPORTER
        if L > 3 or M > 15:
            return Rate.RATE_KOMBI
        if L > 1 or M > 6:
            return Rate.RATE_PKW
        if L > 0 or M > 2 or S > 10:
            return Rate.RATE_CARGO
        return Rate.RATE_BIKE

    def get_rate_display(self):
        display_values = {
            Rate.RATE_BIKE: 'Fahrrad',
            Rate.RATE_CARGO: 'Lastenrad',
            Rate.RATE_PKW: 'E-PKW',
            Rate.RATE_KOMBI: 'E-Kombi',
            Rate.RATE_TRANSPORTER: 'E-Transporter'
        }
        return display_values[self.calculate_rate()]

    def save(self, *args, **kwargs):
        # TODO: The actions taking place in this method should be logged in
        # the database

        # TODO: Check for the order to be fully qualified by validating it
        # through a form before setting the status to confirmed.

        self.get_directions()

        # automatically set the rate according to the package sizes
        if not self.rate:
            self.rate = Rate.objects.get(id=self.calculate_rate())

        # automatically set the price according to the rate
        if self.rate:
            self.price = self.calculate_price()

        # automatically update the delivery timestamp
        if self.status == 'DELIVERED' and not self.delivered:
            self.delivered = timezone.now()

        # remove delivery timestamp
        if self.status != 'DELIVERED' and self.delivered:
            self.delivered = None

        super(Order, self).save(*args, **kwargs)
        if not self.id:
            logger.info("A new order has been placed: %s" % self)
            context = {
                "order": self,
            }
            subject = "Neue Bestellung: %s" % self
            message = render_to_string("fwk/order_email.txt", context)
            send_mail(subject, message,
                settings.DEFAULT_FROM_EMAIL,
                [settings.DEFAULT_FROM_EMAIL,
                'jvajen+fahrwerk-bestellungen@gmail.com'])



