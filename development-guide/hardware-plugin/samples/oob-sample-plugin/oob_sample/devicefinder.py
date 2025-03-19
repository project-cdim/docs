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

"""Device finder."""

from typing import Any, Iterator

from app.common.utils.oob_plugin_base import OOBDeviceListItem
from . import redfish


class DeviceFinder:
    """Base class of device finder."""

    def __init__(self, manager_uri: str) -> None:
        """Initialize DeviceFinder.

        Args:
            manager_uri: Manager URI (/redfish/v1/Managers/{ManagerId})
        """
        self.manager_uri = manager_uri

    def get_device_info(self, client: redfish.Client) -> Iterator[OOBDeviceListItem]:
        """Find devices and get those identifying information.

        Args:
            client: Redfish client
        Returns:
            Iterator of information to identify device
        """
        for device_id_info in self.find_all_devices(client):
            default_value = {
                "PCIeVendorId": None,
                "PCIeDeviceId": None,
                "PCIeDeviceSerialNumber": None,
                "CPUSerialNumber": None,
                "CPUManufacturer": None,
                "CPUModel": None,
                "portKeys": None,
                "deviceKeys": None,
                "deviceType": "",
                "oobDeviceID": "",
            }
            default_value.update(device_id_info)
            yield OOBDeviceListItem(**default_value)

    def find_all_devices(self, client: redfish.Client) -> Iterator[dict]:  # pylint: disable=unused-argument
        """Find devices and get those identifying information specific to device type.

        Args:
            client: Redfish client
            manager: Manager
        Returns:
            Iterator of device-type specific information to identify device
        """
        yield from ()

    # ------------------------------------------------------------
    # Resource accessors
    # ------------------------------------------------------------
    def all_resources_in_chassis(self, client: redfish.Client, collection_name: str) -> Iterator[redfish.Resource]:
        """Get all resources in Chassis.

        Args:
            client: Redfish client
            collection_name: resource collection name
        Returns:
            Iterator of the resource in Chassis
        """
        manager = client.get_resource(self.manager_uri)
        for chassis_uri in manager.all_links("Links/ManagerForChassis"):
            chassis = client.get_resource(chassis_uri)
            if collection_uri := chassis.link(collection_name):
                yield from client.find_all_resources_in_collection(collection_uri)

    def all_resources_in_computer_system(
        self, client: redfish.Client, collection_name: str
    ) -> Iterator[redfish.Resource]:
        """Get all resources in ComputerSystem.

        Args:
            client: Redfish client
            collection_name: resource collection name
        Returns:
            Iterator of the resource in ComputerSystem
        """
        manager = client.get_resource(self.manager_uri)
        for computer_system_uri in manager.all_links("Links/ManagerForServers"):
            computer_system = client.get_resource(computer_system_uri)
            if collection_uri := computer_system.link(collection_name):
                yield from client.find_all_resources_in_collection(collection_uri)

    def get_pcie_id_info(self, pcie_device: redfish.Resource | None, pcie_function: redfish.Resource | None) -> dict:
        """Get PCIe identifying information as dictionary.

        Args:
            pcie_device: PCIeDevice
            pcie_function: PCIeFunction
        Returns:
            PCIe identifying information dictionary
        """
        result = {}
        if pcie_device:
            if pcie_serial_number := pcie_device.prop("SerialNumber"):
                result["PCIeDeviceSerialNumber"] = pcie_serial_number
        if pcie_function:
            if pcie_vendor_id := pcie_function.prop("VendorId"):
                result["PCIeVendorId"] = pcie_vendor_id.removeprefix("0x")
            if pcie_device_id := pcie_function.prop("DeviceId"):
                result["PCIeDeviceId"] = pcie_device_id.removeprefix("0x")
        return result


