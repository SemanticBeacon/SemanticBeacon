from django.urls import path
from . import views
from beacon.views import beacon_tpf, beacon_mapping

urlpatterns = [
    path("", views.hello_world, name="hello_world"),
    path("beacon/query", beacon_tpf, name="test_beacon"),
    path("beacon/mapping", beacon_mapping, name="beacon_mapping")
]
