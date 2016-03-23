from django.views.generic import CreateView
from .models import Order
from .forms import OrderForm

class OrderCreateView(CreateView):
	model = Order
	form_class = OrderForm