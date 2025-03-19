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

"""Device operations."""

from typing import Any, Iterator

from app.common.basic_exceptions import RequestNotSupportedHwControlError, DeviceNotFoundHwControlError

from . import redfish


class DeviceOperations:
    """Base class of device operations."""

    def __init__(self, manager_uri: str) -> None:
        self.manager_uri = manager_uri

    def get_spec_info(self, client: redfish.Client, oob_device_id: str) -> tuple[dict[str, Any], list[dict[str, str]]]:
        """Get device information.

        Args:
            client: Redfish client
            oob_device_id: OOB device ID
        Returns:
            tuple of Schema and Link
        """
        raise RequestNotSupportedHwControlError

    def get_metric_info(
        self, client: redfish.Client, oob_device_id: str
    ) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
        """Get metric information.

        Args:
            client: Redfish client
            oob_device_id: OOB device ID
        Returns:
            tuple of Schema, Metric and Environment
        """
        raise RequestNotSupportedHwControlError

    def get_power_state(self, client: redfish.Client, oob_device_id: str) -> str | None:
        """Get power state.

        Args:
            client: Redfish client
            oob_device_id: OOB device ID
        Returns:
            PowerState if available, None otherwise
        """
        raise RequestNotSupportedHwControlError

    def power_on(self, client: redfish.Client, oob_device_id: str) -> int:
        """Power on.

        Args:
            client: Redfish client
            oob_device_id: OOB device ID
        Returns:
            response status code
        """
        raise RequestNotSupportedHwControlError

    def power_off(self, client: redfish.Client, oob_device_id: str) -> int:
        """Power off.

        Args:
            client: Redfish client
            oob_device_id: OOB device ID
        Returns:
            response status code
        """
        raise RequestNotSupportedHwControlError

    def reset(self, client: redfish.Client, oob_device_id: str) -> int:
        """Reset.

        Args:
            client: Redfish client
            oob_device_id: OOB device ID
        Returns:
            response status code
        """
        raise RequestNotSupportedHwControlError

    def shutdown_os(self, client: redfish.Client, oob_device_id: str) -> int:
        """Shutdown OS.

        Args:
            client: Redfish client
            oob_device_id: OOB device ID
        Returns:
            response status code
        """
        raise RequestNotSupportedHwControlError

    # ------------------------------------------------------------
    # Resource accessors
    # ------------------------------------------------------------
    def get_manager(self, client: redfish.Client) -> redfish.Resource:
        """Get Manager.

        Args:
            client: Redfish client
        Returns:
            Manager
        """
        return client.get_resource(self.manager_uri)

    def all_resources_in_computer_system(
        self, client: redfish.Client, collection_name: str
    ) -> Iterator[tuple[redfish.Resource, redfish.Resource]]:
        """Get all resources in ComputerSystem.

        Args:
            client: Redfish client
            collection_name: resource collection name
        Returns:
            Iterator of tuple of the resource and ComputerSystem
        """
        manager = client.get_resource(self.manager_uri)
        for computer_system_uri in manager.all_links("Links/ManagerForServers"):
            computer_system = client.get_resource(computer_system_uri)
            if collection_uri := computer_system.link(collection_name):
                for resource in client.find_all_resources_in_collection(collection_uri):
                    yield resource, computer_system

    def get_resource_in_chassis(
        self, client: redfish.Client, collection_name: str, oob_device_id: str
    ) -> redfish.Resource:
        """Get the resource in Chassis.

        Args:
            client: Redfish client
            collection_name: resource collection name
            oob_device_id: OOB device ID to identify the resource
        Returns:
            the resource
        """
        manager = self.get_manager(client)
        if chassis_uri := manager.link("Links/ManagerInChassis"):
            chassis = client.get_resource(chassis_uri)
            if collection_uri := chassis.link(collection_name):
                if resource := client.find_resource_in_collection(collection_uri, oob_device_id):
                    return resource
        raise DeviceNotFoundHwControlError

    def get_resource_in_computer_system(
        self, client: redfish.Client, collection_name: str, oob_device_id: str
    ) -> tuple[redfish.Resource, redfish.Resource]:
        """Get the resource in ComputerSystem.

        Args:
            client: Redfish client
            collection_name: resource collection name
            oob_device_id: OOB device ID to identify the resource
        Returns:
            tuple of the resource and ComputerSystem
        """
        manager = self.get_manager(client)
        for computer_system_uri in manager.all_links("Links/ManagerForServers"):
            computer_system = client.get_resource(computer_system_uri)
            if collection_uri := computer_system.link(collection_name):
                if resource := client.find_resource_in_collection(collection_uri, oob_device_id):
                    return resource, computer_system
        raise DeviceNotFoundHwControlError

    def get_resource_in_computer_system_or_chassis(
        self, client: redfish.Client, collection_name: str, oob_device_id: str
    ) -> tuple[redfish.Resource, redfish.Resource | None]:
        """Get the resource in ComputerSystem or Chassis.

        Args:
            client: Redfish client
            collection_name: resource collection name
            oob_device_id: OOB device ID to identify the resource
        Returns:
            tuple of the resource and ComputerSystem.
            The ComputerSystem is None if the resource is found in Chassis.
        """
        try:
            return self.get_resource_in_computer_system(client, collection_name, oob_device_id)
        except DeviceNotFoundHwControlError:
            resource = self.get_resource_in_chassis(client, collection_name, oob_device_id)
            return resource, None

    def get_environment_metrics(self, client: redfish.Client, resource: redfish.Resource) -> dict[str, Any]:
        """Get EnvironmentMetrics as dictionary.

        Args:
            client: Redfish client
            resource: Redfish resource (Processor, Memory, ...)
        Returns:
            EnvironmentMetrics dictionary
        """
        env_metrics_dict = {}
        if env_metrics_uri := resource.link("EnvironmentMetrics"):
            env_metrics = client.get_resource(env_metrics_uri)
            env_metrics_dict.update(env_metrics.as_dict())
            if ds_uri := env_metrics.prop("EnergyJoules/DataSourceUri"):
                env_metrics_dict["Sensor"] = client.get_resource(ds_uri).as_dict()
        return env_metrics_dict

    def get_metrics_and_environment_metrics(
        self, client: redfish.Client, resource: redfish.Resource
    ) -> tuple[dict[str, Any], dict[str, Any]]:
        """Get Metrics and EnvironmentMetrics as dictionary.

        Args:
            client: Redfish client
            resource: Redfish resource (Processor, Memory, ...)
        Returns:
            tuple of Metrics dictionary and EnvironmentMetrics dictionary
        """
        metrics_dict = {}
        if metrics_uri := resource.link("Metrics"):
            metrics_dict.update(client.get_resource(metrics_uri).as_dict())

        env_metrics_dict = self.get_environment_metrics(client, resource)

        return metrics_dict, env_metrics_dict

    # ------------------------------------------------------------
    # Utilities
    # ------------------------------------------------------------
    def link_for(self, device_type: str, oob_device_id: str) -> dict[str, str]:
        """Create a dictionary in Link.

        Args:
            device_type: device type
            oob_device_id: OOB device ID
        Return:
            dictionary for Link element
        """
        return {"type": device_type, "deviceID": oob_device_id}

    def find_cpu_links(self, client: redfish.Client, computer_system: redfish.Resource) -> Iterator[dict]:
        """Find CPU links in ComputerSystem.

        Args:
            client: Redfish client
            computer_system: ComputerSystem
        Returns:
            Iterator of Link
        """
        if processors_uri := computer_system.link("Processors"):
            for processor in client.find_all_resources_in_collection(processors_uri):
                if processor.prop("ProcessorType") == "CPU" and (oob_device_id := processor.prop("Id")):
                    yield self.link_for("CPU", oob_device_id)


