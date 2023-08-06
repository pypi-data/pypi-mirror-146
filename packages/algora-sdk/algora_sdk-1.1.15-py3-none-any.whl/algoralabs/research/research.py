from algoralabs.common.requests import __get_request
from algoralabs.decorators.data import data_request


@data_request(transformer=lambda data: data)
def get_research(id: str):
    endpoint = f"research-service/research/{id}"
    return __get_request(endpoint)
