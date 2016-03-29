from django.shortcuts import get_object_or_404
from django.views.generic import CreateView, DetailView
from .models import Order, hashids
from .forms import OrderForm

class OrderCreateView(CreateView):
    model = Order
    form_class = OrderForm

class OrderStatusView(DetailView):
    model = Order

    def get_object(self, queryset=None):
        hash_id = self.kwargs.get("id")
        pk = hashids.decode(hash_id)
        return get_object_or_404(self.model, pk=pk[0])