class ProcessorOperations(DeviceOperations):
    """Processor operations."""

    def set_power_state(self, client: redfish.Client, oob_device_id: str, reset_type: str) -> int:
        """Set power state.

        Args:
            client: Redfish client
            oob_device_id: OOB device ID
            reset_type: ResetType of Reset Action (On, ForceOff, ForceRestart, GracefulShutdown)
        Returns:
            response status code
        """
        processor = self.get_resource_in_chassis(client, "Processors", oob_device_id)
        return client.do_action(processor, "Processor", "Reset", {"ResetType": reset_type})


class CPUOperations(ProcessorOperations):
    """CPU operations."""

    def get_spec_info(self, client: redfish.Client, oob_device_id: str) -> tuple[dict[str, Any], list[dict[str, str]]]:
        processor, computer_system = self.get_resource_in_computer_system(client, "Processors", oob_device_id)
        schema = processor.as_dict()
        schema["PowerCapability"] = processor.action_values_allowable(
            "Processor", "Reset", "ResetType", "On", "ForceOff", "ForceRestart"
        )
        links = list(self._find_non_cpu_links(client, computer_system))
        return schema, links

    def _find_non_cpu_links(self, client: redfish.Client, computer_system: redfish.Resource) -> Iterator[dict]:
        yield from self._find_gpu_links(client, computer_system)
        yield from self._find_memory_links(client, computer_system)
        yield from self._find_storage_links(client, computer_system)
        yield from self._find_network_interface_links(client, computer_system)
        yield from self._find_graphic_controller_links(client, computer_system)

    def _find_gpu_links(self, client: redfish.Client, computer_system: redfish.Resource) -> Iterator[dict]:
        if processors_uri := computer_system.link("Processors"):
            for processor in client.find_all_resources_in_collection(processors_uri):
                if processor.prop("ProcessorType") == "GPU" and (oob_device_id := processor.prop("Id")):
                    yield self.link_for("GPU", oob_device_id)

    def _find_memory_links(self, client: redfish.Client, computer_system: redfish.Resource) -> Iterator[dict]:
        if memory_list_uri := computer_system.link("Memory"):
            for memory in client.find_all_resources_in_collection(memory_list_uri):
                if oob_device_id := memory.prop("Id"):
                    yield self.link_for("memory", oob_device_id)

    def _find_storage_links(self, client: redfish.Client, computer_system: redfish.Resource) -> Iterator[dict]:
        if storages_uri := computer_system.link("Storage"):
            for storage in client.find_all_resources_in_collection(storages_uri):
                for drive_uri in storage.all_links("Drives"):
                    drive = client.get_resource(drive_uri)
                    if oob_device_id := drive.prop("Id"):
                        yield self.link_for("storage", oob_device_id)

    def _find_network_interface_links(
        self, client: redfish.Client, computer_system: redfish.Resource
    ) -> Iterator[dict]:
        if nw_interfaces_uri := computer_system.link("NetworkInterfaces"):
            for nw_interface in client.find_all_resources_in_collection(nw_interfaces_uri):
                if nw_adapter_uri := nw_interface.link("Links/NetworkAdapter"):
                    nw_adapter = client.get_resource(nw_adapter_uri)
                    if oob_device_id := nw_adapter.prop("Id"):
                        yield self.link_for("networkInterface", oob_device_id)

    def _find_graphic_controller_links(
        self, client: redfish.Client, computer_system: redfish.Resource
    ) -> Iterator[dict]:
        if gc_list_uri := computer_system.link("GraphicsControllers"):
            for gc in client.find_all_resources_in_collection(gc_list_uri):
                if oob_device_id := gc.prop("Id"):
                    yield self.link_for("graphicController", oob_device_id)

    def get_metric_info(
        self, client: redfish.Client, oob_device_id: str
    ) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
        processor = self.get_resource_in_chassis(client, "Processors", oob_device_id)
        schema = processor.as_dict()
        schema["PowerCapability"] = processor.action_values_allowable(
            "Processor", "Reset", "ResetType", "On", "ForceOff", "ForceRestart"
        )
        metrics, env_metrics = self.get_metrics_and_environment_metrics(client, processor)
        return schema, metrics, env_metrics

    def get_power_state(self, client: redfish.Client, oob_device_id: str) -> str | None:
        processor = self.get_resource_in_chassis(client, "Processors", oob_device_id)
        return processor.prop("PowerState")

    def power_on(self, client: redfish.Client, oob_device_id: str) -> int:
        return self.set_power_state(client, oob_device_id, "On")

    def power_off(self, client: redfish.Client, oob_device_id: str) -> int:
        return self.set_power_state(client, oob_device_id, "ForceOff")

    def reset(self, client: redfish.Client, oob_device_id: str) -> int:
        return self.set_power_state(client, oob_device_id, "ForceRestart")

    def shutdown_os(self, client: redfish.Client, oob_device_id: str) -> int:
        _, computer_system = self.get_resource_in_computer_system(client, "Processors", oob_device_id)
        return client.do_action(computer_system, "ComputerSystem", "Reset", {"ResetType": "GracefulShutdown"})


