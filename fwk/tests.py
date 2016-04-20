# -*- coding: utf-8 -*-

from datetime import time

from django.test import TestCase
from django.contrib.admin.sites import AdminSite
from django.core.validators import ValidationError


from .models import Order, Rate
from .admin import OrderAdmin

# Fake a request object and a user object with admin privileges for easier
# testing by not having to go through the whole request-response-cycle.
class MockRequest(object):
	pass

class MockSuperUser(object):
	def has_perm(self, perm):
		return True

request = MockRequest()
request.user = MockSuperUser()


class RateTestCases(TestCase):
	def test_zero_distance(self):
		# Providing a distance of 0 should not result in an error
		data = {'distance': 0, 'rate': Rate.objects.get(pk=1)}
		o = Order(**data)
		self.assertEqual(o.rate.price(), 8.39)




class OrderTestCases(TestCase):
	def test_confirmation(self):
		# It should not be possible to set an Order to confirmed if an
		# eCourier tour number has not yet been assigned.

		data = {'distance': 10, 'status': 'CONFIRMED'}
		ma = OrderAdmin(Order, AdminSite())

		Form = ma.get_form(request)
		form = Form(data)

		self.assertFalse(form.is_valid())
		with self.assertRaises(ValidationError) as exc_info:
			form.clean()

		self.assertTrue('Tournummer' in str(exc_info.exception))

	def test_calculate_rate(self):
		data = {
			'distance': 10,
			'from_person': 'A',
			'from_street': 'A Strasse 1',
			'from_zipcode': 10999,
			'from_phone_no': '+49 000 000000',
			'to_person': 'B',
			'to_street': 'B Strasse 2',
			'to_zipcode': 10999,
			'to_phone_no': '+49 000 000000',
			'packages_s': 0,
			'packages_m': 1,
			'packages_l': 0,
			'timeframe_pickup': "8",
			'timeframe_dropoff': "9",
			'customer': 'PICKUP',
		}
		ma = OrderAdmin(Order, AdminSite())

		Form = ma.get_form(request)
		form = Form(data)

		obj = form.save()
		self.assertTrue(obj.rate is not None)








