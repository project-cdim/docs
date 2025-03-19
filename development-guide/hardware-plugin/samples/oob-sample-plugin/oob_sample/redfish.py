# Copyright 2025 NEC Corporation
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
#  under the License.

"""Redfish client and response objects."""

from typing import Any, Iterator

from app.common.basic_exceptions import RequestNotSupportedHwControlError
from . import restclt


_ODATA_ID = "@odata.id"


class Resource:
    """Redfish resource."""

    def __init__(self, data: dict[str, Any]) -> None:
        """Initialize Redfish resource.

        Args:
            data: Redfish response.
        """
        self.data = data

    def __str__(self) -> str:
        return self.data.__str__()

    def __repr__(self) -> str:
        return self.data.__repr__()

    def as_dict(self) -> dict[str, Any]:
        """Get Redfish resource as dictionary."""
        return self.data

    def prop(self, path: str) -> Any | None:
        """Get the property if it exists.

        Args:
            path: slash-separated property path
        Returns:
            property value if it exists or None otherwise
        """
        return _get_if_exists(self.data, path)

    def link(self, path: str) -> str | None:
        """Get the link of a property if it exists.

        Args:
            path: slash-separated property path
        Returns:
            the link (uri named @odata.id) of the property if it exists or None otherwise
        """
        prop = self.prop(path)
        if isinstance(prop, dict):
            return _get_if_exists(prop, _ODATA_ID)
        return None

    def all_links(self, path: str) -> Iterator[str]:
        """Get all links of a property.

        Args:
            path: slash-separated property path referring list
        Returns:
            the links (uri named @odata.id) of the property
        """
        links = self.prop(path)
        if isinstance(links, list):
            for link in links:
                if uri := _get_if_exists(link, _ODATA_ID):
                    yield uri

    def first_link(self, path: str) -> str | None:
        """Get the first link of a property if it exists.

        Args:
            path: slash-separated property path
        Returns:
            the first link (uri named @odata.id) of the property if it exists or None otherwise
        """
        return next(self.all_links(path), None)

    def action_target(self, resource_type: str, action_name: str) -> str | None:
        """Get the action target if it exists.

        Args:
            resource_type: resource type (Processor, Memory, ...)
            action_name: action name (Reset, ...)
        Returns:
            the action target (uri) if it exists or None otherwise
        """
        return self.prop(f"Actions/#{resource_type}.{action_name}/target")

    def action_values_allowable(self, resource_type: str, action_name: str, value_type: str, *values: str) -> bool:
        """Check whether or not the action allows all values.

        Args:
            resource_type: resource type (Processor, Memory, ...)
            action_name: action name (Reset, ...)
            value_type: type of action value (ResetType, ....)
            values: action values to check
        Returns:
            True if all values are allowed, False otherwise
        """
        allowable_values = self.prop(f"Actions/#{resource_type}.{action_name}/{value_type}@Redfish.AllowableValues")
        if isinstance(allowable_values, list):
            return set(values).issubset(set(allowable_values))
        return False


class ResourceCollection:
    """Redfish resource collection."""

    def __init__(self, data: dict[str, Any]) -> None:
        """Initialize Redfish resource collection.

        Args:
            data: Redfish response.
        """
        self.data = data

    def __str__(self) -> str:
        return self.data.__str__()

    def __repr__(self) -> str:
        return self.data.__repr__()

    def all_links(self) -> Iterator[str]:
        """Get all links (uri named @odata.id) of the "Members"."""
        members = _get_if_exists(self.data, "Members")
        if isinstance(members, list):
            for member in members:
                if uri := _get_if_exists(member, _ODATA_ID):
                    yield uri


def _get_if_exists(mapping: dict[str, Any], path: str) -> Any:
    """Return dictionary value if it exists.

    The path is slash-separated dictionary keys.
    The dict value is retrieved as like mapping.get(keys[0], {}).get(keys[1], {})...
    The dict value is considered to exist if all keys exist and it is not None,
    an empty dict, an empty list, an empty tuple, an empty string or whitespace.
    If list or tuple is not last entry, its first element is used.

    Args:
        mapping: dictionary to retrieve value
        path: slash-separated dictionary keys

    Returns:
        the dictionary value or None
    """

    def _is_none_or_blank(v: Any) -> bool:
        """Return true if the value is None, empty or whitespace."""
        if not v:
            return not isinstance(v, int | float | bool)  # 0, 0.0, False
        return isinstance(v, str) and v.isspace()

    keys = path.split("/")
    last_key = keys[-1]
    value: Any = mapping
    for key in keys:
        value = value.get(key)
        if _is_none_or_blank(value):
            return None
        if key is not last_key and isinstance(value, list | tuple):
            value = value[0]

    return value


class Client:
    """Redfish client."""

    def __init__(self, client: restclt.RestClient) -> None:
        """Initialize Redfish client.

        Args:
            client: REST API client
        """
        self.client = client

    def close(self) -> None:
        """Close Redfish connection."""
        self.client.close()

    def get_resource(self, uri: str) -> Resource:
        """Get resource by URI.

        Args:
            uri: resource URI
        Returns:
            resource
        """
        return Resource(self.client.get(uri))

    def get_collection(self, uri: str) -> ResourceCollection:
        """Get resource collection by URI.

        Args:
            uri: resource collection URI
        Returns:
            resource collection
        """
        return ResourceCollection(self.client.get(uri))

    def find_all_resources_in_collection(self, uri: str) -> Iterator[Resource]:
        """Get all resources in the resource collection.

        Args:
            uri: resource collection URI
        Returns:
            iterator to the resource
        """
        for member_uri in self.get_collection(uri).all_links():
            yield self.get_resource(member_uri)

    def find_first_resource_in_collection(self, uri: str) -> Resource | None:
        """Get the first resource in the resource collection.

        Args:
            uri: resource collection URI
        Returns:
            first resource if it exists or None otherwise
        """
        if member_uri := next(self.get_collection(uri).all_links(), None):
            return self.get_resource(member_uri)
        return None

    def find_resource_in_collection(self, uri: str, resource_id: str) -> Resource | None:
        """Find resource in the resource collection.

        Args:
            uri: resource collection URI
            resource_id: resource ID (last element of the resource URI)
        Returns:
            resource if it exists or None otherwise
        """
        for member_uri in self.get_collection(uri).all_links():
            if member_uri.endswith(f"/{resource_id}"):
                return self.get_resource(member_uri)
        return None

    def do_action(self, resource: Resource, resource_type: str, action_name: str, data: dict) -> int:
        """Do the action.

        Args:
            resource: target of the action
            resource_type: resource type (Processor, Memory, ...)
            action_name: action name (Reset, ...)
            data: request body
        Returns:
            response status code
        """
        if action_uri := resource.action_target(resource_type, action_name):
            return self.client.post(action_uri, data)
        raise RequestNotSupportedHwControlError