class GPUOperations(ProcessorOperations):
    """GPU operations."""

    def get_spec_info(self, client: redfish.Client, oob_device_id: str) -> tuple[dict[str, Any], list[dict[str, str]]]:
        processor, computer_system = self.get_resource_in_computer_system_or_chassis(
            client, "Processors", oob_device_id
        )
        schema = processor.as_dict()
        schema["PowerCapability"] = processor.action_values_allowable(
            "Processor", "Reset", "ResetType", "On", "ForceOff"
        )

        links: list[dict] = []
        if computer_system:
            links.extend(self.find_cpu_links(client, computer_system))

        return schema, links

    def get_metric_info(
        self, client: redfish.Client, oob_device_id: str
    ) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
        processor = self.get_resource_in_chassis(client, "Processors", oob_device_id)
        schema = processor.as_dict()
        schema["PowerCapability"] = processor.action_values_allowable(
            "Processor", "Reset", "ResetType", "On", "ForceOff"
        )
        metrics, env_metrics = self.get_metrics_and_environment_metrics(client, processor)
        return schema, metrics, env_metrics

    def power_on(self, client: redfish.Client, oob_device_id: str) -> int:
        return self.set_power_state(client, oob_device_id, "On")

    def power_off(self, client: redfish.Client, oob_device_id: str) -> int:
        return self.set_power_state(client, oob_device_id, "ForceOff")


