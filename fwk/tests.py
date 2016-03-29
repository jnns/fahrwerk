# -*- coding: utf-8 -*-

from django.test import TestCase
from django.contrib.admin.sites import AdminSite
from django.core.validators import ValidationError


from .models import Order
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






