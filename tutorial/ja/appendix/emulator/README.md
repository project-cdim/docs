# エミュレーターの操作方法 
ここでは、Composable Disaggregated Infrastructure Manager(略称:CDIM)で用いるエミュレータについて説明します。
より詳細な設定方法が知りたい方は、[hw-emulator-reference](https://github.com/project-cdim/hw-emulator-reference)を参照してください。

- [1. エミュレータの設定方法](#1-エミュレータの設定方法)
- [2. エミュレータの操作方法](#2-エミュレータの操作方法)
   - [2.1. 情報収集方法](#21-情報収集方法)
   - [2.2. metric状態変更方法](#22-metric状態変更方法)

## 1. エミュレータの設定方法
ここではエミュレータの設定ファイルとその基本的な設定項目を示します。  
デフォルトで用意しているデバイス情報を変更したい場合は、「2. Redfishエミュレータ デバイス定義ファイル設定」、「3. Redfishエミュレータ 出力データ設定」もあわせて確認してください。  

   <details>
   <summary> 1. Redfishエミュレータの基本設定 </summary>  
   
   設定ファイル名  
   - デバイス定義ファイルを使用する場合 : emulator-config_device_populate.json  

   - デバイス定義ファイルを使用しない場合 : emulator-config_dynamic_populate.json  
   
   設定項目一覧

   |項目|説明|設定値|
   |:--|:--|:--|
   | MODE | 使用するポートを指定します。値が「Local」の場合、ポートにはデフォルトでコマンドラインまたは 5000 のポートパラメータの値が割り当てられます | Local |
   | HTTPS | HTTPSを使用するかを指定する項目です。 | Disable |
   | TRAYS | 初期リソースプールを構成するリソースへのパス。複数のトレイを指定することができます。TRAYSを指定すると、デバイス作成時にTRAYSから取得していきます。 | 未使用 |
   | POPULATE | エミュレータ起動時の要素。設定ファイルを指定します | ../simulatorDeviceList.json |
   | DEVICE_SPEC | 設定ファイルを使用してデバイスを作成するかどうか。設定ファイルを使用する場合は必ず指定します | true |
   | SPEC | コンピューターシステムがRedfish ComputerSystemとして表現されているか、あるいは他のスキーマとして表現されているか。システムパスを設定する際に使用します | Redfish |
   | MOCKUPFOLDERS | モックアップフォルダーの格納先。フォルダーには変更や操作を行わない静的なデータ(モックアップ)を返却する際のJSONファイルを格納します | Redfish |
   | POWER_LINK | CPUの電源状態と、同じComputerSystemに存在するGPU、メモリ、ストレージ、NICの電源状態を連動します | true |
   </details>

   <details>
   <summary> 2. Redfishエミュレータ デバイス定義ファイル設定 </summary>  
   
   設定ファイル名  

   デバイス定義ファイル : simulatorDeviceList.json 

   
   設定項目一覧

   以下に基本的な入力事項のみを記載します。各デバイスに特有の項目は基本記載していません。

   |項目|説明|
   |:--|:--|
   | deviceID | デバイスを個別に認識するためのID。deviceID は一意の文字列を指定する必要があります。 |
   | model | デバイスのモデル名を記入する項目です。 |
   | manufacturer | デバイスの製造元を記載する項目です。 |
   | link | CPUにあらかじめ接続されている内蔵デバイスを記載する項目。CPUのみに存在する項目で、1つ以上の内蔵メモリの記載が必要です。 |
   </details>

   <details>
   <summary> 3. Redfishエミュレータ 出力データ設定 </summary>  
   
   設定ファイル名  

   出力データ設定ファイル : infragen/test_device_parameter.json
 
   
   設定項目一覧

   以下に基本的な入力事項のみを記載します。各デバイスに特有の項目は記載していません。

   |項目|説明|
   |:--|:--|
   | state | そのデバイスの状態を指定します。デフォルトではEnableが入力されています。 |
   | health | そのデバイスに異常がないかを指定します。デフォルトではOKが入力されており、他に「Warning」、「Critical」を入力することが可能です。 |
   | sensingInterval | センサーの読み取り間の時間間隔(s)を指定します。 |

   </details>

## 2. エミュレータの操作方法
ここでは、エミュレータの基本的な使用方法を示します。  

### 2.1. 情報収集方法    
   ここでは、エミュレータ上での情報収集方法を説明します。

   マネージャー情報一覧を取得し、マネージャ情報を取得します。
   ```sh
   $ docker container exec -it hw-emulator /bin/sh
   $ curl http://localhost:5000/redfish/v1/Managers
   $ curl http://localhost:5000/redfish/v1/Managers/BMC-1
   ```
   取得したいデバイスに合わせて、ComputerSystemもしくはChassisの情報を取得します。
   ```sh
   $ curl http://localhost:5000/redfish/v1/Systems/System-1
   $ curl http://localhost:5000/redfish/v1/Chassis/Chassis-1
   ```
   対象デバイスタイプのデバイス一覧を取得します。
   ```sh
   $ curl http://localhost:5000/redfish/v1/Systems/System-1/Processors
   ```
   対象のデバイス情報を取得します。
   ```sh
   $ curl http://localhost:5000/redfish/v1/Systems/System-1/Processors/PROC-0001
   ```

### 2.2. metric状態変更方法
   ここでは、エミュレータのmetric状態の変更方法をCPUを例にして説明します。

   CPUの詳細情報を取得します。
   ```sh
   $ docker container exec -it hw-emulator /bin/sh
   $ curl http://localhost:5000/redfish/v1/Systems/System-1/Processors/PROC-0001 | jq
   ```
   取得した情報から以下を確認します。
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
   確認した情報を用いてmetric状態の変更を行います。
   ```sh
   $ curl -XPOST http://localhost:5000/redfish/v1/Systems/System-1/Processors/PROC-0001/Actions/Processor.MetricState -H "Content-Type: application/json" -d '{"StateType": "off"}'
   ```

   変更内容を確認します。
   ```sh
   $ http://localhost:5000/redfish/v1/Systems/System-1/Processors/PROC-0001/ProcessorMetrics | jq
   {
            :
      "BandwidthPercent": 0,  #offにしたことで0に変更された。
            :
   }
   ```
