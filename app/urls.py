from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from app import views


urlpatterns = [
    url(r'^parcels/$', views.ParcelEdit.as_view()),
    url(r'^parcels/(?P<id>[0-9]+)$', views.ParcelEdit.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)