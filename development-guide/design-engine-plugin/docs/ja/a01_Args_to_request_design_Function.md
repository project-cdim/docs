# 付録1. request_design関数へ渡される引数

## 要求ID (```requestID```)

要求IDは、構成案設計機能の呼び出し元で管理する構成案設計要求を識別するためのIDです。

<details>
<summary>要求IDの詳細情報を表示</summary>

- requestID (String) : 構成案設計要求を識別するためのID

データ例:
```json
{
    "requestID": "463e79c1-d138-4748-9018-5c1435a50d87"
}
```

</details>

## 再設計対象ノード一覧 (```targetNodeIDs```)

再設計対象ノード一覧は、全ノード一覧のうち設計対象となるノードのノードIDの一覧です。
全体設計の場合 ([部分設計フラグ](a01_Args_to_request_design_Function.md#部分設計フラグ-partialdesign)がfalseの場合)、再設計対象ノード一覧は空のリストが指定されます。

<details>
<summary>再設計対象ノード一覧の詳細情報を表示</summary>

- targetNodeIDs (StringList) : 設計対象のノードIDの一覧

データ例:
```json
{
    "targetNodeIDs": ["9158d69e-abca-4ef1-929b-78424b01005b"]
}
```

</details>

## サービスセット要求リソース (```serviceSetRequestResources```)

サービスセット要求リソースは、サービスが要求するリソース種別と性能情報です。

<details>
<summary>サービスセット要求リソースの詳細情報を表示</summary>

以下は、サービスセット要求リソースの構造と各項目の意味を階層構造で示したものです。

- serviceSetRequestResources (ObjectList) : サービスセットが必要とするリソース
    - id (String): 個々のサービスセット要求リソースID
    - serviceSetID (String) : サービスセットID
    - serviceSetName (String) : サービスセット名
    - serviceRequestResources (ObjectList) : サービスセットに含まれるサービスが必要とするリソース
        - id (String) : 個々のサービス要求リソースID
        - serviceID (String) : サービスID
        - serviceName (String) : サービス名
        - shareService (bool) : 当該サービスが他サービスとノードを共有することができるかを示すフラグ (true: 共有、false: 専有)
        - resources (Object) : サービスの実行に必要なデバイスとその性能情報
            - operatingSystem (String) : 使用OS
            - instances (ObjectList) : サービスインスタンスごとに必要なデバイスとその性能情報
                - requestInstanceID (String) : 設計時にサービスインスタンスを識別するID
                - serviceInstanceID (String) : サービス配備後にサービスインスタンスを識別するID
                - redundant (bool) : 当該サービスインスタンスが予備インスタンスか否かを示すフラグ (true: 予備インスタンス、false: 通常インスタンス)
                - changed (bool) : 部分設計時に当該インスタンスを再設計するか否かを示すフラグ (true: 再設計する、false: 再設計しない)
                - cpu (Object) : 要求するCPUのデバイス性能
                    - architecture (String) : CPUのアーキテクチャ
                    - coreNumber (Number) : CPUコア数
                    - operatingSpeedMHz (Number) : CPU動作周波数 (MHz)
                - memory (Object) : 要求するメモリのデバイス性能
                    - size (Number) : メモリサイズ (MB)
                    - operatingSpeedMHz (Number) : メモリ動作周波数 (MHz)
                - storage (Object) : 要求するストレージのデバイス性能
                    - size (Number) : ストレージサイズ (GB)
                    - capableSpeedGbs (Number) : ストレージコントローラとの通信速度 (Gbit/s)
                - gpu (ObjectList) : 要求するGPUのデバイス性能
                    - architecture (String) : GPUのアーキテクチャ
                    - coreNumber (Number) : GPUコア数
                    - operatingSpeedMHz (Number) : GPU動作周波数 (MHz)
                    - memorySize (Number) : GPUメモリサイズ (MB)
                    - deviceCount (Number) : GPUの要求デバイス数
                - networkInterface (Object) : 要求するネットワークインターフェースのデバイス性能
                    - bitRate (Number) : ネットワークインターフェースの通信速度 (Mbit/s)

データ例:
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

## 設計対象サービス一覧 (```services```)

設計対象サービス一覧は、設計の対象となるサービスの定義情報の一覧です。

<details>
<summary>設計対象サービス一覧の詳細情報を表示</summary>

以下は、設計対象サービス一覧の構造と各項目の意味を階層構造で示したものです。

- services (ObjectList) : 設計対象のサービスの定義情報の一覧
    - id (String) : サービスID
    - name (String) : サービス名
    - description (String) : サービスの説明
    - owner (String) : サービスの所有者
    - instances (ObjectList) : 現行構成で稼働中のサービスインスタンス情報
        - serviceInstanceID (String) : サービス配備後にサービスインスタンスを識別するID
        - requestInstanceID (String) : 設計時にサービスインスタンスを識別するID
        - status (String) : サービスインスタンスの稼働状態
        - nodeID (String) : サービスインスタンスが稼働しているノードID

データ例:
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

## 全リソース一覧 (```resources```)

全リソース一覧情報は、全リソースの性能情報です。  
CPUやメモリなど、デバイス種別によってデータ構造やパラメータが異なります。

<details>
<summary>共通データの詳細情報を表示</summary>

以下は、全デバイス種別で共通の構造と各項目の意味を階層構造で示したものです。

- resources (ObjectList) : リソース性能情報の一覧
    - resourceGroupIDs (StringList) : 各デバイスが属しているリソースグループIDの一覧
    - detected (bool) : デバイスの検出状態フラグ (true: 検出済み、false: 検出不可)
    - deviceUnit (Object) : デバイスユニット情報
        - annotation (Object) : デバイスユニットの付加情報
            - systemItems (Object) : デバイスユニットのシステム情報に関する付加情報
                - available (Object) : デバイスの利用可否フラグ (true: 構成案の設計に利用可能、false: 構成案の設計に利用不可)
    - device (Object) : デバイス種別に固有の性能情報 (詳細は以下のデバイスごとの詳細情報を参照)

データ例:
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
            "device": <デバイス種別に固有の性能情報>
        }
    ]
}
```

</details>

<details>
<summary>CPU/GPUの詳細情報を表示</summary>

以下は、CPUおよびGPUの構造と各項目の意味を階層構造で示したものです。

- device (Object) : デバイスの性能情報
    - deviceID (String) : デバイスID
    - type (String) : デバイス種別
    - model (String) : デバイスの型番
    - processorArchitecture (String) : プロセッサーのアーキテクチャ
    - totalEnabledCores (Number) : プロセッサーの有効なコア数
    - operatingSpeedMHz (Number) : プロセッサーの動作周波数 (MHz)
    - status (Object) : 
        - state (String) : デバイスの状態
        - health (String) : デバイスのヘルス状態
    - links (ObjectList) : 当該デバイスに接続された他デバイスの情報
        - type (String) : 接続されているデバイスの種別
        - deviceID (String) : 接続されているデバイスのデバイスID
    - constraints (Object) : デバイスの接続制約
        - nonRemovableDevices (ObjectList) : 切断不可デバイスの情報
            - deviceID (String) : 当該デバイスから切断ができないデバイスのデバイスID
        - incompatibilities (ObjectList) : 接続不可デバイスの情報
            - type (String) : 接続できないデバイスの種別
            - model (String) : 接続できないデバイスの型番

データ例:
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
            {
                "type": "memory",
                "deviceID": "3cd29852-38ff-4495-a048-7d8e2f57a294"
            },
            {
                "type": "storage",
                "deviceID": "f470464e-407d-4860-a1d9-c9cf621fb4a0"
            },
            {
                "type": "networkInterface",
                "deviceID": "1e7746fc-d96d-4d55-a47f-9c35f21d33b2"
            }
        ],
        "constraints": {
            "nonRemovableDevices": [
                {
                    "deviceID": "3cd29852-38ff-4495-a048-7d8e2f57a294"
                }
            ],
            "incompatibilities": [
                {
                    "type": "memory",
                    "model": "DDR4"
                }
            ]
        }
    }
}
```

