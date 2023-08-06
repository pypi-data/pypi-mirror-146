import json

from algoralabs.common.enum import PermissionRequest
from algoralabs.common.requests import __put_request, __post_request, __get_request, __delete_request
from algoralabs.data.transformations.response_transformers import no_transform
from algoralabs.decorators.data import data_request


@data_request(transformer=no_transform)
def get_permission(id: str):
    endpoint = f"research-service/permission/{id}"
    return __get_request(endpoint)


@data_request(transformer=no_transform)
def get_permission_by_resource_id(resource_id: str):
    endpoint = f"research-service/permission/resource/{resource_id}"
    return __get_request(endpoint)


@data_request(transformer=no_transform)
def get_permissions_by_resource_id(resource_id: str):
    endpoint = f"research-service/permission/resource/{resource_id}/permissions"
    return __get_request(endpoint)


@data_request(transformer=no_transform)
def create_permission(request: PermissionRequest):
    endpoint = f"research-service/permission"
    return __put_request(endpoint, json=json.loads(request.json()))


@data_request(transformer=no_transform)
def update_permission(id: str, request: PermissionRequest):
    endpoint = f"research-service/permission/{id}"
    return __post_request(endpoint, json=json.loads(request.json()))


@data_request(transformer=no_transform)
def delete_permission(id: str):
    endpoint = f"research-service/permission/{id}"
    return __delete_request(endpoint)
