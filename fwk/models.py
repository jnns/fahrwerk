# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.db import models
from datetime import time
from django.utils import timezone

# Rates. Hard defined here. I'm not sure yet wether they should be stored in
# the database or not but some constants are needed one way or the other
# because they're needed in the rate calculation method.
RATE_BIKE = 'bike'
RATE_CARGO = 'cargo'
RATE_PKW = 'pkw'
RATE_KOMBI = 'kombi'
RATE_TRANSPORTER = 'transporter'

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

class Rate(models.Model):
	"""
	This model represents a delivery rate for different modes of
	transportation or particular transportation options.

	Think cargo- or electric car rates.
	"""

	# Keep field definitions clean because this gets repeated a lot
	DECIMAL_KWARGS = {'max_digits': 4, 'decimal_places': 2}

	name = models.CharField(max_length=30, unique=True)
	price_base =  models.DecimalField('Grundpreis',
		help_text="Der Grundpreis für eine Abholung bzw. den ersten Kilometer.",
		**DECIMAL_KWARGS
		)
	price_per_km = models.DecimalField('Preis pro Km',
		help_text="Der Preis pro gefahrenen Kilometer.",
		**DECIMAL_KWARGS
		)
	price_priority = models.DecimalField('Zuschlag',
		help_text='Wird derzeit noch nicht verwendet',
		null=True,
		editable=False,
		**DECIMAL_KWARGS
		)
	tax = models.DecimalField('MwSt.',
		default=1.19,
		blank=True,
		help_text='Optional; standardmäßig 19 %.',
		**DECIMAL_KWARGS
		)

	class Meta:
		verbose_name = 'Tarif'
		verbose_name_plural = 'Tarife'

	def __unicode__(self):
		return self.name



class Order(models.Model):
	"""
	A model which stores all orders that are submitted via the online form.
	They are stored and not just send via email to be able to log them, change
	the status, delete them.

	In the future, they will eventually be transferable to eCourier via API.
	"""
	HOUR_CHOICES = (
		(time(8), ' 8:00 –  9:00'),
		(time(9), ' 9:00 – 10:00'),
		(time(10), '10:00 – 11:00'),
		(time(11), '11:00 – 12:00'),
		(time(12), '12:00 – 13:00'),
		(time(13), '13:00 – 14:00'),
		(time(14), '14:00 – 15:00'),
		(time(15), '15:00 – 16:00'),
		(time(16), '16:00 – 17:00'),
		(time(17), '17:00 – 18:00'),
		(time(18), '18:00 – 19:00'),
	)

	# Pickup information
	from_person = models.CharField("Ansprechpartner_in", max_length=40)
	from_company = models.CharField("Firma", max_length=40, blank=True)
	from_telephone = models.CharField("Telefonnummer", max_length=20)
	from_street = models.CharField("Straße", max_length=30)
	from_streetnumber = models.CharField("Hausnummer", max_length=5)
	from_zipcode = models.PositiveSmallIntegerField("PLZ")
	from_comment = models.CharField("Bemerkung", max_length=40, blank=True,
		help_text='Gebäude, Stockwerk, o.Ä.')
	timeframe_pickup = models.TimeField("Zeitfenster Abholung", choices=HOUR_CHOICES)

	# Drop-off information
	to_person = models.CharField("Ansprechpartner_in", max_length=40)
	to_company = models.CharField("Firma", max_length=40, blank=True)
	to_telephone = models.CharField("Telefonnummer", max_length=20)
	to_street = models.CharField("Straße", max_length=30)
	to_streetnumber = models.CharField("Hausnummer", max_length=5)
	to_zipcode = models.PositiveSmallIntegerField("PLZ")
	to_comment = models.CharField("Bemerkung", max_length=40, blank=True,
		help_text='Gebäude, Stockwerk, o.Ä.')
	timeframe_dropoff = models.TimeField("Zeitfenster Auslieferung", choices=HOUR_CHOICES)

	# Delivery details
	distance = models.PositiveSmallIntegerField("Distanz", null=True)

	# Package sizes
	package_detail = models.CharField("Was wird transportiert?", max_length=40, blank=True)
	packages_s = models.PositiveSmallIntegerField("Packstücke klein", default=0)
	packages_m = models.PositiveSmallIntegerField("Packstücke mittel", default=0)
	packages_l = models.PositiveSmallIntegerField("Packstücke groß", default=0)

	# Meta information
	ecourier_id = models.PositiveIntegerField("Tournummer", blank=True, null=True,
		help_text='Sobald diese Tour in eCourier übernommen wurde, sollte hier die \
		entsprechende Tournummer hinterlegt sein.')
	status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=STATUS_CHOICES[0][0])
	ordered = models.DateTimeField("Bestelldatum", auto_now_add=True)
	delivered = models.DateTimeField("Auslieferungsdatum", blank=True, null=True)
	ip_addr = models.GenericIPAddressField("IP-Adresse", blank=True, null=True)

	class Meta:
		verbose_name = "Bestellung"
		verbose_name_plural = "Bestellungen"

	def __unicode__(self):
		return "%s → %s" % (self.from_street, self.to_street)

	def pickup_short(self):
		return "%s %s %s" % (self.from_street, self.from_streetnumber, self.from_zipcode)

	def dropoff_short(self):
		return "%s %s %s" % (self.to_street, self.to_streetnumber, self.to_zipcode)

	def distance_display(self):
		return "%s 	km" % self.distance

	def rate(self):
		"""
		Returns the rate for the current order, i.e. which means of
		transportation are apropriate to deliver the packages.
		"""

		# Package sizes as I would define them are as follows:
		#
		# S:
		#	very small objects in the size of a keychain, a small (!) dentists
		# 	bag or an envelope
		# M:
		#	objects of the size of a 'Leitz' binder
		#
		# L:
		# 	objects the size of moving boxes and the like
		S, M, L = self.packages_s, self.packages_m, self.packages_l

		if S > 25:
			return RATE_CARGO
		# There's probably no amount of small packages that requires
		# transportation with a car instead of a cargo bike, so skip that
		# condition.

		if M > 3:
			return RATE_CARGO
		if M > 10:
			return RATE_PKW
		if M > 30:
			return RATE_KOMBI
		# As with the small package, I'm to lazy to think of a hard limit for
		# medium packages in a car which would justify a higher rate.

		if L > 3:
			return RATE_KOMBI
		if L > 6:
			return RATE_TRANSPORTER
		return RATE_BIKE

	def save(self, *args, **kwargs):
		# TODO: The actions taking place in this method should be logged in
		# the database

		# automatically update the delivery timestamp
		if self.status == 'DELIVERED' and not self.delivered:
			self.delivered = timezone.now()

		# remove delivery timestamp
		if self.status != 'DELIVERED' and self.delivered:
			self.delivered = None

		super(Order, self).save(*args, **kwargs)