</details>

<details>
<summary>メモリの詳細情報を表示</summary>

以下は、メモリと各項目の意味を階層構造で示したものです。

- device (Object) : デバイスの性能情報
    - deviceID (String) : デバイスID
    - type (String) : デバイス種別
    - model (String) : デバイスの型番
    - capacityMiB (Number) : メモリの容量 (MiB)
    - operatingSpeedMHz (Number) : メモリの動作周波数 (MHz)
    - status (Object) : 
        - state (String) : デバイスの状態
        - health (String) : デバイスのヘルス状態
    - links (ObjectList) : 当該デバイスに接続された他デバイスの情報
        - type (String) : 接続されているデバイスの種別
        - deviceID (String) : 接続されているデバイスのデバイスID
    - constraints (Object) : デバイスの接続制約
        - nonRemovableDevices (ObjectList) : 切断不可デバイスの情報
            - deviceID (String) : 当該デバイスから切断ができないデバイスのデバイスID
        - incompatibilities (ObjectList) : 接続不可デバイスの情報
            - type (String) : 接続できないデバイスの種別
            - model (String) : 接続できないデバイスの型番

データ例:
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
            {
                "type": "CPU",
                "deviceID": "c188e8bf-bef0-4465-97ff-6e9a14fedd02"
            },
            {
                "type": "storage",
                "deviceID": "f470464e-407d-4860-a1d9-c9cf621fb4a0"
            },
            {
                "type": "networkInterface",
                "deviceID": "1e7746fc-d96d-4d55-a47f-9c35f21d33b2"
            }
        ],
        "constraints": {
            "nonRemovableDevices": [
                {
                    "deviceID": "c188e8bf-bef0-4465-97ff-6e9a14fedd02"
                }
            ],
            "incompatibilities": [
                {
                    "type": "CPU",
                    "model": "Intel Core-i9 14900K"
                }
            ]
        }
    }
}
```

</details>

<details>
<summary>ストレージの詳細情報を表示</summary>

以下は、CPUおよびGPUの構造と各項目の意味を階層構造で示したものです。

- device (Object) : デバイスの性能情報
    - deviceID (String) : デバイスID
    - type (String) : デバイス種別
    - model (String) : デバイスの型番
    - volumeCapacityBytes (Number) : ストレージ容量 (B)
    - driveCapableSpeedGbs (Number) : データのI/O速度 (Gbps)
    - status (Object) : 
        - state (String) : デバイスの状態
        - health (String) : デバイスのヘルス状態
    - links (ObjectList) : 当該デバイスに接続された他デバイスの情報
        - type (String) : 接続されているデバイスの種別
        - deviceID (String) : 接続されているデバイスのデバイスID
    - constraints (Object) : デバイスの接続制約
        - nonRemovableDevices (ObjectList) : 切断不可デバイスの情報
            - deviceID (String) : 当該デバイスから切断ができないデバイスのデバイスID
        - incompatibilities (ObjectList) : 接続不可デバイスの情報
            - type (String) : 接続できないデバイスの種別
            - model (String) : 接続できないデバイスの型番

データ例:
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
            {
                "type": "CPU",
                "deviceID": "c188e8bf-bef0-4465-97ff-6e9a14fedd02"
            },
            {
                "type": "memory",
                "deviceID": "3cd29852-38ff-4495-a048-7d8e2f57a294"
            },
            {
                "type": "networkInterface",
                "deviceID": "1e7746fc-d96d-4d55-a47f-9c35f21d33b2"
            }
        ],
        "constraints": {
            "nonRemovableDevices": [],
            "incompatibilities": []
        }
    }
}
```

