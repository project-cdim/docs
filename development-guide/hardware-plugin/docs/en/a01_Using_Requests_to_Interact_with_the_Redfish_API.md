# Appendix 1. Using Requests to interact with the Redfish API

When implementing the plugin, you can use [Requests](https://requests.readthedocs.io/en/latest/) as a REST API client.  
This chapter describes a simple example of using Requests to run the Redfish API.  
The complete sample is available in [restclt.py](../../samples/oob-sample-plugin/oob_sample/restclt.py).

Create a RestClient class.

``` python
import requests
import pprint

class RestClient:
    def __init__(self, base_url: str, timeout: float) -> None:
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout

    def get(self, uri: str) -> dict:
        response = requests.get(f"{self.base_url}/{uri}", timeout=self.timeout)
        response.raise_for_status()
        return response.json()

    def post(self, uri: str, data: dict) -> dict:
        # ...(omitted)...
```

Create a RestClient instance.  
Here, the base URL of the Redfish API is `http://localhost:5000` and the timeout is 60 seconds.

``` python
rest_clt = RestClient(base_url="http://localhost:5000", timeout=60)
```

Processor resource and print it to the console.

``` python
processor = rest_clt.get("/redfish/v1/Chassis/Chassis-1/Processors/PROC-0001")
pprint(processor)
```

Output:

``` python
{'@odata.context': '/redfish/v1/$metadata#Processor.Processor',
 '@odata.id': '/redfish/v1/Chassis/Chassis-1/Processors/PROC-0001',
 '@odata.type': '#Processor.1_0_0.Processor',
 'Actions': {'#Processor.Reset': {'ResetType@Redfish.AllowableValues': ['On',
                                                                        'ForceOff',
                                                                        'GracefulShutdown',
                                                                        'GracefulRestart',
                                                                        'ForceRestart',
                                                                        'ForceOn'],
                                  'target': '/redfish/v1/Chassis/Chassis-1/Processors/PROC-0001/Actions/Processor.Reset'},
             'Oem': {'#Processor.MetricState': {'StateType@Redfish.AllowableValues': ['off',
                                                                                      'steady',
                                                                                      'low',
                                                                                      'high',
                                                                                      'action'],
                                                'target': '/redfish/v1/Chassis/Chassis-1/Processors/PROC-0001/Actions/Processor.MetricState'}}},
 'BaseSpeedMHz': 1200,
 'EnvironmentMetrics': {'@odata.id': '/redfish/v1/Chassis/Chassis-1/Processors/PROC-0001/EnvironmentMetrics'},
 'Id': 'PROC-0001',
 'InstructionSet': 'x86-64',
 'MemorySummary': {'ECCModeEnabled': True,
                   'MemoryMirroring': None,
                   'Metrics': {'@odata.id': '{rb}{suffix}/{suffix_id}/Memory/{memory_id}/MemoryMetrics'},
                   'Status': {},
                   'TotalCacheSizeMiB': 4096,
                   'TotalMemorySizeMiB': 8192},
# ... (omitted) ...
```

Prints the base clock and memory size to the console.

``` python
print(f"BaseSpeedMHz = {processor['BaseSpeedMHz']}")
print(f"TotalMemorySizeMiB = {processor['MemorySummary']['TotalMemorySizeMiB']}")
```

Output:

``` python
BaseSpeedMHz = 1200
TotalMemorySizeMiB = 8192
```
