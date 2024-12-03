import os
from odmtp.odmtp import Odmtp
from odmtp.modules.mapper import Mapper
from beacon.tp2query import Tp2QueryBeacon
from tpf.tpq import TriplePatternQuery
from django.http.response import HttpResponse
from django.views.decorators.http import require_http_methods, require_http_methods
from rdflib import Graph

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MAPPING_PATH = f"{BASE_DIR}/beacon/mapping/mapping_beacon.ttl"

# To avoid creating a new instance of Odmtp for each request, we create a global instance
ODMTP_BEACON = Odmtp(Tp2QueryBeacon(), Mapper(MAPPING_PATH))
print(ODMTP_BEACON.mapper.get_reverse_mapping())

# Beacon API endpoints
@require_http_methods(["GET", "HEAD", "OPTIONS"])
def beacon_tpf(request):

    tpq = TriplePatternQuery(
        request.GET.get("page", "1"),
        request.GET.get("subject"),
        request.GET.get("predicate"),
        request.GET.get("object"),
    )

    fragment = ODMTP_BEACON.match(tpq, request)
    #fragment.output()

    response = HttpResponse(
        fragment.serialize(), content_type="application/trig; charset=utf-8"
    )

    response["Content-Disposition"] = 'attachment; filename="beacon_tpf_fragment.trig"'
    response["Access-Control-Allow-Origin"] = "*"
    response["Access-Control-Allow-Headers"] = "Accept-Datetime,Accept"
    return response

# Mapping endpoint for Beacon API
@require_http_methods(["GET"])
def beacon_mapping(request):
    mapping = Graph().parse(MAPPING_PATH, format="ttl")
    response = HttpResponse(
        mapping.serialize(format="turtle"), content_type="text/turtle; charset=utf-8"
    )
    response["Access-Control-Allow-Origin"] = "*"
    return response
