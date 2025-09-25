# 2. HW Control Function

This chapter describes an overview of the REST API for the HW control function,
and then presents the functions implemented by the plugin.

## 2.1. REST API of HW Control Function

The REST API of the HW control function related to plugins is shown below.

|No.|Name                            |URI                                         |METHOD|Description
|:-:|--------------------------------|--------------------------------------------|:----:|------------------------------
| 1 |Get device ID list information  |/cdim/api/v1/device-ids                     | GET  |Get a list of device IDs.
| 2 |Get all device spec information |/cdim/api/v1/devices                        | GET  |Get spec information of all devices.
| 3 |Get spec information            |/cdim/api/v1/devices/{deviceID}/specs       | GET  |Get spec information of the device.
| 4 |Get metric information          |/cdim/api/v1/devices/{deviceID}/metrics     | GET  |Get metric information of the device.
| 5 |Get resource information        |/cdim/api/v1/devices/{deviceID}             | GET  |Get spec and metric information of the device.
| 6 |Change configuration (CPU to Device)     |/cdim/api/v1/cpu/{CPUDeviceID}/aggregations | PUT  |Controls the aggregation state between CPU and device.**Deprecated**
| 7 |Control power                   |/cdim/api/v1/devices/{deviceID}/power       | PUT  |Controls the power of the device.
| 8 |Get OS boot status              |/cdim/api/v1/cpu/{CPUDeviceID}/is-os-ready  | GET  |Gets the boot status of the OS.
| 9 |Change configuration (Device to Device)  |/cdim/api/v1/devices/{sourceDeviceID}/aggregations | PUT  |Controls the aggregation state between upstream side device and downstream side device.

Change configuration (CPU to Device) will be removed in future releases.

## 2.2. Plugin Overview

Plugins are implemented as classes(see [4.2 Class Structure](04_Configuration.md#42-class-structure)).  
The REST API of the HW control function collects device information and controls the device.  
When hardware-dependent processing is required, HW control function instantiates the appropriate plugin for the target device  
and calls its methods to delegate hardware-dependent processing.

The following are the methods that the plugin implements.

### OOB Plugin Methods

|No.|Name                        |Method           |Description
|:-:|----------------------------|-----------------|----------------------------
| 1 |Get device list information |get_device_info  |Get a list of devices.
| 2 |Get spec information        |get_spec_info    |Get spec information of the device.
| 3 |Get metric information      |get_metric_info  |Get metric information of the device.
| 4 |Get power state             |get_power_state  |Get the power state of the device.
| 5 |Power ON                    |post_power_on    |Turn on the device.
| 6 |Power OFF                   |post_power_off   |Turn off the device.
| 7 |CPU reset                   |post_cpu_reset   |Reset CPU.
| 8 |OS shutdown                 |post_os_shutdown |Shutdown OS.

### FM Plugin Methods

|No.|Name                   |Method           |Description
|:-:|-----------------------|-----------------|---------------------------------
| 1 |Connect device         |connect          |Connect the USP-side port to the DSP-side port (see *1).
| 2 |Disconnect device      |disconnect       |Disconnect the USP-side port and the DSP-side port (see *1).
| 3 |Get port information   |get_port_info    |Get the port information of the CXL switch.
| 4 |Get switch information |get_switch_info  |Get information of the CXL switch.

*1. USP: Upstream Switch Port, DSP: Downstream Switch Port
