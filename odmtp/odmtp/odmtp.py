from odmtp.modules.tp2query import Tp2Query
from odmtp.modules.mapper import Mapper
from tpf.fragment import Fragment
from tpf.tpq import TriplePatternQuery

class Odmtp(object):

    def __init__(self, tp2query: Tp2Query, mapper: Mapper):
        self.tp2query = tp2query
        self.mapper = mapper

    def match(self, tpq: TriplePatternQuery, request) -> Fragment:

        fragment = Fragment()

        scheme = request.scheme
        host = request.get_host()
        path = request.path  
        tpfBaseUrl = f'{scheme}://{host}{path}'

        tpResp = self.tp2query.request(tpq, self.mapper.get_reverse_mapping())
        convertedGraph = self.mapper.convert(tpResp.response)
        
        # Debugging
        # print(convertedGraph.serialize(format='turtle'))
        #for subject, predicate, obj in convertedGraph:
          # print(f"P: {predicate}")

        # Filter the triples to keep only the ones we requested
        filteredGraph = []
        
        for subject, predicate, obj in convertedGraph:
            match = True
            # Check if the triple matches the TPQ query
            # if S is a variable then p and o should be the same as the TPQ 
            # if P is a variable then s and o should be the same as the TPQ
            # etc...
            if tpq.subject is not None and tpq.subject != subject:
                match = False
            if tpq.predicate is not None and tpq.predicate != predicate:
                match = False
            if tpq.obj is not None and tpq.obj != obj:
                match = False
            if match:
                filteredGraph.append((subject, predicate, obj))

        nbOfTriples = len(filteredGraph)

        #print(f"Number of triples: {nbOfTriples}")
        #print(f"API number of responses (variants): {tpResp.nbResults}")

        fragment._frament_fill_meta(tpq, 
                                    tpResp.apiUrl, 
                                    tpResp.isLastPage, 
                                    tpResp.nbResults, 
                                    nbOfTriples,
                                    request,
                                    tpfBaseUrl)

        for subject, predicate, obj in filteredGraph:
            fragment.add_data_triple(subject, predicate, obj)

        return fragment

