from algoralabs.common.requests import __get_request, __delete_request
from algoralabs.decorators.data import data_request


@data_request(
    transformer=lambda data: data,
    process_response=lambda response: response.content
)
def get_resource(id: str):
    endpoint = f"research-service/resource/{id}/code"
    return __get_request(endpoint)


def delete_resource(id: str):
    endpoint = f"research-service/resource/{id}"
    return __delete_request(endpoint)
