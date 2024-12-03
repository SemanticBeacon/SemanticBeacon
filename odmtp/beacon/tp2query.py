from odmtp.modules.tp2query import Tp2Query, Tp2QueryResponse
from tpf.tpq import TriplePatternQuery
from beacon.api import BeaconApi, API_ENDPOINT, RESULTS_PER_PAGE
from typing import Dict, List
from rdflib import URIRef, Literal

# Example of reverse mapping for a predicate we can do the following
# {
#     'http://ourlab.org/ressources/ol_hasNumberOfVariants': ['resultsCount'],
#     'http://semanticscience.org/resource/SIO_000219': ['results.variantInternalId'],
#     'http://schema.org/identifier': ['identifiers.genomicHGVSId'],
#     'http://biohackathon.org/resource/faldo#location': ['variation.location.interval.start.value', 'variation.location.interval.end.value'], 
#     'http://biohackathon.org/resource/faldo#reference': ['variation.location.chr'], 
#     'http://purl.obolibrary.org/obo/GENO_0000382': ['variation.referenceBases', 'variation.alternateBases'], 
#     'http://semanticscience.org/resource/SIO_000300': ['referenceBases', 'alternateBases', 'chr'], 
#     'http://biohackathon.org/resource/faldo#position': ['start.value', 'end.value'], 
#     'http://biohackathon.org/resource/faldo#begin': ['start.value'], 
#     'http://biohackathon.org/resource/faldo#end': ['end.value']
# }

# TO IMPROVE
MAPPING_TO_API = {
    'start.value': 'set_start',
    'end.value': 'set_end'
}

class Tp2QueryBeacon(Tp2Query):

    def request(self, tpq : TriplePatternQuery, reverseMapping: Dict[str, List[str]]) -> Tp2QueryResponse:
        page = tpq.page if tpq.page is not None else 1
        offset = (page - 1) * RESULTS_PER_PAGE
        
        api = BeaconApi()
        # ==============================================
        # For now from what we discussed we always search SNP variant
        api.set_pagination(offset, RESULTS_PER_PAGE)
        api.set_variant_type("SNP")
       
        # if tpq.subject:
        #     print(f"Subject {tpq.subject}")
        
        # if tpq.predicate:
        #     print(f"Predicate {tpq.predicate}")

        # if tpq.obj:
        #     print(f"Obj {tpq.obj}")

        # Map the TPQ to the API parameter dynamically using the reverse mapping
        if tpq.predicate and tpq.obj:

            predicate_uri = str(tpq.predicate)
            
            if predicate_uri in reverseMapping:
                if predicate_uri in reverseMapping:
                    source_fields = reverseMapping[predicate_uri]

                if len(source_fields) > 1:
                    for source_field in source_fields:
                        if source_field == "variation.location.interval.start.value" or source_field == "variation.location.interval.end.value":
                            #print(f"TPQ object: {tpq.obj}")
                            # http://ourlab.org/ressources/ol_location16050318_16050319
                            # extract the start and end values from the object
                            if isinstance(tpq.obj, URIRef):
                                location = str(tpq.obj)
                                start_raw, end = location.split("_")[1:]
                                start = start_raw.replace('location', '')
                                api.set_start(int(start))
                                api.set_end(int(end))
                else:
                    source_field = source_fields[0]
                    if source_field in MAPPING_TO_API:
                        method_name = MAPPING_TO_API[source_field]
                        value = self.extract_value(tpq.obj)
                        if value is not None:
                            #print(f"Calling API method {method_name} with value {value}")
                            getattr(api, method_name)(value)
                    else:
                        print(f"No API method mapped for source field {source_field}")
        # ==============================================
        apiResponse = api.post_request(API_ENDPOINT)
        num_total_results = apiResponse.get("responseSummary", {}).get("numTotalResults", 0)

        # Determine if there's more data for pagination
        last_result = (offset + RESULTS_PER_PAGE) >= num_total_results
        return Tp2QueryResponse(API_ENDPOINT, apiResponse, num_total_results, last_result)
    
    def extract_value(self, obj):
        if isinstance(obj, Literal):
            return obj.value
        elif isinstance(obj, URIRef):
            return str(obj)
        elif obj is None:
            return None
        else:
            return str(obj)