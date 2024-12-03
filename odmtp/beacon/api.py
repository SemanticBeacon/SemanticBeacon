import json
import urllib.request
from urllib.error import HTTPError
from dotenv import load_dotenv
import os
load_dotenv()

API_ENDPOINT = os.getenv("BEACON_API_URL", "mysecretkey")
RESULTS_PER_PAGE = 100

class ClientException(Exception):
    pass

class Payload:
    """Class to build and manage payload parameters incrementally."""
    def __init__(self):
        self.payload = {
            "meta": {
                "apiVersion": "2.0"
            },
            "query": {
                "requestParameters": {},  # Empty by default
                "filters": [],
                "includeResultsetResponses": "HIT",
                "pagination": {
                    "skip": 0,
                    "limit": RESULTS_PER_PAGE
                },
                "testMode": False,
                "requestedGranularity": "record"
            }
        }

    def set_start(self, start):
        """Set the start parameter for the query."""
        self.payload["query"]["requestParameters"]["start"] = [ start ]

    def set_end(self, end):
        """Set the end parameter for the query."""
        self.payload["query"]["requestParameters"]["end"] = [ end ]

    def set_variant_type(self, variant_type):
        """Set the variant type parameter for the query."""
        self.payload["query"]["requestParameters"]["variantType"] = variant_type

    def set_alternate_bases(self, alternate_bases):
        """Set the alternateBases parameter for the query."""
        self.payload["query"]["requestParameters"]["alternateBases"] = alternate_bases

    def set_reference_bases(self, reference_bases):
        """Set the referenceBases parameter for the query."""
        self.payload["query"]["requestParameters"]["referenceBases"] = reference_bases

    def set_aminoacid_change(self, aminoacid_change):
        """Set the aminoacidChange parameter for the query."""
        self.payload["query"]["requestParameters"]["aminoacidChange"] = aminoacid_change

    def set_variant_min_length(self, variant_min_length):
        """Set the variantMinLength parameter for the query."""
        self.payload["query"]["requestParameters"]["variantMinLength"] = variant_min_length

    def set_variant_max_length(self, variant_max_length):
        """Set the variantMaxLength parameter for the query."""
        self.payload["query"]["requestParameters"]["variantMaxLength"] = variant_max_length

    def set_gene_id(self, gene_id):
        """Set the geneId parameter for the query."""
        self.payload["query"]["requestParameters"]["geneId"] = gene_id

    def set_pagination(self, skip=None, limit=None):
        """Set pagination parameters."""
        if skip is not None:
            self.payload["query"]["pagination"]["skip"] = skip
        if limit is not None:
            self.payload["query"]["pagination"]["limit"] = limit

    def build(self):
        """Return the current state of the payload."""
        return self.payload


class BeaconApi:
    """This class implements POST requests with customizable payloads."""

    def __init__(self, access_token=""):
        self.access_token = access_token
        self.payload_builder = Payload()

    def set_start(self, start):
        """Set the start parameter in the payload."""
        self.payload_builder.set_start(start)

    def set_end(self, end):
        """Set the end parameter in the payload."""
        self.payload_builder.set_end(end)

    def set_variant_type(self, variant_type):
        """Set the variant type in the payload."""
        self.payload_builder.set_variant_type(variant_type)

    def set_alternate_bases(self, alternate_bases):
        """Set the alternateBases in the payload."""
        self.payload_builder.set_alternate_bases(alternate_bases)

    def set_reference_bases(self, reference_bases):
        """Set the referenceBases in the payload."""
        self.payload_builder.set_reference_bases(reference_bases)

    def set_aminoacid_change(self, aminoacid_change):
        """Set the aminoacidChange in the payload."""
        self.payload_builder.set_aminoacid_change(aminoacid_change)

    def set_variant_min_length(self, variant_min_length):
        """Set the variantMinLength in the payload."""
        self.payload_builder.set_variant_min_length(variant_min_length)

    def set_variant_max_length(self, variant_max_length):
        """Set the variantMaxLength in the payload."""
        self.payload_builder.set_variant_max_length(variant_max_length)

    def set_gene_id(self, gene_id):
        """Set the geneId in the payload."""
        self.payload_builder.set_gene_id(gene_id)

    def set_pagination(self, skip=None, limit=None):
        """Set pagination for the payload."""
        self.payload_builder.set_pagination(skip, limit)

    def post_request(self, url=API_ENDPOINT):
        """Send a POST request with the current payload."""
        headers = {
            "Content-Type": "application/json",
        }

        if self.access_token:
            headers["Authorization"] = f"Bearer {self.access_token}"

        params = self.payload_builder.build()
        # print(f"POST request to {url} with payload: {params}")

        data = json.dumps(params).encode('utf-8')
        request = urllib.request.Request(url, data=data, headers=headers, method="POST")

        try:
            response = urllib.request.urlopen(request)
            raw_data = response.read().decode("utf-8")
            return json.loads(raw_data)
        except HTTPError as e:
            raise ClientException(f"POST request failed with status: {e.code}, message: {e.reason}")
