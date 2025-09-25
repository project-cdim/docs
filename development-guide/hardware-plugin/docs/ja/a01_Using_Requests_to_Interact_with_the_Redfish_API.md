# 付録1. RequestsによるRedfish APIの実行

プラグインを実装する際、REST APIクライアントとして[Requests](https://requests.readthedocs.io/en/latest/)を使用することができます。  
本章でRequestsを使用してRedfish APIを実行する簡単な例を示します。  
完全なサンプルは[restclt.py](../../samples/oob-sample-plugin/oob_sample/restclt.py)を参照してください。

RestClientクラスを作成します。

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
        # ...(省略)...
```

RestClientインスタンスを作成します。  
ここではRedfish APIのベースURLを`http://localhost:5000`、タイムアウトを60秒としています。

``` python
rest_clt = RestClient(base_url="http://localhost:5000", timeout=60)
```

Processorリソースを取得してコンソールに出力します。

``` python
processor = rest_clt.get("/redfish/v1/Chassis/Chassis-1/Processors/PROC-0001")
pprint(processor)
```

出力:

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
# ... (以下省略) ...
```

ベースクロックとメモリサイズをコンソールに出力します。

``` python
print(f"BaseSpeedMHz = {processor['BaseSpeedMHz']}")
print(f"TotalMemorySizeMiB = {processor['MemorySummary']['TotalMemorySizeMiB']}")
```

出力:

``` python
BaseSpeedMHz = 1200
TotalMemorySizeMiB = 8192
```
