# How to Operate the Emulator
This section explains the emulator used with Composable Disaggregated Infrastructure Manager (CDIM). For more detailed configuration methods, please refer to [hw-emulator-reference](https://github.com/project-cdim/hw-emulator-reference).

- [1. Emulator Configuration Method](#1-emulator-configuration-method)
- [2. Emulator Operation Method](#2-emulator-operation-method)
  - [2.1. Information Collection Method](#21-information-collection-method)
  - [2.2. Metric State Change Method](#22-metric-state-change-method)

## 1. Emulator Configuration Method
This section outlines the configuration file and basic configuration items for the emulator.
Please review "2. Redfish Emulator Device Definition File Configuration" and "3. Redfish Emulator Output Data Configuration" for modifications to default device information.

<details>
<summary> 1. Basic Configuration of Redfish Emulator </summary>
Configuration File Names:

- **With device definition file**: emulator-config_device_populate.json
- **Without device definition file**: emulator-config_dynamic_populate.json

Configuration Items:

| Item | Description | Setting Value |
|:--|:--|:--|
| MODE | Port to be used. Defaults to port 5000 if set to "Local". | Local |
| HTTPS | Determines if HTTPS is used. | Disable |
| TRAYS | Initial resource pool components path. Multiple trays can be specified. | Not used |
| POPULATE | Common file specified at emulator launch. | ../simulatorDeviceList.json |
| DEVICE_SPEC | Flag to create a device using a common file. | true |
| SPEC | Defines the schema representation of the computer system. | Redfish |
| MOCKUPFOLDERS | Location for storing mockup JSON files. | Redfish |
| POWER_LINK | Links the power state of components within the same ComputerSystem. | true |
</details>

<details>
<summary> 2. Redfish Emulator Device Definition File Configuration </summary>
Configuration File:

- *simulatorDeviceList.json*

Configuration Items:

| Item | Description |
|:--|:--|
| deviceID | Unique identifier for recognizing the device. |
| model | Model name of the device. |
| manufacturer | Manufacturer of the device. |
| link | Connectivity to built-in devices, specific to CPUs. |
</details>

<details>
<summary> 3. Redfish Emulator Output Data Configuration </summary>
Configuration File:

- *infragen/test_device_parameter.json*

Configuration Items:

| Item | Description |
|:--|:--|
| state | Device state, typically "Enable". |
| health | Device health status, options include "OK", "Warning", or "Critical". |
| sensingInterval | Time interval (seconds) for sensor readings. |
</details>

## 2. Emulator Operation Method
This section outlines basic operations of the emulator.

### 2.1. Information Collection Method    
This section explains the information collection method on the emulator.

Retrieve manager list and specific manager details.
```sh
$ docker container exec -it hw-emulator /bin/sh
$ curl http://localhost:5000/redfish/v1/Managers
$ curl http://localhost:5000/redfish/v1/Managers/BMC-1
```
Retrieve information for ComputerSystem or Chassis.
```sh
$ curl http://localhost:5000/redfish/v1/Systems/System-1
$ curl http://localhost:5000/redfish/v1/Chassis/Chassis-1
```
Retrieve the list of devices for the target device type.
```sh
$ curl http://localhost:5000/redfish/v1/Systems/System-1/Processors
```
Retrieve the information of the target device.
```sh
$ curl http://localhost:5000/redfish/v1/Systems/System-1/Processors/PROC-0001
```

### 2.2. Metric State Change Method
This section explains the steps to change the metric state of devices, using a CPU as an example.

Retrieve detailed CPU information.
```sh
$ docker container exec -it hw-emulator /bin/sh
$ curl http://localhost:5000/redfish/v1/Systems/System-1/Processors/PROC-0001 | jq
```
Check the following from the obtained information.
```json
"Oem": {
  "#Processor.MetricState": {
    "StateType@Redfish.AllowableValues": [
      "off",
      "steady",
      "low",
      "high",
      "action"
    ],
    "target": "/redfish/v1/Systems/System-1/Processors/PROC-0001/Actions/Processor.MetricState"
  }
}
```
Use the confirmed information to change the metric state.
```sh
$ curl -XPOST http://localhost:5000/redfish/v1/Systems/System-1/Processors/PROC-0001/Actions/Processor.MetricState -H "Content-Type: application/json" -d '{"StateType": "off"}'
```

Confirm the changes:
```sh
$ curl http://localhost:5000/redfish/v1/Systems/System-1/Processors/PROC-0001/ProcessorMetrics | jq
{
        :
  "BandwidthPercent": 0,  # Reflects the 'off' setting.
        :
}
```