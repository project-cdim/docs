# Appendix 2. Return Value of `get_design`

## Design Status (`status`)

The status string indicating the execution state of the layout design.

<details>
<summary>Show details for Design Status</summary>

- status (String): Design status

Available values:

| Status | Overview |
| --- | --- |
| IN_PROGRESS | Design in progress |
| COMPLETED | Design completed |
| FAILED | Design failed |
| CANCELING | Canceling the design process |
| CANCELED | Cancellation completed |

Example:
```json
{
    "status": "COMPLETED"
}
```

</details>

## Request ID (`requestID`)

The request ID used by the caller to identify the layout design request.
Return the [input request ID](a01_Args_to_request_design_Function.md#request-id-requestid) as-is.

<details>
<summary>Show details for Request ID</summary>

- requestID (String): ID used by the caller to identify the layout design request

Example:
```json
{
    "requestID": "463e79c1-d138-4748-9018-5c1435a50d87"
}
```

</details>

## Started At (`startedAt`)

The timestamp (string) when the plugin/engine started the design process.

<details>
<summary>Show details for Started At</summary>

- startedAt (String): Time when the plugin/engine started processing (ISO 8601 UTC)

Example:
```json
{
    "startedAt": "2026-01-01T00:00:00.000000Z"
}
```

</details>

## Ended At (`endedAt`)

The timestamp (string) when the plugin/engine ended the design process.

<details>
<summary>Show details for Ended At</summary>

- endedAt (String): Time when the plugin/engine finished processing (ISO 8601 UTC)

Example:
```json
{
    "endedAt": "2026-01-01T00:00:00.000000Z"
}
```

</details>

## Design (`design`)

A node layout plan created from the input data.

<details>
<summary>Show details for Design</summary>

Structure and meaning of each item:

- design (Object): The resulting layout plan
    - nodes (ObjectList): List of node layout plans to run services
        - services (ObjectList): Services to run on the node
            - id (String): Service ID
            - requestInstanceID (String): ID of the service instance during design
        - device (Object): Devices that make up the node
            - cpu (Object): CPU devices assigned to the node
                - deviceIDs (StringList): CPU device IDs
            - memory (Object): Memory devices assigned to the node
                - deviceIDs (StringList): Memory device IDs
            - storage (Object): Storage devices assigned to the node
                - deviceIDs (StringList): Storage device IDs
            - gpu (ObjectList): GPU devices assigned to the node
                - deviceID (String): GPU device ID
                - requests (Object): Instance information for the assigned device
                    - requestInstanceID (String): ID of the service instance during design
                    - index (Number): Assignment index
            - networkInterface (Object): NICs assigned to the node
                - deviceIDs (StringList): NIC device IDs
        - spec (Number): Total memory capacity assigned to the node (MB)
        - averageEnergyWatts (Number): Estimated average energy consumption (W)
        - constructTime (Number): Time to construct the node (s)
        - destructTime (Number): Time to deconstruct the node (s)

Example:
```json
{
    "design": {
        "nodes": [
            {
                "services": [
                    {"id": "a58ee3a7-62a0-46f3-ba80-f7080eaa0d1c", "requestInstanceID": "1d40d2a9-979f-4956-aee7-30587de64fe9"}
                ],
                "device": {
                    "cpu": {"deviceIDs": ["c188e8bf-bef0-4465-97ff-6e9a14fedd02"]},
                    "memory": {"deviceIDs": ["3cd29852-38ff-4495-a048-7d8e2f57a294"]},
                    "storage": {"deviceIDs": ["f470464e-407d-4860-a1d9-c9cf621fb4a0"]},
                    "gpu": [
                        {
                            "deviceID": "63ccc12d-d10c-4d2a-949f-7a732bbe4710",
                            "requests": {"requestInstanceID": "1d40d2a9-979f-4956-aee7-30587de64fe9", "index": 0}
                        }
                    ],
                    "networkInterface": {"deviceIDs": ["1e7746fc-d96d-4d55-a47f-9c35f21d33b2"]}
                },
                "spec": 16384,
                "averageEnergyWatts": 500,
                "constructTime": 60,
                "destructTime": 60
            }
        ]
    }
}
```

</details>

## Conditions (`conditions`)

Constraints on node load tolerated when migrating from the current node configuration to the designed layout plan.

<details>
<summary>Show details for Conditions</summary>

Structure and meaning of each item:

- conditions (Object): Migration conditions
    - toleranceCriteria (Object): Load tolerance criteria
        - cpu (ObjectList): Per-node CPU tolerance
            - deviceIDs (StringList): CPU device IDs connected to the node
            - limit (Object): Usage limit info
                - weights (NumberList): Weights for calculating CPU utilization considering core counts
                - averageUseRate (Number): Upper bound for average CPU utilization
        - memory (ObjectList): Per-node memory tolerance
            - deviceIDs (StringList): Memory device IDs connected to the node
            - limit (Object): Usage limit info
                - averageUseBytes (Number): Upper bound for average memory usage (MB)
    - energyCriteria (Number): Upper bound of average system-wide energy consumption (W)

Example:
```json
{
    "conditions": {
        "toleranceCriteria": {
            "cpu": [
                {
                    "deviceIDs": ["c188e8bf-bef0-4465-97ff-6e9a14fedd02"],
                    "limit": {"weights": [1.0], "averageUseRate": 80}
                }
            ],
            "memory": [
                {
                    "deviceIDs": ["3cd29852-38ff-4495-a048-7d8e2f57a294"],
                    "limit": {"averageUseBytes": 12000}
                }
            ]
        },
        "energyCriteria": 600
    }
}
```

</details>

## Procedures (`procedures`)

Steps to migrate from the current node configuration to the designed layout plan.

<details>
<summary>Show details for Procedures</summary>

Structure and meaning of each item:

- procedures (ObjectList): Migration procedures
    - operationID (Number): Operation ID
    - operation (String): Operation type
    - targetCPUID (String): Target CPU device ID
    - targetDeviceID (String): Target device ID
    - targetRequestInstanceID (String): Target service instance ID during design
    - dependencies (NumberList): List of dependent operation IDs

Available operations:

| operation | Overview |
| --- | --- |
| boot | Boot a device |
| shutdown | Stop a device |
| connect | Connect a CPU and another device |
| disconnect | Disconnect a CPU and another device |
| start | Start a service instance |
| stop | Stop a service instance |

Example:
```json
{
    "procedures": [
        {
            "operationID": 1, 
            "operation": "stop", 
            "targetCPUID": "c188e8bf-bef0-4465-97ff-6e9a14fedd02", 
            "targetRequestInstanceID": "1d40d2a9-979f-4956-aee7-30587de64fe9", 
            "dependencies": [6]
        },
        {
            "operationID": 2, 
            "operation": "shutdown", 
            "targetCPUID": "c188e8bf-bef0-4465-97ff-6e9a14fedd02", 
            "dependencies": [1]
        },
        {
            "operationID": 3, 
            "operation": "disconnect", 
            "targetCPUID": "c188e8bf-bef0-4465-97ff-6e9a14fedd02", 
            "targetDeviceID": "f470464e-407d-4860-a1d9-c9cf621fb4a0", 
            "dependencies": [2]
        },
        {
            "operationID": 4, 
            "operation": "connect", 
            "targetCPUID": "c188e8bf-bef0-4465-97ff-6e9a14fedd02", 
            "targetDeviceID": "03eb1b44-d8fd-4a65-a5c2-1c0de9aa03b6", 
            "dependencies": []
        },
        {
            "operationID": 5,
            "operation": "boot", 
            "targetCPUID": "c188e8bf-bef0-4465-97ff-6e9a14fedd02", 
            "dependencies": [4]
        },
        {
            "operationID": 6, 
            "operation": "start", 
            "targetCPUID": "c188e8bf-bef0-4465-97ff-6e9a14fedd02", 
            "targetRequestInstanceID": "1d40d2a9-979f-4956-aee7-30587de64fe9", 
            "dependencies": [5]
        }
    ]
}
```

</details>

## Failure Cause (`cause`)

A message indicating why the layout design failed (when status is FAILED).

<details>
<summary>Show details for Failure Cause</summary>

- cause (String): Reason for failure

Example:
```json
{
    "cause": "Design request needs more available CPUs."
}
```

The example above indicates insufficient available CPUs for the layout design.

</details>
