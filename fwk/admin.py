# -*- coding: utf-8 -*-

from django.contrib import admin

from .models import Order, Rate
from .forms import OrderAdminForm

admin.site.site_header = "Online-Bestellungen"

class RateAdmin(admin.ModelAdmin):
	model = Rate
	list_display = (
		'name',
		'price_base',
		'price_per_km',
		'price_service',
		'tax'
	)

admin.site.register(Rate, RateAdmin)

class OrderAdmin(admin.ModelAdmin):
	model = Order
	form = OrderAdminForm
	list_display = (
		'ordered',
		'ecourier',
		'pickup_short',
		'dropoff_short',
		'status',
		'rate',
		'distance_display'
	)
	list_editable = ('status',)
	readonly_fields = ('hash',)
	list_select_related = ('rate',)

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
		('Kundeninformationen', {
			'fields': (
				'customer',
				'customer_email',
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

