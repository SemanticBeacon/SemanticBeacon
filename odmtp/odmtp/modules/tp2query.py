from tpf.tpq import TriplePatternQuery
from abc import ABC, abstractmethod
from typing import Dict, List

class Tp2QueryResponse():
    def __init__(self, apiUrl, response, nbResults, isLastPage):
        self.apiUrl = apiUrl
        self.response = response
        self.nbResults = nbResults
        self.isLastPage = isLastPage

class Tp2Query(ABC):
    @abstractmethod
    def request(self, tpq: TriplePatternQuery, reverseMapping: Dict[str, List[str]]) -> Tp2QueryResponse:
       raise NotImplementedError("This method should be implemented by the subclass")