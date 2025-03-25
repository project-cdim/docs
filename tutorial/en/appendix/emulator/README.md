# How to Operate the Emulator
This section explains the emulator used with the Composable Disaggregated Infrastructure Manager (CDIM). For more detailed configuration methods, please refer to [hw-emulator-reference](https://github.com/project-cdim/hw-emulator-reference).

- [1. Emulator Configuration Method](#1-emulator-configuration-method)
- [2. Emulator Operation Method](#2-emulator-operation-method)
   - [2.1. Information Collection Method](#21-information-collection-method)
   - [2.2. Metric State Change Method](#22-metric-state-change-method)

## 1. Emulator Configuration Method
This section shows the emulator configuration file and its basic configuration items.  
If you want to change the default device information provided, please also check "2. Redfish Emulator Device Definition File Configuration" and "3. Redfish Emulator Output Data Configuration".

<details>
<summary> 1. Basic Configuration of Redfish Emulator </summary>  
<r>
Configuration File Name  
<br>

- When using a device definition file: emulator-config_device_populate.json  

- When not using a device definition file: emulator-config_dynamic_populate.json  
<r>
Configuration Item List

| Item | Description | Setting Value |
|:--|:--|:--|
| MODE | Specifies the port to use. If the value is "Local", the port is assigned the value of the command line or port parameter 5000 by default | Local |
| HTTPS | Specifies whether to use HTTPS. | Disable |
| TRAYS | Path to resources that make up the initial resource pool. Multiple trays can be specified. When TRAYS is specified, it will be obtained from TRAYS when creating a device. | Not used |
| POPULATE | Element at emulator startup. Specifies a common file | ../simulatorDeviceList.json |
| DEVICE_SPEC | Whether to create a device using a common file. Must be specified if using a common file | true |
| SPEC | Whether the computer system is represented as a Redfish ComputerSystem or another schema. Used when setting the system path | Redfish |
| MOCKUPFOLDERS | Storage location for mockup folders. The folder stores JSON files for returning static data (mockup) that do not change or operate | Redfish |
| POWER_LINK | Links the power state of the CPU with the power state of the GPU, memory, storage, and NIC present in the same ComputerSystem | true |
</details>

<details>
<summary> 2. Redfish Emulator Device Definition File Configuration </summary>  
<r>
Configuration File Name  
<br>

Device Definition File: simulatorDeviceList.json 

<r>
Configuration Item List

Only basic input items are listed below. Items specific to each device are not listed.

| Item | Description |
|:--|:--|
| deviceID | ID for individually recognizing the device. The deviceID must be a unique string. |
| model | Item to enter the model name of the device. |
| manufacturer | Item to enter the manufacturer of the device. |
| link | Item to list built-in devices pre-connected to the CPU. This item is only present on the CPU and requires the listing of one or more built-in memories. |
</details>

<details>
<summary> 3. Redfish Emulator Output Data Configuration </summary>  
<r>
Configuration File Name  
<br>

Output Data Configuration File: infragen/test_device_parameter.json

<r>
Configuration Item List

Only basic input items are listed below. Items specific to each device are not listed.

| Item | Description |
|:--|:--|
| state | Specifies the state of the device. By default, "Enable" is entered. |
| health | Specifies whether there is an abnormality in the device. By default, "OK" is entered, and "Warning" or "Critical" can also be entered. |
| sensingInterval | Specifies the time interval (s) between sensor readings. |

</details>

## 2. Emulator Operation Method
This section shows the basic usage of the emulator.

### 2.1. Information Collection Method    
This section explains the information collection method on the emulator.

Retrieve the manager information list and manager information.
```sh
$ docker container exec -it hw-emulator /bin/sh
$ curl http://localhost:5000/redfish/v1/Managers
$ curl http://localhost:5000/redfish/v1/Managers/BMC-1
```
Retrieve the information of ComputerSystem or Chassis according to the device you want to obtain.
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
This section explains how to change the metric state of the emulator using the CPU as an example.

Retrieve detailed information about the CPU.
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

Verify the changes.
```sh
$ curl http://localhost:5000/redfish/v1/Systems/System-1/Processors/PROC-0001/ProcessorMetrics | jq
{
        :
  "BandwidthPercent": 0,  # Changed to 0 because it was set to off.
        :
}
```
