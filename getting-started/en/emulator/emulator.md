# Install the Emulator

## 1. Build the Emulator

Retrieve the emulator.

```sh
git clone --recursive https://github.com/project-cdim/hw-emulator-reference-compose.git
```

Execute the following commands to build and start the emulator.

```sh
cd hw-emulator-reference-compose
docker compose up -d --build
```

## 2. Verify Emulator Operation

Execute the following command.

```sh
docker exec hw-emulator curl http://localhost:5000/redfish/v1/Systems/System-1/Processors | python -m json.tool
```

If you receive a response similar to the one below, the emulator is operating correctly.

```json
{
    "@odata.context": "/redfish/v1/$metadata#ProcessorCollection.ProcessorCollection",
    "@odata.id": "/redfish/v1/Systems/System-1/Processors",
    "@odata.type": "#ProcessorCollection.ProcessorCollection",
    "Members": [
        {
            "@odata.id": "/redfish/v1/Systems/System-1/Processors/PROC-0001"
        }
    ],
    "Members@odata.count": 1,
    "Name": "Processors Collection"
}
```

[Next step: Install CDIM](../install/install.md)
