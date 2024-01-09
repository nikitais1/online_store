from django.urls import path

from catalog.apps import CatalogConfig
from catalog.views import home, contacts, prod

app_name = CatalogConfig.name

urlpatterns = [
    path('', home, name='home'),
    path('contacts/', contacts, name='contacts'),
    path('prod/<int:pk>', prod, name='prod'),
]
