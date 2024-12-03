import logging
import morph_kgc
import tempfile
import os
import json
import re
from rdflib import Graph, Namespace, RDF
from typing import Dict, List
from collections import defaultdict

class Mapper:
    def __init__(self, mapping_path):
        self.mapping_path = mapping_path
        self.reverse_mapping = self.build_reverse_mapping(mapping_path)
        logging.basicConfig(level=logging.WARNING)

    def get_reverse_mapping(self):
        return self.reverse_mapping
        
    def convert(self, json_data):
        if isinstance(json_data, dict):
            json_data = json.dumps(json_data)  # Convert dictionary to JSON string if needed
        
        # Create a temporary file to store the JSON input
        with tempfile.NamedTemporaryFile(delete=False, suffix='.json', mode='w', encoding='utf-8') as temp_json_file:
            temp_json_file.write(json_data)
            temp_json_path = temp_json_file.name

        logging.debug(f"Temporary JSON file created at: {temp_json_path}")
        
        # Prepare the configuration for Morph-KGC
        config = f"""
        [DEFAULT]
        file_path = {temp_json_path}

        [DataSource]
        mappings = {self.mapping_path}
        """

        try:
            # Run Morph-KGC to generate RDF output
            rdf_output = morph_kgc.materialize(config)
            logging.debug("RDF materialization successful.")
            
            # Clean up the temporary file
            os.remove(temp_json_path)

            # Return the RDF graph
            return rdf_output
        except Exception as e:
            logging.error(f"Error during RDF materialization: {e}")
            # Clean up the temporary file in case of an error
            if os.path.exists(temp_json_path):
                os.remove(temp_json_path)
            raise

    def build_reverse_mapping(self, mapping_path) -> Dict[str, List[str]]:
        g = Graph()
        g.parse(mapping_path, format='turtle')

        RR = Namespace("http://www.w3.org/ns/r2rml#")
        RML = Namespace("http://semweb.mmlab.be/ns/rml#")

        predicate_to_source_fields = defaultdict(list)

        for tm in g.subjects(RDF.type, RR.TriplesMap):
            for pom in g.objects(tm, RR.predicateObjectMap):
                predicate = g.value(pom, RR.predicate)
                object_map = g.value(pom, RR.objectMap)
                source_fields = []
                # Check for rml:reference
                reference = g.value(object_map, RML.reference)

                if reference:
                    source_fields.append(str(reference))
                else:
                    template = g.value(object_map, RR.template)
                    if template:
                        # Extract all fields from template
                        fields = re.findall(r'{(.*?)}', str(template))
                        source_fields.extend(fields)

                if predicate and source_fields:
                    predicate_to_source_fields[str(predicate)].extend(source_fields)

        return predicate_to_source_fields
