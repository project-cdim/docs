## 2. 構成の変更 <!-- omit in toc -->
ここでは、Composable Disaggregated Infrastructure Manager(略称:CDIM)を用いた構成変更について説明します。  

CDIMでは実際に構築したいノード構成を入力することで、手軽に現在のノード構成を理想のノード構成に変更できます。  
構成変更を行う機能としては、以下の2つが存在します。  
- 構成変更機能
  - 一括で十数ノードの構成変更が可能な機能です。
- APIを用いた構成変更
  - デバイスのON・OFFなど、細かい構成変更を行うための機能です。構成変更機能でエラーが発生した場合などに使用します。

<br>

- [2.1. ノードを新規作成する](#21-ノードを新規作成する)
  - [2.1.1. デバイス情報を確認する](#211-デバイス情報を確認する)
  - [2.1.2. 構成したい内容を記述する](#212-構成したい内容を記述する)
  - [2.1.3. 実行する](#213-実行する)
- [2.2. ノードを変更追加する](#22-ノードを変更追加する)
  - [2.2.1. デバイス情報を確認する](#221-デバイス情報を確認する)
  - [2.2.2. 構成したい内容を記述登録する](#222-構成したい内容を記述登録する)
  - [2.2.3. 実行する](#223-実行する)
- [2.3. ノードを削除する](#23-ノードを削除する)
  - [2.3.1. デバイス情報を確認する](#231-デバイス情報を確認する)
  - [2.3.2. 構成したい内容を記述登録する](#232-構成したい内容を記述登録する)
  - [2.3.3. 実行する](#233-実行する)
- [2.4. APIを用いた構成変更](#24-apiを用いた構成変更)
  - [2.4.1. デバイスの電源状態を変える](#241-デバイスの電源状態を変える)
  - [2.4.2. デバイスの接続状態を変える](#242-デバイスの接続状態を変える)
- [2.5. 構成変更機能の記述内容(サンプルファイル)](#25-構成変更機能の記述内容サンプルファイル)
  
### 2.1. ノードを新規作成する

#### 2.1.1. デバイス情報を確認する

各デバイスの詳細画面を確認し、使用したいスペックを選定します。

![](imgs/check_device_state_temp1.png)

ノード構成が定まったら、構成変更後に使用予定のデバイスIDを確認します。

> [!WARNING]
> デバイスの中には、あらかじめcpuと接続されている内蔵デバイスが存在し、内蔵デバイスはあらかじめ接続されているcpu以外のcpuと接続することはできません。
> 内蔵デバイスかどうかを確認する方法は以下になります。
> - 詳細情報にnonRemovableDevicesの記載がある : 内蔵デバイスであり、記載があるデバイスIDのcpuと接続されている
> - 詳細情報にnonRemovableDevicesの記載がない : 内蔵デバイス以外
> ※cpuには内蔵デバイスが存在しません。cpuに記載されているnonRemovableDevicesは内蔵デバイスを示しています。
> ![](imgs/nonRemovableDevice.png)

#### 2.1.2. 構成したい内容を記述する

新しく構成したいノード構成を記述します。  
> [!NOTE]
> デバイスIDについては、CDIMを立ち上げた時に生成された値に変更してください。 
```sh
$ mkdir test
$ vi test/template_1.json
```
<details>
<summary>test/template_1.json (example)</summary>

```json

{
    "targetNodeIDs": [
            "408f0ee4-4570-4461-b6c4-4c1f4bf4756e",
            "5a5cc33d-11e5-4b80-89ef-4af5cf342c6e"
    ],
    "desiredLayout": {
        "nodes": [
            {
                "device": {
                    "cpu": {
                        "deviceIDs": [
                            "408f0ee4-4570-4461-b6c4-4c1f4bf4756e"
                        ]
                    },
                    "memory": {
                        "deviceIDs": [
                            "1bb7cd4a-e635-49a5-9ca1-e97b7699c32c",
                            "108ad96d-af9a-4af5-ab4f-9aee1d52698e"
                        ]
                    },
                    "storage": {
                        "deviceIDs": [
                            "12836b47-e2ec-4209-8c91-875fade897e7"
                        ]
                    },
                    "networkInterface": {
                        "deviceIDs": [
                            "cd3d1f47-fde5-4cb0-bc6e-bb79921280f8"
                        ]
                    },
                    "gpu": {
                        "deviceIDs": [
                            "060da9eb-4fba-4c06-9d0f-bf1c56992037"
                        ]
                    }
                }
            },
            {
                "device": {
                    "cpu": {
                        "deviceIDs": [
                            "5a5cc33d-11e5-4b80-89ef-4af5cf342c6e"
                        ]
                    },
                    "memory": {
                        "deviceIDs": [
                            "8c1e4a13-2d27-4431-9b82-d2f65f49313e",
                            "3a2cd9bc-d4fb-4eaf-881b-a8ac98a91b1b"
                        ]
                    },
                    "storage": {
                        "deviceIDs": [
                            "1ea189b4-ad07-4519-ac2b-e1301151bf1c"
                        ]
                    },
                    "networkInterface": {
                        "deviceIDs": [
                            "be347398-9179-4173-8bda-15d55083606c"
                        ]
                    },
                    "gpu": {
                        "deviceIDs": [
                            "189a08b2-a609-489b-8958-9876925c426b"
                        ]
                    }
                }
            }
        ]
    }
}

```

</details>

#### 2.1.3. 実行する

1. 上で登録した構成の移行手順を作成し、確認する
   ```sh
   $ curl -XPOST -H 'Content-Type: application/json' http://<ipアドレス>:8013/cdim/api/v1/migration-procedures -d @test/template_1.json | jq > test/procedure_template_1.json
   $ cat test/procedure_template_1.json 
   ```

2. 出力された移行手順を編集する  
   出力された移行手順が以下の形式になっていない場合は、以下の形式に修正します。
   ```sh
   $ vi test/procedure_template_1.json
   {
    "procedures": [
        <出力内容>
    ]
   }
   ```

3. 作成した移行手順を反映する
    ```sh
    $ curl -XPOST -H 'Content-Type: application/json' http://<ipアドレス>:8013/cdim/api/v1/layout-apply -d @test/procedure_template_1.json
    ```

4. メトリクス情報の更新する  
   メトリクス情報の更新には、数分の時間がかかります。
   ```sh
    $ docker exec -it performance-collector /bin/sh
    $ curl -i -s -X PUT http://localhost:8080/cdim/api/v1/configs
    ```

5. 構成変更されたことをUIで確認する
   > 実行後、ノード一覧やリソース一覧に反映されるまで数分かかります。

   ![](imgs/result_templete_1.png)
   FailedやSuspendの場合はもう一度[2.](#212-構成したい内容を記述する)から実行するか、 [トラブルシューティング](../appendix/troubleshooting/README.md)を参照してください。

### 2.2. ノードを変更追加する

#### 2.2.1. デバイス情報を確認する

各デバイスの詳細画面を確認し、変更・追加したいスペックを選定します。
![](imgs/check_device_state_temp2.png)  
ノード構成が定まったら、構成変更する前のノードに使用されているデバイスIDと構成変更後のデバイスIDを確認します。

> [!WARNING]
> デバイスの中には、あらかじめcpuと接続されている内蔵デバイスが存在し、内蔵デバイスはあらかじめ接続されているcpu以外のcpuと接続することはできません。
> 内蔵デバイスかどうかを確認する方法は以下になります。
> - 詳細情報にnonRemovableDevicesの記載がある : 内蔵デバイスであり、記載があるデバイスIDのcpuと接続されている
> - 詳細情報にnonRemovableDevicesの記載がない : 内蔵デバイス以外
> ※cpuには内蔵デバイスが存在しません。cpuに記載されているnonRemovableDevicesは内蔵デバイスを示しています。
> ![](imgs/nonRemovableDevice.png)

#### 2.2.2. 構成したい内容を記述(登録)する

新しく構成したいノード構成を記述します。  
> [!NOTE]
> デバイスIDについては、先程登録した時に生成された値に変更してください。 
```sh
$ mkdir test
$ vi test/template_2.json
```
<details>
<summary>test/template_2.json (example)</summary>

```json
{
    "targetNodeIDs": [
            "5a5cc33d-11e5-4b80-89ef-4af5cf342c6e",
            "6e40fc9e-b99a-455e-bce3-21e360ed9f71",
            "77683d0a-d257-4b4d-a7ec-57eba1466681"
    ],
    "desiredLayout": {
        "nodes": [
            {
                "device": {
                    "cpu": {
                        "deviceIDs": [
                            "5a5cc33d-11e5-4b80-89ef-4af5cf342c6e"
                        ]
                    },
                    "memory": {
                        "deviceIDs": [
                            "8c1e4a13-2d27-4431-9b82-d2f65f49313e",
                            "3a2cd9bc-d4fb-4eaf-881b-a8ac98a91b1b",
                            "5dd8f904-d466-4062-87b7-6f7f5a72afad"
                        ]
                    },
                    "storage": {
                        "deviceIDs": [
                            "1ea189b4-ad07-4519-ac2b-e1301151bf1c",
                            "24968a3b-0f23-4093-9a8f-bd1bb40b1189"
                        ]
                    },
                    "networkInterface": {
                        "deviceIDs": [
                            "be347398-9179-4173-8bda-15d55083606c",
                            "0d1601dd-f1d0-490b-b591-8c4e80c4806f"
                        ]
                    },
                    "gpu": {
                        "deviceIDs": [
                            "189a08b2-a609-489b-8958-9876925c426b",
                            "26a01737-5ae2-4d6e-aa1e-82f26cf16595",
                            "3e679d00-c313-4f26-aa89-8415b7b6a085"
                        ]
                    }
                }
            },
            {
                "device": {
                    "cpu": {
                        "deviceIDs": [
                            "6e40fc9e-b99a-455e-bce3-21e360ed9f71"
                        ]
                    },
                    "memory": {
                        "deviceIDs": [
                            "01c0be1e-b73b-42f0-9167-35f8f3c4d343",
                            "810cbd3a-0808-4623-8f2d-e60a618d4b23"
                        ]
                    },
                    "storage": {
                        "deviceIDs": [
                            "5b3d6c29-2733-4542-814c-6381277f2ba7",
                            "3e8eecc7-6c68-4d8d-8d21-12bcde4d2c50"
                        ]
                    },
                    "networkInterface": {
                        "deviceIDs": [
                            "cb14c649-de57-482f-9198-23dbb58f51dc"
                        ]
                    },
                    "gpu": {
                        "deviceIDs": [
                            "4ba8f685-8a11-4086-bc6f-50c0d21e17fa"
                        ]
                    }
                }
            },
            {
                "device": {
                    "cpu": {
                        "deviceIDs": [
                            "77683d0a-d257-4b4d-a7ec-57eba1466681"
                        ]
                    },
                    "memory": {
                        "deviceIDs": [
                            "cf8b4abc-12e2-4af4-98c7-3077ebfaf1b7",
                            "a87e2f63-7ff3-4656-b1f0-638c2487589b"
                        ]
                    },
                    "storage": {
                        "deviceIDs": [
                            "7cd6b0c2-194b-4451-a5b4-6ac6e0478525"
                        ]
                    },
                    "networkInterface": {
                        "deviceIDs": [
                            "fd5f1c21-7116-445e-bb8e-4af8d80bd25b"
                        ]
                    }
                }
            }
        ]
    }
}
```

</details>

#### 2.2.3. 実行する

1. 上で登録した構成の移行手順を作成し、確認する
   ```sh
   $ curl -XPOST -H 'Content-Type: application/json' http://<ipアドレス>:8013/cdim/api/v1/migration-procedures -d @test/template_2.json | jq > test/procedure_template_2.json
   $ cat test/procedure_template_2.json 
   ```
2. 出力された移行手順を編集する  
   出力された移行手順が以下の形式になっていない場合は、以下の形式に修正します。
   ```sh
   $ vi test/procedure_template_2.json
   {
    "procedures": [
        <出力内容>
    ]
   }
   ```
3. 作成した移行手順を反映する
   ```sh
   $ curl -XPOST -H 'Content-Type: application/json' http://<ipアドレス>:8013/cdim/api/v1/layout-apply -d @test/procedure_template_2.json
   ```
4. メトリクス情報の更新する  
   メトリクス情報の更新には、数分の時間がかかります。
   ```sh
    $ docker exec -it performance-collector /bin/sh
    $ curl -i -s -X PUT http://localhost:8080/cdim/api/v1/configs
    ```
5. 構成変更されたことをUIで確認する
   > 実行後、ノード一覧やリソース一覧に反映されるまで数分かかります。

   ![](imgs/result_templete_2.png)
   FailedやSuspendの場合はもう一度[2.](#222-構成したい内容を記述登録する)から実行するか、 [トラブルシューティング](../appendix/troubleshooting/README.md)を参照してください。

### 2.3. ノードを削除する

#### 2.3.1. デバイス情報を確認する 

各デバイスの詳細画面を確認し、削除したいノードを選定します。
![](imgs/check_device_state_temp3.png)
ノード構成が定まったら、構成変更する前のノードに使用されているデバイスIDと構成変更後のデバイスIDを確認します。

> [!WARNING]
> デバイスの中には、あらかじめcpuと接続されている内蔵デバイスが存在し、内蔵デバイスはあらかじめ接続されているcpu以外のcpuと接続することはできません。
> 内蔵デバイスかどうかを確認する方法は以下になります。
> - 詳細情報にnonRemovableDevicesの記載がある : 内蔵デバイスであり、記載があるデバイスIDのcpuと接続されている
> - 詳細情報にnonRemovableDevicesの記載がない : 内蔵デバイス以外
> ※cpuには内蔵デバイスが存在しません。cpuに記載されているnonRemovableDevicesは内蔵デバイスを示しています。
> ![](imgs/nonRemovableDevice.png)

#### 2.3.2. 構成したい内容を記述(登録)する

新しく構成したいノード構成を記述します。
> [!NOTE]
> デバイスIDについては、先程登録した時に生成された値に変更してください。 
```sh
$ mkdir test
$ vi test/template_3.json
```
<details>
<summary>test/template_3.json (example)</summary>

```json
{
    "targetNodeIDs": [
            "5a5cc33d-11e5-4b80-89ef-4af5cf342c6e"
    ],
    "desiredLayout": {
        "nodes": [
        ]
    }
}
```

</details>

#### 2.3.3. 実行する

1. 上で登録した構成の移行手順を作成し、確認する
   ```sh
   $ curl -XPOST -H 'Content-Type: application/json' http://<ipアドレス>:8013/cdim/api/v1/migration-procedures -d @test/template_3.json | jq > test/procedure_template_3.json
   $ cat test/procedure_template_3.json 
   ```
2. 出力された移行手順を編集する  
   出力された移行手順が以下の形式になっていない場合は、以下の形式に修正します。
   ```sh
   $ vi test/procedure_template_3.json
   {
    "procedures": [
        <出力内容>
    ]
   }
   ```
3. 作成した移行手順を反映する
   ```sh
   $ curl -XPOST -H 'Content-Type: application/json' http://<ipアドレス>:8013/cdim/api/v1/layout-apply -d @test/procedure_template_3.json
   ```
4. メトリクス情報の更新する  
   メトリクス情報の更新には、数分の時間がかかります。
   ```sh
    $ docker exec -it performance-collector /bin/sh
    $ curl -i -s -X PUT http://localhost:8080/cdim/api/v1/configs
    ```
5. 構成変更されたことをUIで確認する
   > 実行後、ノード一覧やリソース一覧に反映されるまで数分かかります。

   ![](imgs/result_templete_3.png)
   FailedやSuspendの場合はもう一度[2.](#232-構成したい内容を記述登録する)から実行するか、 [トラブルシューティング](../appendix/troubleshooting/README.md)を参照してください。

### 2.4. APIを用いた構成変更

ここでは構成情報機能での変更がむずかしい、細かな構成変更方法を説明します。

#### 2.4.1. デバイスの電源状態を変える

1. 電源状態を変更したいデバイスの情報を確認する
    　![](imgs/check_device_state.png)
    ```sh
    $ docker container exec -t hw-control curl http://localhost:3500/v1.0/invoke/hw-control/method/cdim/api/v1/devices/<電源状態を変更したいデバイスID> | jq
    {
    "deviceID": "1ea189b4-ad07-4519-ac2b-e1301151bf1c",
    "type": "storage",
            :
    "powerState": "Off"
            :
    }
    ```
1. 電源状態を変更する
    下の電源状態一覧から変更したい電源状態を選択し、以下のコマンドを入力します。

    <details>
    <summary> 変更可能な電源状態一覧 </summary>

    - on
    - off
    - reset
    - force-off

    </details>

    ```sh
    $ docker container exec -t hw-control curl -X PUT http://localhost:3500/v1.0/invoke/hw-control/method/cdim/api/v1/devices/<電源状態を変更したいデバイスID>/power -d '{"action": "on"}' -H 'accept: application/json' -H 'Content-Type: application/json'
    {"deviceID":"1ea189b4-ad07-4519-ac2b-e1301151bf1c"}
    変更したデバイス情報を確認します
    $ docker container exec -t hw-control curl http://localhost:3500/v1.0/invoke/hw-control/method/cdim/api/v1/devices/<電源状態を変更したいデバイスID> | jq
    {
    "deviceID": "1ea189b4-ad07-4519-ac2b-e1301151bf1c",
    "type": "storage",
            :
    "powerState": "On"
            :
    }
    ```

#### 2.4.2. デバイスの接続状態を変える

1. 接続状態を変更したいデバイス情報を確認する
    ![](imgs/check_cpu_of_node.png)
    ```sh
    CPU情報を確認します
    $ docker container exec -t hw-control curl http://localhost:3500/v1.0/invoke/hw-control/method/cdim/api/v1/devices/<cpuのデバイスID> | jq
    {
    "deviceID": "9ea47b1b-bf73-4267-95e2-31c702a274c9",
    "type": "CPU",
            :
    "powerState": "On"
            :
    }
    接続状態を変更するデバイス情報を確認します
    $ docker container exec -t hw-control curl http://localhost:3500/v1.0/invoke/hw-control/method/cdim/api/v1/devices/<接続情報を変更するデバイスID> | jq
    {
    "deviceID": "1ea189b4-ad07-4519-ac2b-e1301151bf1c",
    "type": "storage",
            :
    "powerState": "On"
            :
    }
    ```
1. 接続状態を変更する

    　下の接続状態一覧から接続状態を選択し、以下のコマンドを実行します。

    変更可能な接続状態一覧
    - connect
    - disconnect
    ```sh
    $ docker container exec -t hw-control curl -X PUT http://localhost:3500/v1.0/invoke/hw-control/method/cdim/api/v1/cpu/<cpuのデバイスID>/aggregations -d '{"deviceID": "<接続状態を変更するデバイスID>", "action": "connect"}' -H 'accept: application/json' -H 'Content-Type: application/json'
    {"CPUDeviceID":"9ea47b1b-bf73-4267-95e2-31c702a274c9","deviceID":"1ea189b4-ad07-4519-ac2b-e1301151bf1c"}
    ```
    デバイスの接続状態を確認します。
    ![](imgs/check_cpu_after_connect.png)
    > 実行後、ノード一覧やリソース一覧に反映されるまで数分かかります。

1. メトリクス情報の更新する
    メトリクス情報の更新には、数分の時間がかかります。
    ```sh
    $ docker exec -it performance-collector /bin/sh
    $ curl -i -s -X PUT http://localhost:8080/cdim/api/v1/configs
    ```

### 2.5. 構成変更機能の記述内容(サンプルファイル)

ここではサンプルファイルを用いて、CDIMでの構成内容の記述方法・項目を示します。

<details>
<summary>構成内容の記述詳細(template_0.json)</summary>

```json
{
    <!-- 変更したいノードID(CPUのデバイスID)を記載する -->
    "targetNodeIDs": [
        <!-- 複数ある場合は複数記載する -->
        "f72874dd-509b-445f-ad7a-47e21114736d",
        "c71ca465-189a-4315-ab91-ff8cf58bbfd2"
    ],
    <!-- 変更後のノード構成を記載する -->
    "desiredLayout": {
        "nodes": [
            <!-- ノード1つ目 -->
            {
                <!-- ノードのデバイス情報を記載する -->
                "device": {
                    "cpu": {
                        "deviceIDs": [
                            "f72874dd-509b-445f-ad7a-47e21114736d"
                        ]
                    },
                    "memory": {
                        "deviceIDs": [
                            "01c510d4-9f9c-4d7e-9107-ab976a7a46fb",
                        ]
                    },
                    "storage": {
                        "deviceIDs": [
                            "b001a83a-10ff-4e53-bb71-fdc4e1fc6c05"
                        ]
                    },
                    "networkInterface": {
                        "deviceIDs": [
                            "fefafbaa-98cf-4d65-a1ef-c24df942c420"
                        ]
                    }
                }
            },
            <!-- ノード2つ目 -->
            {
                "device": {
                    "cpu": {
                        "deviceIDs": [
                            "c71ca465-189a-4315-ab91-ff8cf58bbfd2"
                        ]
                    },
                    "memory": {
                        "deviceIDs": [
                            <!-- デバイスを複数使用する場合は複数記載する -->
                            "10991104-a11c-4c44-b20d-78b7ebcab0f8",
                            "99adb16d-e75b-43f9-8215-76fbc26bff33"
                        ]
                    },
                    "storage": {
                        "deviceIDs": [
                            "0d94b110-bde5-48ad-8159-23dbcc2918bd",
                            "db9e86c4-aeb6-4bc1-a061-d31542fbe2b9"
                        ]
                    },
                    "networkInterface": {
                        "deviceIDs": [
                            "499cf595-b79f-40b4-bfd2-af9a05c04c2c"
                        ]
                    }
                }
            }
        ]
    }
}
```

</details>

<br>

<details>
<summary>記述項目詳細</summary>

|name|explantation|
|:--|:--|
|targetNodeIDs|変更したいノード一覧を記載するオブジェクトです。この項目が空の場合、すべてのノードに対して実行されるため注意が必要です。|
|desireLayout|構成変更した後の情報を記載するオブジェクトです。|
|nodes|ノード情報をリスト形式で記述するオブジェクトです。|
|devices|ノードに使用されているまたは使用予定のデバイス一覧を記述するオブジェクトです。|

</details>

<br>

<details>
<summary>使用可能リソース一覧</summary>

- CPU
- memory
- storage
- networkInterface(NIC)
- GPU
> 使用可能リソースは順次追加予定

</details>

[Next 3.各種設定](../configuration/README.md)
