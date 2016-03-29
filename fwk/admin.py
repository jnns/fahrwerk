# -*- coding: utf-8 -*-

from django.contrib import admin

from .models import *  # NOOP
from .forms import OrderAdminForm

admin.site.site_header = "Online-Bestellungen"
admin.site.register(Rate)

class OrderAdmin(admin.ModelAdmin):
	model = Order
	form = OrderAdminForm
	list_display = (
		'ecourier',
		'pickup_short',
		'dropoff_short',
		'status',
		'rate',
		'distance_display'
	)
	list_editable = ('status',)
	readonly_fields = ('hash',)

	def ecourier(self, obj):
		if obj.ecourier_id:
			return "#%d" % obj.ecourier_id
	ecourier.short_description = 'Tournr.'

	def hash(self, obj):
		return obj.get_hash_id()
	hash.short_description = 'Kennung für Kund_innen'


	fieldsets = (
		('Abholung', {
			'fields': (
				'from_company',
				'from_person',
				'from_phone_no',
				('from_street', 'from_zipcode',),
				'from_comment',
				'timeframe_pickup'
			)
		}),
		('Auslieferung', {
			'fields': (
				'to_company',
				'to_person',
				'to_phone_no',
				('to_street', 'to_zipcode',),
				'to_comment',
				'timeframe_dropoff'
			)
		}),
		('Sendungsdetails', {
			'fields': (
				'package_detail',
				('packages_s', 'packages_m', 'packages_l'),
				'distance',
				'rate',
				'price',
			)
		}),
		('Meta-Informationen', {
			'fields': (
				'ecourier_id',
				'status',
				'ip_addr',
				'delivered',
				'hash',
				'directions_json'
			)
		}),
	)

admin.site.register(Order, OrderAdmin)

