import json
from typing import List

from algoralabs.common.requests import __delete_request, __put_request, __post_request, __get_request
from algoralabs.data.datasets.models import DatasetSearchRequest, DatasetSummaryResponse, DatasetRequest
from algoralabs.data.transformations.response_transformers import no_transform
from algoralabs.decorators.data import data_request


@data_request(transformer=no_transform)
def get_dataset(id: str):
    endpoint = f"data/datasets/dataset/{id}"
    return __get_request(endpoint)


@data_request(transformer=no_transform)
def get_datasets() -> List[DatasetSummaryResponse]:
    endpoint = f"data/datasets/dataset"
    return __get_request(endpoint)


@data_request(transformer=no_transform)
def search_datasets(request: DatasetSearchRequest) -> List[DatasetSummaryResponse]:
    endpoint = f"data/datasets/dataset/search"
    return __post_request(endpoint, json=json.loads(request.json()))


@data_request(transformer=no_transform)
def create_dataset(request: DatasetRequest):
    endpoint = f"data/datasets/dataset"
    return __put_request(endpoint, json=json.loads(request.json()))


@data_request(transformer=no_transform)
def update_dataset(id: str, request: DatasetRequest):
    endpoint = f"data/datasets/dataset/{id}"
    return __post_request(endpoint, json=json.loads(request.json()))


@data_request(transformer=no_transform)
def delete_field(id: str) -> None:
    endpoint = f"data/datasets/field/{id}"
    return __delete_request(endpoint)


@data_request(transformer=no_transform)
def delete_schema(id: str) -> None:
    endpoint = f"data/datasets/schema/{id}"
    return __delete_request(endpoint)


@data_request(transformer=no_transform)
def delete_dataset(id: str) -> None:
    endpoint = f"data/datasets/dataset/{id}"
    return __delete_request(endpoint)
