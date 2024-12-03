from rdflib import URIRef, Literal

from django.core.validators import URLValidator
from django.core.exceptions import ValidationError


class TriplePatternQuery(object):

    def __init__(self, page, subject, predicate, obj):
        """Turn http parameters into a triple pattern query object using RDFlib objects."""
        self.page = int(page)
        self.subject = URIRef(subject) if subject else None
        self.predicate = URIRef(predicate) if predicate else None
        self.obj = URIRef(obj) if obj else None
        if self.obj is not None:
            validator = URLValidator()
            try:
                validator(self.obj)
                self.obj = URIRef(self.obj)
            except ValidationError:
                self.obj = string_to_literal(self.obj, validator)


def string_to_literal(string, urlvalidator):
    splited_literal = string.split('"')
    value = splited_literal[1]
    datatype = splited_literal[2].split('^^')[1] if splited_literal[2] else None
    try:
        urlvalidator(datatype)
        datatype = URIRef(datatype)
    except ValidationError:
        datatype = None
    return Literal(value, datatype=datatype)