class MemoryOperations(DeviceOperations):
    """Memory operations."""

    def get_spec_info(self, client: redfish.Client, oob_device_id: str) -> tuple[dict[str, Any], list[dict[str, str]]]:
        memory, computer_system = self.get_resource_in_computer_system_or_chassis(client, "Memory", oob_device_id)
        schema = memory.as_dict()
        schema["PowerCapability"] = memory.action_values_allowable("Memory", "Reset", "ResetType", "On", "ForceOff")

        links: list[dict] = []
        if computer_system:
            links.extend(self.find_cpu_links(client, computer_system))
        return schema, links

    def get_metric_info(
        self, client: redfish.Client, oob_device_id: str
    ) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
        memory = self.get_resource_in_chassis(client, "Memory", oob_device_id)
        schema = memory.as_dict()
        schema["PowerCapability"] = memory.action_values_allowable("Memory", "Reset", "ResetType", "On", "ForceOff")
        metrics, env_metrics = self.get_metrics_and_environment_metrics(client, memory)
        return schema, metrics, env_metrics

    def power_on(self, client: redfish.Client, oob_device_id: str) -> int:
        return self._set_power_state(client, oob_device_id, "On")

    def power_off(self, client: redfish.Client, oob_device_id: str) -> int:
        return self._set_power_state(client, oob_device_id, "ForceOff")

    def _set_power_state(self, client: redfish.Client, oob_device_id: str, reset_type: str) -> int:
        memory = self.get_resource_in_chassis(client, "Memory", oob_device_id)
        return client.do_action(memory, "Memory", "Reset", {"ResetType": reset_type})


class StorageOperations(DeviceOperations):
    """Storage operations."""

    def get_spec_info(self, client: redfish.Client, oob_device_id: str) -> tuple[dict[str, Any], list[dict[str, str]]]:
        schema = {}
        links: list[dict] = []

        drive = self.get_resource_in_chassis(client, "Drives", oob_device_id)
        drive_dict = drive.as_dict()
        drive_dict["PowerCapability"] = drive.action_values_allowable("Drive", "Reset", "ResetType", "On", "ForceOff")
        schema["Drive"] = drive_dict

        if storage_uri := drive.first_link("Links/Storage"):
            storage = client.get_resource(storage_uri)
            storage_dict = storage.as_dict()
            schema["Storage"] = storage_dict

            if storage_oob_device_id := storage.prop("Id"):
                try:
                    _, computer_system = self.get_resource_in_computer_system(client, "Storage", storage_oob_device_id)
                    links.extend(self.find_cpu_links(client, computer_system))
                except DeviceNotFoundHwControlError:
                    pass  # not used by ComputerSystem

        if volume_uri := drive.first_link("Links/Volumes"):
            volume = client.get_resource(volume_uri)
            schema["Volume"] = volume.as_dict()

        return schema, links

    def get_metric_info(
        self, client: redfish.Client, oob_device_id: str
    ) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
        schema = {}

        drive = self.get_resource_in_chassis(client, "Drives", oob_device_id)
        drive_dict = drive.as_dict()
        drive_dict["PowerCapability"] = drive.action_values_allowable("Drive", "Reset", "ResetType", "On", "ForceOff")
        schema["Drive"] = drive_dict

        if volume_uri := drive.first_link("Links/Volumes"):
            volume = client.get_resource(volume_uri)
            schema["Volume"] = volume.as_dict()

        env_metrics = self.get_environment_metrics(client, drive)

        return schema, {}, env_metrics

    def power_on(self, client: redfish.Client, oob_device_id: str) -> int:
        return self._set_power_state(client, oob_device_id, "On")

    def power_off(self, client: redfish.Client, oob_device_id: str) -> int:
        return self._set_power_state(client, oob_device_id, "ForceOff")

    def _set_power_state(self, client: redfish.Client, oob_device_id: str, reset_type: str) -> int:
        drive = self.get_resource_in_chassis(client, "Drives", oob_device_id)
        return client.do_action(drive, "Drive", "Reset", {"ResetType": reset_type})


