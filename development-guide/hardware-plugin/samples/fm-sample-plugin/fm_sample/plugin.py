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

"""FM sample plugin."""

from contextlib import contextmanager
from dataclasses import dataclass
from typing import Any, Iterator

import requests

from app.common.basic_exceptions import InternalHWControlError
from app.common.utils.fm_plugin_base import FMPluginBase, FMPortData, FMSwitchData


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
            raise InternalHWControlError(additional_message=f"Failed to {method} {url}") from exc


@dataclass
class FMSamplePluginConfig:
    """FM sample plugin configuration."""

    base_url: str
    timeout_sec: float


class FMSamplePlugin(FMPluginBase):
    """FM sample plugin."""

    def __init__(self, specific_data: Any = None) -> None:
        super().__init__(specific_data)
        self.config = self._get_config()

    def connect(self, cpu_id: str, device_id: str) -> None:
        with self._create_rest_client() as client:
            client.post("/connect", {"uid": cpu_id, "did": device_id})

    def disconnect(self, cpu_id: str, device_id: str) -> None:
        with self._create_rest_client() as client:
            client.post("/disconnect", {"uid": cpu_id, "did": device_id})

    def get_port_info(self, target_id: str | None = None) -> dict:
        with self._create_rest_client() as client:
            params = {"target": target_id} if target_id else None
            response = client.get("/portinfo", params=params)
            response["data"] = [FMPortData(**item) for item in response["data"]]
            return response

    def get_switch_info(self, switch_id: str | None = None) -> dict:
        with self._create_rest_client() as client:
            params = {"target": switch_id} if switch_id else None
            response = client.get("/switchinfo", params=params)
            response["data"] = [FMSwitchData(**item) for item in response["data"]]
            return response

    # ------------------------------------------------------------
    # Utilities
    # ------------------------------------------------------------
    def _get_config(self) -> FMSamplePluginConfig:
        if not isinstance(self.specific_data, dict):
            raise InternalHWControlError(additional_message="specific_data is not dictionary.")
        return FMSamplePluginConfig(
            base_url=str(self.specific_data["base_url"]).rstrip("/"),
            timeout_sec=float(self.specific_data["timeout_sec"]),
        )

    @contextmanager
    def _create_rest_client(self) -> Iterator[RestClient]:
        rest_client = RestClient(self.config.base_url, self.config.timeout_sec)
        try:
            yield rest_client
        finally:
            rest_client.close()
