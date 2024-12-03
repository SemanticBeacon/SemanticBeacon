from rdflib import Dataset, Namespace
from rdflib import URIRef, Literal, Namespace, BNode, RDF, XSD
from urllib.parse import urlencode

class Fragment(object):

    HYDRA = Namespace("http://www.w3.org/ns/hydra/core#")
    VOID = Namespace("http://rdfs.org/ns/void#")
    FOAF = Namespace("http://xmlns.com/foaf/0.1/")
    DCTERMS = Namespace("http://purl.org/dc/terms/")

    def __init__(self):
        self.rdf_graph = Dataset()

    def add_data_triple(self, subject, predicate, obj):
        self.rdf_graph.add((subject, predicate, obj))

    def add_graph(self, identifier):
        self.rdf_graph.graph(identifier)

    def add_meta_quad(self, graph, subject, predicate, obj):
        self.rdf_graph.add((graph, subject, predicate, obj))

    def add_prefix(self, prefix, uri):
        self.rdf_graph.bind(prefix, uri)

    def serialize(self):
        return self.rdf_graph.serialize(format="trig", encoding="utf-8")
    
    def output(self):
        # write the fragment to a turtle file
        with open("fragment.ttl", "wb") as f:
            f.write(self.serialize())

    # ============================= DO NOT CHANGE =============================
    def _frament_fill_meta(
        self,
        tpq,
        api_endpoint,
        last_result,
        total_nb_triples,
        nb_triple_per_page,
        request,
        tpf_url,
    ):
        meta_graph = self._tpf_uri(tpf_url, "metadata")
        self.add_graph(meta_graph)
        dataset_base = self._tpf_uri(tpf_url)
        source = URIRef(request.build_absolute_uri())
        dataset_template = Literal(
            "%s%s" % (dataset_base, "{?subject,predicate,object}")
        )
        data_graph = self._tpf_uri(tpf_url, "dataset")
        tp_node = BNode("triplePattern")
        subject_node = BNode("subject")
        predicate_node = BNode("predicate")
        object_node = BNode("object")

        SCHEMA = Namespace("http://schema.org/")
        HYDRA = Namespace("http://www.w3.org/ns/hydra/core#")
        VOID = Namespace("http://rdfs.org/ns/void#")
        FOAF = Namespace("http://xmlns.com/foaf/0.1/")
        DCTERMS = Namespace("http://purl.org/dc/terms/")
        PROV = Namespace("http://www.w3.org/ns/prov#")

        self.add_meta_quad(
            meta_graph, SCHEMA["primaryTopic"], dataset_base, meta_graph
        )
        self.add_meta_quad(data_graph, HYDRA["member"], data_graph, meta_graph)
        self.add_meta_quad(data_graph, RDF.type, VOID["Dataset"], meta_graph)
        self.add_meta_quad(data_graph, RDF.type, HYDRA["Collection"], meta_graph)
        self.add_meta_quad(data_graph, VOID["subset"], dataset_base, meta_graph)
        self.add_meta_quad(
            data_graph, VOID["uriLookupEndpoint"], dataset_template, meta_graph
        )
        self.add_meta_quad(data_graph, HYDRA["search"], tp_node, meta_graph)
        self.add_meta_quad(tp_node, HYDRA["template"], dataset_template, meta_graph)
        self.add_meta_quad(
            tp_node,
            HYDRA["variableRepresentation"],
            HYDRA["ExplicitRepresentation"],
            meta_graph,
        )
        self.add_meta_quad(tp_node, HYDRA["mapping"], subject_node, meta_graph)
        self.add_meta_quad(tp_node, HYDRA["mapping"], predicate_node, meta_graph)
        self.add_meta_quad(tp_node, HYDRA["mapping"], object_node, meta_graph)
        self.add_meta_quad(
            subject_node, HYDRA["variable"], Literal("subject"), meta_graph
        )
        self.add_meta_quad(subject_node, HYDRA["property"], RDF.subject, meta_graph)
        self.add_meta_quad(
            predicate_node, HYDRA["variable"], Literal("predicate"), meta_graph
        )
        self.add_meta_quad(
            predicate_node, HYDRA["property"], RDF.predicate, meta_graph
        )
        self.add_meta_quad(
            object_node, HYDRA["variable"], Literal("object"), meta_graph
        )
        self.add_meta_quad(object_node, HYDRA["property"], RDF.object, meta_graph)

        self.add_meta_quad(dataset_base, VOID["subset"], source, meta_graph)
        self.add_meta_quad(
            source, RDF.type, HYDRA["PartialCollectionView"], meta_graph
        )
        self.add_meta_quad(
            source, DCTERMS["title"], Literal("TPF Test API"), meta_graph
        )
        self.add_meta_quad(
            source,
            DCTERMS["description"],
            Literal(
                "Triples from the beacon api matching the pattern {?s=%s, ?p=%s, ?o=%s}"
                % (tpq.subject, tpq.predicate, tpq.obj)
            ),
            meta_graph,
        )
        self.add_meta_quad(source, DCTERMS["source"], data_graph, meta_graph)

        # ========================== TO VERIFY  ========================== 
        self.add_meta_quad(
            source,
            HYDRA["totalItems"],
            Literal(total_nb_triples, datatype=XSD.int),
            meta_graph,
        )
        self.add_meta_quad(
            source,
            VOID["triples"],
            Literal(total_nb_triples, datatype=XSD.int),
            meta_graph,
        )

        self.add_meta_quad(
            source,
            HYDRA["itemsPerPage"],
            Literal(nb_triple_per_page, datatype=XSD.int),
            meta_graph,
        )
         # ========================== TO VERIFY  ========================== 

        self.add_meta_quad(
            source,
            HYDRA["first"],
            self._tpf_url(dataset_base, 1, tpq.subject, tpq.predicate, tpq.obj),
            meta_graph,
        )

        self.add_meta_quad(source, RDF.type, PROV["Entity"], meta_graph)
        self.add_meta_quad(
            source, PROV["wasDerivedFrom"], URIRef(api_endpoint), meta_graph
        )
        self.add_meta_quad(
            source,
            PROV["wasGeneratedBy"],
            URIRef("https://github.com/your-repo/test-api-tpf"),
            meta_graph,
        )
        if tpq.page > 1:
            self.add_meta_quad(
                source,
                HYDRA["previous"],
                self._tpf_url(
                    dataset_base, tpq.page - 1, tpq.subject, tpq.predicate, tpq.obj
                ),
                meta_graph,
            )
        if not last_result:
            self.add_meta_quad(
                source,
                HYDRA["next"],
                self._tpf_url(
                    dataset_base, tpq.page + 1, tpq.subject, tpq.predicate, tpq.obj
                ),
                meta_graph,
            )
        self.add_prefix("testtfpf", Namespace(tpf_url))
        self.add_prefix("void", VOID)
        self.add_prefix("foaf", FOAF)
        self.add_prefix("hydra", HYDRA)
        self.add_prefix("purl", Namespace("http://purl.org/dc/terms/"))
        self.add_prefix("prov", PROV)
        
    def _tpf_uri(self, tpf_url, tag=None):
        if tag is None:
            return URIRef(tpf_url)
        return URIRef("%s%s" % (tpf_url, tag))

    def _tpf_url(self, dataset_base, page, subject, predicate, obj):
       
        parameters = {"page": page}  # Ensure page parameter is included

        if subject:
            parameters["subject"] = subject

        if predicate:
            parameters["predicate"] = predicate

        if obj:
            if isinstance(obj, URIRef):
                parameters["object"] = str(obj)
            else:
                parameters["object"] = '"%s"^^%s' % (obj, obj._datatype) if hasattr(obj, '_datatype') else str(obj)

        # Construct the URL
        url = dataset_base
        if parameters:
            url += "?" + urlencode(parameters)

        return URIRef(url)
    # ============================= DO NOT CHANGE =============================