class NetworkInterfaceOperations(DeviceOperations):
    """NetworkInterface operations."""

    def get_spec_info(self, client: redfish.Client, oob_device_id: str) -> tuple[dict[str, Any], list[dict[str, str]]]:
        schema = {}

        # NetworkAdapter
        manager = self.get_manager(client)
        nw_adapter = self.get_resource_in_chassis(client, "NetworkAdapters", oob_device_id)
        nw_adapter_dict = nw_adapter.as_dict()
        nw_adapter_dict["PowerCapability"] = nw_adapter.action_values_allowable(
            "NetworkAdapter", "Reset", "ResetType", "On", "ForceOff"
        )
        schema["Network"] = nw_adapter_dict

        # NetworkDeviceFunction
        if nw_device_functions_uri := nw_adapter.link("NetworkDeviceFunctions"):
            if nw_device_function := client.find_first_resource_in_collection(nw_device_functions_uri):
                schema["NetworkDeviceFunctions"] = nw_device_function.as_dict()

        # SerialInterface
        if serial_interfaces_uri := manager.link("SerialInterfaces"):
            if serial_interface := client.find_first_resource_in_collection(serial_interfaces_uri):
                schema["SerialInterfaces"] = serial_interface.as_dict()

        # Port
        if ports_uri := nw_adapter.link("Ports"):
            if port := client.find_first_resource_in_collection(ports_uri):
                schema["Port"] = port.as_dict()

        # Links
        links: list[dict] = []
        try:
            _, computer_system = self._get_network_adapter_in_computer_system(client, oob_device_id)
            links.extend(self.find_cpu_links(client, computer_system))
        except DeviceNotFoundHwControlError:
            pass  # not used by ComputerSystem

        return schema, links

    def get_metric_info(
        self, client: redfish.Client, oob_device_id: str
    ) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
        schema = {}
        metrics = {}

        # NetworkAdapter
        nw_adapter = self.get_resource_in_chassis(client, "NetworkAdapters", oob_device_id)
        nw_adapter_dict = nw_adapter.as_dict()
        nw_adapter_dict["PowerCapability"] = nw_adapter.action_values_allowable(
            "NetworkAdapter", "Reset", "ResetType", "On", "ForceOff"
        )
        schema["Network"] = nw_adapter_dict

        if metrics_uri := nw_adapter.link("Metrics"):
            metrics["Network"] = client.get_resource(metrics_uri).as_dict()

        # NetworkDeviceFunction
        if nw_device_functions_uri := nw_adapter.link("NetworkDeviceFunctions"):
            if nw_device_function := client.find_first_resource_in_collection(nw_device_functions_uri):
                schema["NetworkDeviceFunctions"] = nw_device_function.as_dict()
                if nw_device_function_metrics_uri := nw_device_function.link("Metrics"):
                    metrics["NetworkDeviceFunctions"] = client.get_resource(nw_device_function_metrics_uri).as_dict()

        # EnvironmentMetrics
        env_metrics = self.get_environment_metrics(client, nw_adapter)

        return schema, metrics, env_metrics

    def power_on(self, client: redfish.Client, oob_device_id: str) -> int:
        return self._set_power_state(client, oob_device_id, "On")

    def power_off(self, client: redfish.Client, oob_device_id: str) -> int:
        return self._set_power_state(client, oob_device_id, "ForceOff")

    def _set_power_state(self, client: redfish.Client, oob_device_id: str, reset_type: str) -> int:
        nw_adapter = self.get_resource_in_chassis(client, "NetworkAdapters", oob_device_id)
        return client.do_action(nw_adapter, "NetworkAdapter", "Reset", {"ResetType": reset_type})

    def _get_network_adapter_in_computer_system(
        self, client: redfish.Client, oob_device_id: str
    ) -> tuple[redfish.Resource, redfish.Resource]:
        for nw_interface, computer_system in self.all_resources_in_computer_system(client, "NetworkInterfaces"):
            if nw_adapter_uri := nw_interface.link("Links/NetworkAdapter"):
                nw_adapter = client.get_resource(nw_adapter_uri)
                if nw_adapter.prop("Id") == oob_device_id:
                    return nw_adapter, computer_system
        raise DeviceNotFoundHwControlError


class GraphicControllerOperations(DeviceOperations):
    """GraphicController operations."""

    def get_spec_info(self, client: redfish.Client, oob_device_id: str) -> tuple[dict[str, Any], list[dict[str, str]]]:
        gc, computer_system = self.get_resource_in_computer_system(client, "GraphicsControllers", oob_device_id)
        schema = gc.as_dict()
        links = list(self.find_cpu_links(client, computer_system))

        return schema, links
