# 付録2. get_design関数から返却される戻り値

## 設計状態 (```status```)

設計状態は、構成案の設計の実行状態を示す文字列です。

<details>
<summary>設計状態の詳細情報を表示</summary>

- status (String) : 設計状態

設計状態として以下の5つがあります。

| 設計状態 | 概要 |
| --- | --- |
| IN_PROGRESS | 設計実行中 |
| COMPLETED | 設計完了 |
| FAILED | 設計失敗 |
| CANCELING | 設計処理キャンセル中 |
| CANCELED | 設計処理キャンセル完了 |

データ例:
```json
{
    "status": "COMPLETED"
}
```

</details>

## 要求ID (```requestID```)

要求IDは、構成案設計機能の呼び出し元で管理する構成案設計要求を識別するためのIDです。  
[入力された要求ID](a01_Args_to_request_design_Function.md#要求id-requestid)をそのまま返却します。

<details>
<summary>要求IDの詳細情報を表示</summary>

- requestID (String) : 構成案設計機能の呼び出し元で管理する構成案設計要求を識別するためのID

データ例:
```json
{
    "requestID": "463e79c1-d138-4748-9018-5c1435a50d87"
}
```

</details>

## 設計開始時刻 (```startedAt```)

設計開始時刻は、プラグイン/設計機構で構成案の設計処理を開始した時刻を示す文字列です。

<details>
<summary>設計開始時刻の詳細情報を表示</summary>

- startedAt (String) : プラグイン/設計機構での設計処理開始時刻 (ISO 8601 UTC)

データ例:
```json
{
    "startedAt": "2026-01-01T00:00:00.000000Z"
}
```

</details>

## 設計終了時刻 (```endedAt```)

設計終了時刻は、プラグイン/設計機構で構成案の設計処理を終了した時刻を示す文字列です。

<details>
<summary>設計終了時刻の詳細情報を表示</summary>

- endedAt (String) : プラグイン/設計機構での設計処理終了時刻 (ISO 8601 UTC)

データ例:
```json
{
    "endedAt": "2026-01-01T00:00:00.000000Z"
}
```

</details>

## 構成案 (```design```)

構成案は、入力情報をもとに作成されたノードの構成案です。

<details>
<summary>構成案の詳細情報を表示</summary>

以下は、構成案の構造と各項目の意味を階層構造で示したものです。

- design (Object) : 設計した結果となる構成案が格納されたオブジェクト
    - nodes (ObjectList) : サービスを稼働させるノード構成案のリスト
        - services (ObjectList) : 対象のノードで稼働させるサービスの一覧
            - id (String) : サービスを識別するID
            - requestInstanceID (String) : 設計時にサービスインスタンスを識別するID
        - device (Object) : ノードを構成する各デバイス情報
            - cpu (Object) : ノードに割り当てるCPUのデバイス情報
                - deviceIDs (StringList) : CPUのデバイスID
            - memory (Object) : ノードに割り当てるメモリのデバイス情報
                - deviceIDs (StringList) : メモリのデバイスID
            - storage (Object) : ノードに割り当てるストレージのデバイス情報
                - deviceIDs (StringList) : ストレージのデバイスID
            - gpu (ObjectList) : ノードに割り当てるGPUのデバイス情報
                - deviceID (String) : GPUのデバイスID
                - requests (Object) : 割り当てデバイスに対するインスタンス情報
                    - requestInstanceID (String) : 設計時にサービスインスタンスを識別するためのID
                    - index (Number) : 割り当て番号
            - networkInterface (Object) : ノードに割り当てるネットワークインターフェースのデバイス情報
                - deviceIDs (StringList) : ネットワークインターフェースのデバイス情報
        - spec (Number) : 対象のノードに割り当てられたメモリの総容量 (MB)
        - averageEnergyWatts (Number) : 対象のノードの想定消費電力量 (W)
        - constructTime (Number) : ノードの構築にかかる時間 (s)
        - destructTime (Number) : ノードの解体にかかる時間 (s)

データ例:
```json
{
    "design": {
        "nodes": [
            {
                "services": [
                    {
                        "id": "a58ee3a7-62a0-46f3-ba80-f7080eaa0d1c",
                        "requestInstanceID": "1d40d2a9-979f-4956-aee7-30587de64fe9"
                    }
                ],
                "device": {
                    "cpu": {
                        "deviceIDs": ["c188e8bf-bef0-4465-97ff-6e9a14fedd02"]
                    },
                    "memory": {
                        "deviceIDs": ["3cd29852-38ff-4495-a048-7d8e2f57a294"]
                    },
                    "storage": {
                        "deviceIDs": ["f470464e-407d-4860-a1d9-c9cf621fb4a0"]
                    },
                    "gpu": [
                        {
                            "deviceID": "63ccc12d-d10c-4d2a-949f-7a732bbe4710",
                            "requests": {
                                "requestInstanceID": "1d40d2a9-979f-4956-aee7-30587de64fe9",
                                "index": 0
                            }
                        }
                    ],
                    "networkInterface": {
                        "deviceIDs": ["1e7746fc-d96d-4d55-a47f-9c35f21d33b2"]
                    }
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

## 移行条件 (```conditions```)

移行条件は、入力された現ノード構成から作成された構成案へ移行する際に許容されるノード負荷の条件です。

<details>
<summary>移行条件の詳細情報を表示</summary>

以下は、移行条件の構造と各項目の意味を階層構造で示したものです。

- conditions (Object) : 移行条件
    - toleranceCriteria (Object) : 許容負荷条件
        - cpu (ObjectList) : CPUのノードごとの許容負荷条件
            - deviceIDs (StringList) : ノードに接続されているCPUのデバイスID
            - limit (Object) : 使用上限に関する情報
                - weights (NumberList) : CPUのコア数を考慮したCPU使用率を算出するための重み
                - averageUseRate (Number) : 対象CPUの平均使用率上限
        - memory (ObjectList) : メモリのノード毎の許容負荷条件
            - deviceIDs (StringList) : ノードに接続されているメモリのデバイスID
            - limit (Object) : 使用上限に関する情報
                - averageUseBytes (Number) : 対象メモリの平均使用用上限 (MB)
    - energyCriteria (Number) : システム全体の平均消費電力の上限値 (W)

データ例:
```json
{
    "conditions": {
        "toleranceCriteria": {
            "cpu": [
                {
                    "deviceIDs": ["c188e8bf-bef0-4465-97ff-6e9a14fedd02"],
                    "limit": {
                        "weights": [1.0],
                        "averageUseRate": 80
                    }
                }
            ],
            "memory": [
                {
                    "deviceIDs": ["3cd29852-38ff-4495-a048-7d8e2f57a294"],
                    "limit": {
                        "averageUseBytes": 12000
                    }
                }
            ]
        },
        "energyCriteria": 600
    }
}
```

</details>

## 移行手順 (```procedures```)

移行手順は、入力された現ノード構成から作成された構成案へ移行するための手順です。

<details>
<summary>移行手順の詳細情報を表示</summary>

以下は、移行条件の構造と各項目の意味を階層構造で示したものです。

- procedures (ObjectList) : 移行手順
    - operationID (Number) : 移行操作のID
    - operation (String) : 移行操作の種別
    - targetCPUID (String) : 操作対象のCPUのデバイスID
    - targetDeviceID (String) : 操作対象のデバイスのデバイスID
    - targetRequestInstanceID (String) : 操作対象となる設計時にサービスインスタンスを識別するID
    - dependencies (NumberList) : 依存関係のある移行操作のoperationIDのリスト

operationとして以下の6つの操作があります。

| operation | 概要 |
| --- | --- |
| boot | デバイスの起動 |
| shutdown | デバイスの停止 |
| connect | CPUと他デバイスの接続 |
| disconnect | CPUと他デバイスの切断 |
| start | サービスインスタンスの稼働開始 |
| stop | サービスインスタンスの稼働停止 |

データ例:
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

## 設計失敗理由 (```cause```)

設計失敗理由は、構成案の設計に失敗した(設計状態がFAILED)場合の失敗理由を示す文字列です。

<details>
<summary>設計失敗理由の詳細情報を表示</summary>

- cause (String) : 構成案の設計に失敗した理由

データ例:
```json
{
    "cause": "Design request needs more available CPUs."
}
```

上記の設計失敗理由のデータ例は、構成案の設計において利用可能なCPUが不足していることを示します。

</details>