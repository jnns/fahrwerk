from django.contrib import admin

from .models import *  # NOOP

admin.site.site_header = "Online-Bestellungen"
admin.site.register(Rate)

class OrderAdmin(admin.ModelAdmin):
	model = Order
	list_display = (
		'ecourier',
		'pickup_short',
		'dropoff_short',
		'status',
		'rate',
		'distance_display'
	)
	list_editable = ('status',)

	def ecourier(self, obj):
		if obj.ecourier_id:
			return "#%d" % obj.ecourier_id
	ecourier.short_description = 'Tournr.'


	fieldsets = (
		('Abholung', {
			'fields': (
				('from_person', 'from_company'),
				('from_street', 'from_streetnumber'),
				'from_comment',
				'from_zipcode',
				'timeframe_pickup'
			)
		}),
		('Auslieferung', {
			'fields': (
				('to_person', 'to_company'),
				('to_street', 'to_streetnumber'),
				'to_comment',
				'to_zipcode',
				'timeframe_dropoff'
			)
		}),
		('Sendungsdetails', {
			'fields': (
				'distance',
				'package_detail',
				('packages_s', 'packages_m', 'packages_l')
			)
		}),
		('Meta-Informationen', {
			'fields': (
				'ecourier_id',
				'status',
				'ip_addr',
				'delivered'
			)
		}),
	)
admin.site.register(Order, OrderAdmin)

