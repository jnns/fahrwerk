# api.py

from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.renderers import JSONRenderer

from .models import Order

@api_view(["GET"])
def price(request):
	distance = request.GET.get("distance")

	if not distance:
		return HttpResponse("Error: No distance specified")

	o = Order(
		distance=distance,
		packages_s=request.GET.get("s"),
		packages_m=request.GET.get("m"),
		packages_l=request.GET.get("l")
	)
	price = o.calculate_price()
	print ("%s km @ %s-%s-%s Pakete = %s" % (
		o.distance,
		o.packages_s,
		o.packages_m,
		o.packages_l,
		price
	))
	return HttpResponse(JSONRenderer().render(price))
