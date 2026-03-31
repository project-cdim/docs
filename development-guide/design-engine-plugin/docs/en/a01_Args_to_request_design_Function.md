# Appendix 1. Arguments to `request_design`

## Request ID (`requestID`)

The request ID identifies the layout design request on the caller side of the Layout Design.

<details>
<summary>Show details for Request ID</summary>

- requestID (String): ID to identify a layout design request

Example:
```json
{
    "requestID": "463e79c1-d138-4748-9018-5c1435a50d87"
}
```

</details>

## Target Node IDs (`targetNodeIDs`)

Target Node IDs are the list of node IDs to be designed among all nodes.
For entire design ([Partial Design Flag](a01_Args_to_request_design_Function.md#partial-design-flag-partialdesign) is false), this list is empty.

<details>
<summary>Show details for Target Node IDs</summary>

- targetNodeIDs (StringList): List of node IDs to design

Example:
```json
{
    "targetNodeIDs": ["9158d69e-abca-4ef1-929b-78424b01005b"]
}
```

</details>

## Service Set Request Resources (`serviceSetRequestResources`)

Service Set Request Resources describe resource types and performance required by services.

<details>
<summary>Show details for Service Set Request Resources</summary>

Structure and meaning of each item:

- serviceSetRequestResources (ObjectList): Resources required by the service set
    - id (String): Service set request resource ID
    - serviceSetID (String): Service set ID
    - serviceSetName (String): Service set name
    - serviceRequestResources (ObjectList): Resources required by services in the set
        - id (String): Service request resource ID
        - serviceID (String): Service ID
        - serviceName (String): Service name
        - shareService (bool): Whether this service can share a node with other services (true: share, false: exclusive)
        - resources (Object): Devices and performance required by the service
            - operatingSystem (String): OS to use
            - instances (ObjectList): Per-instance device and performance
                - requestInstanceID (String): ID to identify the service instance during design
                - serviceInstanceID (String): ID to identify the service instance after deployment
                - redundant (bool): Whether this instance is a redundant one (true) or a normal one (false)
                - changed (bool): For partial design, whether to re-design this instance (true) or not (false)
                - cpu (Object): CPU performance requirements
                    - architecture (String): CPU architecture
                    - coreNumber (Number): Number of cores
                    - operatingSpeedMHz (Number): Clock speed (MHz)
                - memory (Object): Memory performance requirements
                    - size (Number): Capacity (MB)
                    - operatingSpeedMHz (Number): Speed (MHz)
                - storage (Object): Storage performance requirements
                    - size (Number): Capacity (GB)
                    - capableSpeedGbs (Number): Controller link speed (Gbit/s)
                - gpu (ObjectList): GPU performance requirements
                    - architecture (String): GPU architecture
                    - coreNumber (Number): Number of cores
                    - operatingSpeedMHz (Number): Clock speed (MHz)
                    - memorySize (Number): Memory size (MB)
                    - deviceCount (Number): Number of devices required
                - networkInterface (Object): NIC performance requirements
                    - bitRate (Number): Link speed (Mbit/s)

Example:
```json
{
    "serviceSetRequestResources": [
        {
            "id": "6ea26bd4-ece0-4a9a-b042-3fa04361526e",
            "serviceSetID": "bbb02921-ee54-4b26-97d2-0fec1d987b12",
            "serviceSetName": "Web app chat services",
            "serviceRequestResources": [
                {
                    "id": "cbc896de-1df2-4aed-b71d-4aff38206ca3",
                    "serviceID": "a58ee3a7-62a0-46f3-ba80-f7080eaa0d1c",
                    "serviceName": "LLM agent",
                    "shareService": false,
                    "resource": {
                        "operatingSystem": "Redhat Enterprise 9.0",
                        "instances": [
                            {
                                "requestInstanceID": "1d40d2a9-979f-4956-aee7-30587de64fe9",
                                "serviceInstanceID": "5b4ea1a2-4130-4de8-9045-bc92709df778",
                                "redundant": false,
                                "changed": true,
                                "cpu": {
                                    "architecture": "x86",
                                    "coreNumber": 8,
                                    "operatingSpeedMHz": 3200
                                },
                                "memory": {
                                    "size": 8000,
                                    "operatingSpeedMHz": 3200
                                },
                                "storage": {
                                    "size": 500,
                                    "capableSpeedGbs": 12
                                },
                                "gpu": [
                                    {
                                        "architecture": "x86",
                                        "coreNumber": 32,
                                        "operatingSpeedMHz": 2400,
                                        "memorySize": 16000,
                                        "deviceCount": 2
                                    }
                                ],
                                "networkInterface": {
                                    "bitRate": 9600
                                }
                            }
                        ]
                    }
                }
            ]
        }
    ]
}
```

</details>

## Services (`services`)

A list of service definitions that are in scope for the design.

<details>
<summary>Show details for Services</summary>

Structure and meaning of each item:

- services (ObjectList): Service definitions in scope
    - id (String): Service ID
    - name (String): Service name
    - description (String): Service description
    - owner (String): Service owner
    - instances (ObjectList): Service instances running in the current configuration
        - serviceInstanceID (String): ID after deployment
        - requestInstanceID (String): ID during design
        - status (String): Instance runtime status
        - nodeID (String): Node ID where the instance runs

Example:
```json
{
    "services": [
        {
            "id": "a58ee3a7-62a0-46f3-ba80-f7080eaa0d1c",
            "name": "LLM agent",
            "description": "LLM inference service for natural language tasks.",
            "owner": "NEC Corp.",
            "instances": [
                {
                    "serviceInstanceID": "5b4ea1a2-4130-4de8-9045-bc92709df778",
                    "requestInstanceID": "1d40d2a9-979f-4956-aee7-30587de64fe9",
                    "status": "RUNNING",
                    "nodeID": "64ee5ed7-8897-4b6c-bdcf-9a902a276f32"
                }
            ]
        }
    ]
}
```

</details>

## All Resources (`resources`)

Performance information for all resources.
The structure and parameters differ by device type (CPU, memory, storage, etc.).

<details>
<summary>Show details for common data</summary>

Common structure and meaning across device types:

- resources (ObjectList): List of resource performance data
    - resourceGroupIDs (StringList): IDs of resource groups each device belongs to
    - detected (bool): Detection flag (true: detected, false: not detected)
    - deviceUnit (Object): Device unit information
        - annotation (Object): Additional information about the device unit
            - systemItems (Object): Additional system info
                - available (Object): Availability flag (true: usable in design, false: not usable)
    - device (Object): Device-specific performance info (see device-specific details below)

Example:
```json
{
    "resources": [
        {
            "resourceGroupIDs": ["625d8951-50fb-41b3-a824-6c98438c4c52"],
            "detected": true,
            "deviceUnit": {
                "annotation": {
                    "systemItems": {
                        "available": true
                    }
                }
            },
            "device": <device-specific info>
        }
    ]
}
```

</details>

<details>
<summary>Show details for CPU/GPU</summary>

- device (Object): Device performance
    - deviceID (String): Device ID
    - type (String): Device type
    - model (String): Model number
    - processorArchitecture (String): Processor architecture
    - totalEnabledCores (Number): Enabled core count
    - operatingSpeedMHz (Number): Clock speed (MHz)
    - status (Object): 
        - state (String): Device state
        - health (String): Health state
    - links (ObjectList): Connected devices
        - type (String): Connected device type
        - deviceID (String): Connected device ID
    - constraints (Object): Connection constraints
        - nonRemovableDevices (ObjectList): Non-removable devices
            - deviceID (String): Device ID that cannot be disconnected
        - incompatibilities (ObjectList): Incompatible devices
            - type (String): Device type
            - model (String): Model

Example:
```json
{
    "device": {
        "deviceID": "c188e8bf-bef0-4465-97ff-6e9a14fedd02",
        "type": "CPU",
        "model": "Intel Xeon Gold 6526Y",
        "processorArchitecture": "x86",
        "totalEnabledCores": 16,
        "operatingSpeedMHz": 3600,
        "status": {
            "state": "Enabled",
            "health": "OK"
        },
        "links": [
            {"type": "memory", "deviceID": "3cd29852-38ff-4495-a048-7d8e2f57a294"},
            {"type": "storage", "deviceID": "f470464e-407d-4860-a1d9-c9cf621fb4a0"},
            {"type": "networkInterface", "deviceID": "1e7746fc-d96d-4d55-a47f-9c35f21d33b2"}
        ],
        "constraints": {
            "nonRemovableDevices": [{"deviceID": "3cd29852-38ff-4495-a048-7d8e2f57a294"}],
            "incompatibilities": [{"type": "memory", "model": "DDR4"}]
        }
    }
}
```

</details>

<details>
<summary>Show details for Memory</summary>

- device (Object): Device performance
    - deviceID (String): Device ID
    - type (String): Device type
    - model (String): Model
    - capacityMiB (Number): Capacity (MiB)
    - operatingSpeedMHz (Number): Speed (MHz)
    - status (Object): 
        - state (String): Device state
        - health (String): Health state
    - links (ObjectList): Connected devices
        - type (String): Connected device type
        - deviceID (String): Connected device ID
    - constraints (Object): Connection constraints
        - nonRemovableDevices (ObjectList): Non-removable devices
            - deviceID (String): Device ID that cannot be disconnected
        - incompatibilities (ObjectList): Incompatible devices
            - type (String): Device type
            - model (String): Model

Example:
```json
{
    "device": {
        "deviceID": "3cd29852-38ff-4495-a048-7d8e2f57a294",
        "type": "memory",
        "model": "DDR5",
        "capacityMiB": 16384,
        "operatingSpeedMHz": 3200,
        "status": {
            "state": "Enabled",
            "health": "OK"
        },
        "links": [
            {"type": "CPU", "deviceID": "c188e8bf-bef0-4465-97ff-6e9a14fedd02"},
            {"type": "storage", "deviceID": "f470464e-407d-4860-a1d9-c9cf621fb4a0"},
            {"type": "networkInterface", "deviceID": "1e7746fc-d96d-4d55-a47f-9c35f21d33b2"}
        ],
        "constraints": {
            "nonRemovableDevices": [{"deviceID": "c188e8bf-bef0-4465-97ff-6e9a14fedd02"}],
            "incompatibilities": [{"type": "CPU", "model": "Intel Core-i9 14900K"}]
        }
    }
}
```

</details>

<details>
<summary>Show details for Storage</summary>

- device (Object): Device performance
    - deviceID (String): Device ID
    - type (String): Device type
    - model (String): Model
    - volumeCapacityBytes (Number): Capacity (bytes)
    - driveCapableSpeedGbs (Number): I/O speed (Gbps)
    - status (Object): 
        - state (String): Device state
        - health (String): Health state
    - links (ObjectList): Connected devices
        - type (String): Connected device type
        - deviceID (String): Connected device ID
    - constraints (Object): Connection constraints
        - nonRemovableDevices (ObjectList): Non-removable devices
            - deviceID (String): Device ID that cannot be disconnected
        - incompatibilities (ObjectList): Incompatible devices
            - type (String): Device type
            - model (String): Model

Example:
```json
{
    "device": {
        "deviceID": "f470464e-407d-4860-a1d9-c9cf621fb4a0",
        "type": "storage",
        "model": "SSD-1TB",
        "volumeCapacityBytes": 1073741824000,
        "driveCapableGbs": 4294967296000,
        "status": {
            "state": "Enabled",
            "health": "OK"
        },
        "links": [
            {"type": "CPU", "deviceID": "c188e8bf-bef0-4465-97ff-6e9a14fedd02"},
            {"type": "memory", "deviceID": "3cd29852-38ff-4495-a048-7d8e2f57a294"},
            {"type": "networkInterface", "deviceID": "1e7746fc-d96d-4d55-a47f-9c35f21d33b2"}
        ],
        "constraints": {"nonRemovableDevices": [], "incompatibilities": []}
    }
}
```

</details>

<details>
<summary>Show details for Network Interface</summary>

- device (Object): Device performance
    - deviceID (String): Device ID
    - type (String): Device type
    - model (String): Model
    - bitRate (Number): Link speed (bps)
    - status (Object): 
        - state (String): Device state
        - health (String): Health state
    - links (ObjectList): Connected devices
        - type (String): Connected device type
        - deviceID (String): Connected device ID
    - constraints (Object): Connection constraints
        - nonRemovableDevices (ObjectList): Non-removable devices
            - deviceID (String): Device ID that cannot be disconnected
        - incompatibilities (ObjectList): Incompatible devices
            - type (String): Device type
            - model (String): Model

Example:
```json
{
    "device": {
        "deviceID": "1e7746fc-d96d-4d55-a47f-9c35f21d33b2",
        "type": "networkInterface",
        "model": "Intel Ethernet Connection l219-LM",
        "bitRate": 10995116277760,
        "status": {
            "state": "Enabled",
            "health": "OK"
        },
        "links": [
            {"type": "CPU", "deviceID": "c188e8bf-bef0-4465-97ff-6e9a14fedd02"},
            {"type": "memory", "deviceID": "3cd29852-38ff-4495-a048-7d8e2f57a294"},
            {"type": "storage", "deviceID": "f470464e-407d-4860-a1d9-c9cf621fb4a0"}
        ],
        "constraints": {"nonRemovableDevices": [], "incompatibilities": []}
    }
}
```

</details>

## All Nodes (`nodes`)

Configuration information for all nodes at execution time.

<details>
<summary>Show details for All Nodes</summary>

Structure and meaning of each item:

- nodes (ObjectList): List of nodes in the current configuration
  - id (String): Node ID
  - resources (ObjectList): Resources that make up the node
    - device (Object): Resource information
      - deviceID (String): Device ID
      - type (String): Device type (CPU/memory/storage/etc.)
      - status (Object): Device status
        - state (String): Device state
        - health (String): Health state
      - resourceGroupIDs (StringList): Resource group IDs assigned to the device
      - annotation (Object): Resource usability
        - available (bool): true=usable in layout design / false=disabled (not usable)

Example:
```json
{
    "nodes": [
        {
            "id": "64ee5ed7-8897-4b6c-bdcf-9a902a276f32",
            "resources": [
                {
                    "device": {
                        "deviceID": "c188e8bf-bef0-4465-97ff-6e9a14fedd02",
                        "type": "CPU",
                        "status": {"state": "Enabled", "health": "OK"},
                        "resourceGroupIDs": ["625d8951-50fb-41b3-a824-6c98438c4c52"],
                        "annotation": {"available": true}
                    }
                }
            ]
        }
    ]
}
```

</details>

## Design All Nodes Flag (`designAllNodes`)

Whether all nodes passed in All Nodes are in scope.
If `false`, [Target Node IDs](a01_Args_to_request_design_Function.md#target-node-ids-targetnodeids) contains the node IDs that are in scope.
If `true`, all nodes in [All Nodes](a01_Args_to_request_design_Function.md#all-nodes-nodes) are in scope.

<details>
<summary>Show details for Design All Nodes Flag</summary>

- designAllNodes (bool): Whether all nodes are in scope

Example:
```json
{
    "designAllNodes": true
}
```

</details>

## Partial Design Flag (`partialDesign`)

Whether only specified services/nodes are in scope (partial design) or all services/nodes are in scope (entire design).
If `false`, all services/nodes are in scope (entire design).
If `true`, only the specified services/nodes are in scope (partial design).

<details>
<summary>Show details for Partial Design Flag</summary>

- partialDesign (bool): Whether partial or entire design

Example:
```json
{
    "partialDesign": true
}
```

</details>

## Skip Migration Condition Flag (`noCondition`)

Whether migration conditions are unnecessary as part of the design result.
If `true`, return an empty object for [Conditions](a02_Return_Value_from_get_design.md#conditions-conditions) in [Appendix 2. Return Value of get_design](a02_Return_Value_from_get_design.md).
If `false`, return [Conditions](a02_Return_Value_from_get_design.md#conditions-conditions).

<details>
<summary>Show details for Skip Migration Condition Flag</summary>

- noCondition (bool): Whether to skip calculating migration conditions

Example:
```json
{
    "noCondition": false
}
```

</details>

## Policies (`policies`)

Policies for resource selection during layout design.

<details>
<summary>Show details for Policies</summary>

Structure and meaning of each item:

- policies (Object): Resource selection constraints
  - nodeConfigurationPolicy (Object): Node composition constraints (limits on numbers of connected devices)
    - hardwareConnectionsLimit (Object): Hardware connection limits
      - <device type> (Object): Device type (CPU/memory/storage/etc.)
        - minNum (Number): Minimum number of devices connected to a node
        - maxNum (Number): Maximum number of devices connected to a node
  - systemOperationPolicy (Object): System operation constraints (system requirements)
    - useThreshold (Object): Resource usage threshold when deploying services on a node
      - <device type> (Object): Device type (CPU/memory/storage/etc.)
        - value (Number): Threshold value
        - unit (String): Unit of the threshold
        - comparison (String): Comparator applied to the threshold

Example:
```json
{
    "policies": {
        "nodeConfigurationPolicy": {
            "hardwareConnectionsLimit": {
                "memory": {"minNum": 1, "maxNum": 4}
            }
        },
        "systemOperationPolicy": {
            "useThreshold": {
                "cpu": {"value": 80, "unit": "percent", "comparison": "lt"}
            }
        }
    }
}
```

The example above means:
- nodeConfigurationPolicy: The number of memory devices per node must be between 1 and 4.
- systemOperationPolicy: CPU usage on nodes where services run must be 80% or less.

</details>
