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

"""
REST API client.
"""

import requests

from app.common.basic_exceptions import InternalHwControlError


class RestClient:
    """REST API client."""

    def __init__(self, base_url: str, timeout: float) -> None:
        """Construct REST API client.

        Args:
            base_url: base URL used as prefix of request URL
            timeout: connect / read timeout [sec]
        """
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.session = requests.Session()
        self.session.trust_env = False

    def close(self) -> None:
        """Close the REST API session."""
        self.session.close()

    def get(self, uri: str, params: dict | None = None) -> dict:
        """Send an GET request.

        Args:
            uri: request URI (the base_url is prepended)
            params: query parameters
        Returns:
            response body
        """
        return self._request("GET", uri, params=params).json()

    def post(self, uri: str, data: dict, params: dict | None = None) -> int:
        """Send a POST request.

        Args:
            uri: request URI (the base_url is prepended)
            data: request body
            params: query parameters
        Returns:
            HTTP status code
        """
        return self._request("POST", uri, data=data, params=params).status_code

    def _request(
        self, method: str, uri: str, data: dict | None = None, params: dict | None = None
    ) -> requests.Response:
        url = self.base_url + "/" + uri.lstrip("/")
        try:
            response = self.session.request(method, url, json=data, params=params, timeout=self.timeout)
            response.raise_for_status()
            return response
        except requests.exceptions.RequestException as exc:
            raise InternalHwControlError(additional_message=f"Failed to {method} {url}") from exc