</details>

<details>
<summary>ネットワークインターフェースの詳細情報を表示</summary>

以下は、CPUおよびGPUの構造と各項目の意味を階層構造で示したものです。

- device (Object) : デバイスの性能情報
    - deviceID (String) : デバイスID
    - type (String) : デバイス種別
    - model (String) : デバイスの型番
    - bitRate (Number) : データ転送速度 (bps)
    - status (Object) : 
        - state (String) : デバイスの状態
        - health (String) : デバイスのヘルス状態
    - links (ObjectList) : 当該デバイスに接続された他デバイスの情報
        - type (String) : 接続されているデバイスの種別
        - deviceID (String) : 接続されているデバイスのデバイスID
    - constraints (Object) : デバイスの接続制約
        - nonRemovableDevices (ObjectList) : 切断不可デバイスの情報
            - deviceID (String) : 当該デバイスから切断ができないデバイスのデバイスID
        - incompatibilities (ObjectList) : 接続不可デバイスの情報
            - type (String) : 接続できないデバイスの種別
            - model (String) : 接続できないデバイスの型番

データ例:
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
            {
                "type": "CPU",
                "deviceID": "c188e8bf-bef0-4465-97ff-6e9a14fedd02"
            },
            {
                "type": "memory",
                "deviceID": "3cd29852-38ff-4495-a048-7d8e2f57a294"
            },
            {
                "type": "storage",
                "deviceID": "f470464e-407d-4860-a1d9-c9cf621fb4a0"
            }
        ],
        "constraints": {
            "nonRemovableDevices": [],
            "incompatibilities": []
        }
    }
}
```

</details>

## 全ノード一覧 (```nodes```)

全ノード一覧情報は、実行時点での全ノードの構成情報です。

<details>
<summary>全ノード一覧の詳細情報を表示</summary>

以下は、全ノード一覧情報の構造と各項目の意味を階層構造で示したものです。

- nodes（ObjectList）: 現行構成のノード一覧情報
	- id（String）: ノードID
	- resources（ObjectList）: ノードを構成する各リソースの情報
		- device（Object）: リソース情報
			- deviceID（String）: デバイスID
			- type（String）: デバイス種別 (CPU/メモリ/ストレージ/etc...)
			- status（Object）: デバイスの状態
				- state（String）: デバイスの状態
				- health（String）: デバイスのヘルス状態
			- resourceGroupIDs（StringList）: 当該デバイスに割り当てられたリソースグループID
			- annotation（Object）: リソースの利用可不可
				- available（bool）: true=構成案設計に利用可能 / false=無効化（利用不可）

データ例:
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
                        "status": {
                            "state": "Enabled",
                            "health": "OK"
                        },
                        "resourceGroupIDs": ["625d8951-50fb-41b3-a824-6c98438c4c52"],
                        "annotation": {
                            "available": true
                        }
                    }
                }
            ]
        }
    ]
}
```

