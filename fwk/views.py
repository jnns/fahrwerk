from django.conf import settings
from django.shortcuts import get_object_or_404, render_to_response
from django.views.generic import CreateView, DetailView

from formtools.wizard.views import SessionWizardView

from .models import Order, hashids
from . import forms



FORMS = [
    ("order", forms.OrderForm),
    ("confirmation", forms.OrderConfirmation)
]

TEMPLATES = {
    "order": "fwk/order_form.html",
    "confirmation": "fwk/order_confirmation.html"
}



class OrderWizardView(SessionWizardView):

    def get_template_names(self):
        return [TEMPLATES[self.steps.current]]

    def get_context_data(self, form, **kwargs):
        context = super(OrderWizardView, self).get_context_data(form=form, **kwargs)
        if self.steps.current == 'confirmation':
            context.update({'order': Order(**self.get_cleaned_data_for_step("order"))})
        return context

    def done(self, form_list, form_dict, **kwargs):
        form_dict["order"].save()

        return render_to_response('fwk/done.html', {
            'form_data': [form.cleaned_data for form in form_list],
            'our_phone_no': settings.FWK_PHONE_NO
        })



class OrderCreateView(CreateView):
    model = Order
    form_class = forms.OrderForm



class OrderStatusView(DetailView):
    model = Order

    def get_object(self, queryset=None):
        hash_id = self.kwargs.get("id")
        pk = hashids.decode(hash_id)
        return get_object_or_404(self.model, pk=pk[0])