class ProcessorFinder(DeviceFinder):
    """Processor finder."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.get_id_info_fn_map = {
            "CPU": self._get_cpu_id_info,
            "GPU": self._get_gpu_id_info,
        }

    def find_all_devices(self, client: redfish.Client) -> Iterator[dict]:
        for processor in self.all_resources_in_chassis(client, "Processors"):
            device_id_info = {
                "deviceKeys": {"SerialNumber": processor.prop("SerialNumber")},
                "deviceType": processor.prop("ProcessorType"),
                "oobDeviceID": processor.prop("Id"),
            }
            if (proc_type := processor.prop("ProcessorType")) and (
                get_id_info_fn := self.get_id_info_fn_map.get(proc_type)
            ):
                device_id_info.update(get_id_info_fn(client, processor))
            yield device_id_info

    def _get_cpu_id_info(
        self, client: redfish.Client, processor: redfish.Resource  # pylint: disable=unused-argument
    ) -> dict[str, Any]:
        return {
            "CPUSerialNumber": processor.prop("SerialNumber"),
            "CPUManufacturer": processor.prop("Manufacturer"),
            "CPUModel": processor.prop("Model"),
        }

    def _get_gpu_id_info(self, client: redfish.Client, processor: redfish.Resource) -> dict[str, Any]:
        pcie_device = None
        pcie_function = None
        if pcie_device_uri := processor.link("Links/PCIeDevice"):
            pcie_device = client.get_resource(pcie_device_uri)
            if pcie_functions_uri := pcie_device.link("PCIeFunctions"):
                pcie_function = client.find_first_resource_in_collection(pcie_functions_uri)
        return self.get_pcie_id_info(pcie_device, pcie_function)


class MemoryFinder(DeviceFinder):
    """Memory finder."""

    def find_all_devices(self, client: redfish.Client) -> Iterator[dict]:
        for memory in self.all_resources_in_chassis(client, "Memory"):
            yield {
                "deviceKeys": {"SerialNumber": memory.prop("SerialNumber")},
                "deviceType": "memory",
                "oobDeviceID": memory.prop("Id"),
            }


class StorageFinder(DeviceFinder):
    """Storage finder."""

    def find_all_devices(self, client: redfish.Client) -> Iterator[dict]:
        for drive in self.all_resources_in_chassis(client, "Drives"):
            device_id_info = {
                "deviceKeys": {"SerialNumber": drive.prop("SerialNumber")},
                "deviceType": "storage",
                "oobDeviceID": drive.prop("Id"),
            }

            pcie_device = None
            pcie_function = None
            if pcie_function_uri := drive.first_link("Links/PCIeFunctions"):
                pcie_function = client.get_resource(pcie_function_uri)
                if pcie_device_uri := pcie_function.link("Links/PCIeDevice"):
                    pcie_device = client.get_resource(pcie_device_uri)
            device_id_info.update(self.get_pcie_id_info(pcie_device, pcie_function))

            yield device_id_info


class NetworkInterfaceFinder(DeviceFinder):
    """NetworkInterface finder."""

    def find_all_devices(self, client: redfish.Client) -> Iterator[dict]:
        for nw_adapter in self.all_resources_in_chassis(client, "NetworkAdapters"):
            device_id_info = {
                "deviceKeys": {"SerialNumber": nw_adapter.prop("SerialNumber")},
                "deviceType": "networkInterface",
                "oobDeviceID": nw_adapter.prop("Id"),
            }

            pcie_device = None
            pcie_function = None
            if pcie_device_uri := nw_adapter.first_link("Controllers/Links/PCIeDevices"):
                pcie_device = client.get_resource(pcie_device_uri)
                if pcie_functions_uri := pcie_device.link("PCIeFunctions"):
                    pcie_function = client.find_first_resource_in_collection(pcie_functions_uri)
            device_id_info.update(self.get_pcie_id_info(pcie_device, pcie_function))

            yield device_id_info


class GraphicControllerFinder(DeviceFinder):
    """GraphicController finder."""

    def find_all_devices(self, client: redfish.Client) -> Iterator[dict]:
        for gc in self.all_resources_in_computer_system(client, "GraphicsControllers"):
            yield {
                "deviceKeys": {"SerialNumber": gc.prop("SerialNumber")},
                "deviceType": "graphicController",
                "oobDeviceID": gc.prop("Id"),
            }
