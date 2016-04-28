"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin
from django.views.i18n import javascript_catalog

from fwk.views import OrderWizardView, FORMS
from fwk.api import price

js_info_dict = {
    'domain': 'djangojs',
    'packages': ('fwk',),
}

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    #url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    #url(r'^(?P<id>[A-z0-9]{4,})$', OrderStatusView.as_view(), name="order_status"),
    url(r'^api/v1/price/$', price , name="price"),
    #url(r'^language/$', change_language, name="language")
]

urlpatterns += i18n_patterns(
    url(r'^jsi18n/$', javascript_catalog, js_info_dict, name='javascript-catalog'),
    url(r'^$', OrderWizardView.as_view(FORMS), name="order"),
)