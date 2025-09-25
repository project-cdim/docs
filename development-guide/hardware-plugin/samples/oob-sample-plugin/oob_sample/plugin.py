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

"""OOB sample plugin."""

import datetime
from contextlib import contextmanager
from dataclasses import dataclass
from typing import Iterator, Any

from app.common.basic_exceptions import RequestNotSupportedHWControlError, InternalHWControlError
from app.common.utils.oob_plugin_base import OOBPluginBase, OOBDeviceListItem
from . import restclt, redfish, devicefinder, deviceops


@dataclass
class OOBSamplePluginConfig:
    """OOB sample plugin configuration."""

    base_url: str
    timeout_sec: float
    manager_uri: str


class OOBSamplePlugin(OOBPluginBase):
    """OOB sample plugin."""

    def __init__(self, specific_data: Any = None) -> None:
        super().__init__(specific_data)
        self.config = self._get_config()

    def get_device_info(self) -> list[OOBDeviceListItem]:
        with self._create_redfish_client() as client:
            result: list[OOBDeviceListItem] = []

            for device_finder in self._all_device_finders():
                result.extend(device_finder.get_device_info(client))

            return result

    def get_spec_info(self, key_values: list[dict[str, str]]) -> dict[str, list[dict]]:
        with self._create_redfish_client() as client:
            spec_info_list: list[dict] = []
            result: dict[str, Any] = {"devices": spec_info_list}

            for oob_device_id, device_type in self._for_all_devices(key_values):
                schema, link = self._device_operations_for(device_type).get_spec_info(client, oob_device_id)
                spec_info_list.append(
                    {
                        "deviceID": oob_device_id,
                        "type": device_type,
                        "schema": schema,
                        "link": link,
                        "time": self._current_datetime(),
                    }
                )

            return result

    def get_metric_info(self, key_values: list[dict[str, str]]) -> dict[str, list[dict]]:
        with self._create_redfish_client() as client:
            metric_info_list: list[dict] = []
            result: dict[str, Any] = {"devices": metric_info_list}

            for oob_device_id, device_type in self._for_all_devices(key_values):
                schema, metric, environment = self._device_operations_for(device_type).get_metric_info(
                    client, oob_device_id
                )
                metric_info_list.append(
                    {
                        "deviceID": oob_device_id,
                        "type": device_type,
                        "schema": schema,
                        "metric": metric,
                        "environment": environment,
                        "time": self._current_datetime(),
                    }
                )

            return result

    def get_power_state(self, key_values: list[dict[str, str]]) -> dict[str, list[dict]]:
        with self._create_redfish_client() as client:
            power_states: list[dict] = []
            result: dict[str, Any] = {"devices": power_states}

            for oob_device_id, device_type in self._for_all_devices(key_values):
                power_state = self._device_operations_for(device_type).get_power_state(client, oob_device_id)
                power_states.append(
                    {
                        "deviceID": oob_device_id,
                        "type": device_type,
                        "powerState": power_state,
                        "time": self._current_datetime(),
                    }
                )

            return result

    def post_power_on(self, key_values: list[dict[str, str]]) -> dict[str, list[dict]]:
        with self._create_redfish_client() as client:
            status_list: list[dict] = []
            result: dict[str, Any] = {"devices": status_list}

            for oob_device_id, device_type in self._for_all_devices(key_values):
                status = self._device_operations_for(device_type).power_on(client, oob_device_id)
                status_list.append(
                    {
                        "deviceID": oob_device_id,
                        "type": device_type,
                        "status": status,
                        "time": self._current_datetime(),
                    }
                )

            return result

    def post_power_off(self, key_values: list[dict[str, str]]) -> dict[str, list[dict]]:
        with self._create_redfish_client() as client:
            status_list: list[dict] = []
            result: dict[str, Any] = {"devices": status_list}

            for oob_device_id, device_type in self._for_all_devices(key_values):
                status = self._device_operations_for(device_type).power_off(client, oob_device_id)
                status_list.append(
                    {
                        "deviceID": oob_device_id,
                        "type": device_type,
                        "status": status,
                        "time": self._current_datetime(),
                    }
                )

            return result

    def post_cpu_reset(self, key_values: list[dict[str, str]]) -> dict[str, list[dict]]:
        with self._create_redfish_client() as client:
            status_list: list[dict] = []
            result: dict[str, Any] = {"devices": status_list}

            for oob_device_id, device_type in self._for_all_devices(key_values):
                status = self._device_operations_for(device_type).reset(client, oob_device_id)
                status_list.append(
                    {
                        "deviceID": oob_device_id,
                        "type": device_type,
                        "status": status,
                        "time": self._current_datetime(),
                    }
                )

            return result

    def post_os_shutdown(self, key_values: list[dict[str, str]]) -> dict[str, list[dict]]:
        with self._create_redfish_client() as client:
            status_list: list[dict] = []
            result: dict[str, Any] = {"devices": status_list}

            for oob_device_id, device_type in self._for_all_devices(key_values):
                status = self._device_operations_for(device_type).shutdown_os(client, oob_device_id)
                status_list.append(
                    {
                        "deviceID": oob_device_id,
                        "type": device_type,
                        "status": status,
                        "time": self._current_datetime(),
                    }
                )

            return result

    # ------------------------------------------------------------
    # DeviceFinder / DeviceOperations
    # ------------------------------------------------------------
    def _all_device_finders(self) -> Iterator[devicefinder.DeviceFinder]:
        for device_finder_class in (
            devicefinder.ProcessorFinder,
            devicefinder.MemoryFinder,
            devicefinder.StorageFinder,
            devicefinder.NetworkInterfaceFinder,
            devicefinder.GraphicControllerFinder,
        ):
            yield device_finder_class(self.config.manager_uri)

    _DEVICE_OPERATIONS_BY_DEVICE_TYPE = {
        "CPU": deviceops.CPUOperations,
        "GPU": deviceops.GPUOperations,
        "memory": deviceops.MemoryOperations,
        "storage": deviceops.StorageOperations,
        "networkInterface": deviceops.NetworkInterfaceOperations,
        "graphicController": deviceops.GraphicControllerOperations,
    }

    def _device_operations_for(self, device_type: str) -> deviceops.DeviceOperations:
        if device_ops_class := OOBSamplePlugin._DEVICE_OPERATIONS_BY_DEVICE_TYPE.get(device_type):
            return device_ops_class(self.config.manager_uri)
        raise RequestNotSupportedHWControlError

    # ------------------------------------------------------------
    # Utilities
    # ------------------------------------------------------------
    def _get_config(self) -> OOBSamplePluginConfig:
        if not isinstance(self.specific_data, dict):
            raise InternalHWControlError(additional_message="specific_data is not dictionary.")
        return OOBSamplePluginConfig(
            base_url=self.specific_data["base_url"],
            timeout_sec=float(self.specific_data["timeout_sec"]),
            manager_uri=self.specific_data["manager_uri"],
        )

    def _current_datetime(self) -> str:
        return datetime.datetime.now(datetime.UTC).strftime("%Y-%m-%dT%H:%M:%SZ")

    @contextmanager
    def _create_redfish_client(self) -> Iterator[redfish.Client]:
        rest_client = restclt.RestClient(self.config.base_url, self.config.timeout_sec)
        redfish_client = redfish.Client(rest_client)
        try:
            yield redfish_client
        finally:
            redfish_client.close()

    def _for_all_devices(self, key_values: list[dict[str, str]]) -> Iterator[tuple[str, str]]:
        yield from ((m["oob_device_id"], m["device_type"]) for m in key_values)
