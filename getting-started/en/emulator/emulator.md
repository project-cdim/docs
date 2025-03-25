# Install the Emulator

## 1. Prerequisites

- Docker
- Git

## 2. Create a Docker Network

Create a Docker network that will be used by CDIM and the emulator.

```sh
docker network create cdim-net
```

## 3. Build the Emulator

Retrieve the emulator.

```sh
git clone --recursive https://github.com/project-cdim/hw-emulator-reference-compose.git
```

Execute the following commands to build and start the emulator.

```sh
cd hw-emulator-reference-compose
docker compose up -d --build
```

## 4. Verify Emulator Operation

Enter the container using the following command.

```sh
docker container exec -it hw-emulator bash
```

Execute the following within the container.

```sh
curl http://localhost:5000/redfish/v1/Systems/System-1/Processors | python -m json.tool
```

If you receive a response like the one below, it is operating correctly.

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