</details>

## 全ノード対象フラグ (```designAllNodes```)

全ノード対象フラグは、全ノード一覧で渡された全ノードを設計対象とするフラグです。  
本フラグが```false```の場合、[再設計対象ノード一覧](a01_Args_to_request_design_Function.md#再設計対象ノード一覧-targetnodeids)で設計対象となるノードIDの一覧が渡されます。
本フラグが```true```の場合、[全ノード一覧](a01_Args_to_request_design_Function.md#全ノード一覧-nodes)に含まれる全ノードが設計対象になります。

<details>
<summary>全ノード対象フラグの詳細情報を表示</summary>

- designAllNodes (bool) : 全ノードが設計対象か否かを示すフラグ

データ例:
```json
{
    "designAllNodes": true
}
```

</details>

## 部分設計フラグ (```partialDesign```)

部分設計フラグは、指定されたサービス/ノードのみが設計対象となる部分設計か、すべてのサービス/ノードが設計対象となる全体設計かを示すフラグです。  
本フラグが```false```の場合、全てのサービス/ノードが設計対象となる全体設計になります。
本フラグが```true```の場合、指定されたサービス/ノードのみが設計対象となる部分設計になります。

<details>
<summary>部分設計フラグの詳細情報を表示</summary>

- partialDesign (bool) : 部分設計か、全体設計かを示すフラグ

データ例:
```json
{
    "partialDesign": true
}
```

</details>

## 移行条件スキップフラグ (```noCondition```)

移行条件スキップフラグは、構成案の設計結果として移行条件が不要であることを示すフラグです。  
本フラグが```true```の場合、[付録2. get_design関数から返却される戻り値](a02_Return_Value_from_get_design.md)のうち、[移行条件](a02_Return_Value_from_get_design.md#移行条件-conditions)を空オブジェクトで返却します。
本フラグが```false```の場合、[移行条件](a02_Return_Value_from_get_design.md#移行条件-conditions)を返却します。

<details>
<summary>移行条件スキップフラグの詳細情報を表示</summary>

- noCondition (bool) : 移行条件の算出をスキップするか否かを制御するフラグ

データ例:
```json
{
    "noCondition": false
}
```

</details>

## 制約条件一覧 (```policies```)

制約条件一覧は、構成案の設計時のリソース選定に関する制約事項の一覧です。

<details>
<summary>制約条件一覧の詳細情報を表示</summary>

以下は、制約条件一覧の構造と各項目の意味を階層構造で示したものです。

- policies (Object) : リソース選定の制約事項の一覧
    - nodeConfigurationPolicy (Object) : ノード構成制約 (リソースの接続可能数に関する制約)
        - hardwareConnectionsLimit (Object) : ハードウェア接続制限
            - <デバイス種別> (Object): デバイス種別 (CPU/メモリ/ストレージ/etc...)
                - minNum (Number) : ノードに接続する最小数
                - maxNum (Number) : ノードに接続する最大数
    - systemOperationPolicy (Object) : システム運用制約 (システム要件)
        - useThreshold (Object) : サービスをノードにデプロイした際のリソースの使用率のしきい値
            - <デバイス種別> (Object): デバイス種別 (CPU/メモリ/ストレージ/etc...)
                - value (Number) : しきい値
                - unit (String) : しきい値の単位
                - comparison (String) : しきい値に対する不等号

データ例:
```json
{
    "policies": {
        "nodeConfigurationPolicy": {
            "hardwareConnectionsLimit": {
                "memory": {
                    "minNum": 1,
                    "maxNum": 4
                }
            }
        },
        "systemOperationPolicy": {
            "useThreshold": {
                "cpu": {
                    "value": 80,
                    "unit": "percent",
                    "comparison": "lt"
                }
            }
        }
    }
}
```

上記の制約条件一覧のデータ例は以下の意味を持ちます。
- nodeConfigurationPolicy: 1ノードに接続するメモリのデバイス数は1以上4以下であること
- systemOperationPolicy: サービスが稼働するノードのCPU使用率が80%以下であること

</details>