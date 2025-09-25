# 6. FMプラグインの実装

FMプラグインは`app.common.utils.fm_plugin_base`モジュールに定義された
`FMPluginBase`クラスを継承したクラスとして実装します。  
クラス名は任意であり、プラグイン設定ファイルに`class`プロパティとして定義します。  

```python
from app.common.utils.fm_plugin_base import FMPluginBase

class FMSamplePlugin(FMPluginBase):
```

FMプラグインクラスのコンストラクタは、実装も省略も可能です。  
コンストラクタの実装を省略する場合、プラグイン設定ファイルの`specific_data`プロパティとして定義した情報が
`specific_data`属性として参照できます。  
コンストラクタを実装する場合、設定ファイルの`specific_data`で指定した情報が`specific_data`引数として引き渡されます。
また、コンストラクタはメソッドの実装状況を確認する目的で、`specific_data`がNoneで呼び出されることがあります。
そのため、`specific_data`がNoneの場合は正常終了するように実装する必要があります。  

```python
__init__(specific_data: dict = None) -> None:
```

プラグイン設定ファイルの詳細は、[4.1 ファイル構成](04_Configuration.md#41-ファイル構成)を参照ください。  

FMプラグインは以下のメソッドを定義する必要があります。

- [6.1. `connect(cpu_id, device_id)`](#61-connectcpu_id-device_id)
- [6.2. `disconnect(cpu_id, device_id)`](#62-disconnectcpu_id-device_id)
- [6.3. `get_port_info(target_id=None)`](#63-get_port_infotarget_idnone)
- [6.4. `get_switch_info(switch_id=None)`](#64-get_switch_infoswitch_idnone)

## 6.1. `connect(cpu_id, device_id)`

```python
connect(cpu_id: str, device_id: str) -> None:
```

スイッチ、または、ファブリックのUSP(Upstream Switch Port)とDSP(Downstream Switch Port)をbindする機能を持つメソッド

### 6.1.1. 引数

- `cpu_id`  
USP側のFMポートIDを指定します。  
- `device_id`  
DSP側のFMポートIDを指定します。  

FMポートIDは、FMプラグインがポート情報として返却する識別子です。  
ポート情報については[6.3. `get_port_info`](#63-get_port_infotarget_idnone)を参照ください。  
USP側のFMポートにはCPU装置が、DSP側のFMポートにはデバイスがそれぞれ結線されている想定です。  

### 6.1.2. 返り値

正常終了時は何も返却しません。  
指定されたcpu_idとdevice_idが示すデバイスが既にbindされている場合は正常終了してください。  
異常時は、`BaseHWControlError`を継承した例外を発生させます。  
`connect`メソッドが既定で使用できる例外は以下の表に記載のとおりです。  

|状況|例外クラス|
|----|----|
|コンストラクタで指定された情報に不備がある|`ConfigurationHWControlError`|
|FMで認証に失敗した|`AuthenticationHWControlError`|
|引数の`cpu_id`が存在しない|`UpstreamDeviceNotFoundHWControlError`|
|引数の`device_id`が存在しない|`DownstreamDeviceNotFoundHWControlError`|
|`device_id`で指定したDSP側のFMポートが、`cpu_id`で指定したUSP側FMポートとは異なるFMポートと接続済み|`RequestConflictHWControlError`|
|`cpu_id`と`device_id`が同一ファブリック上にない|`BadRequestHWControlError`|
|FMは指定されたcpu_idとdevice_idの接続に失敗した|`FMConnectFailureHWControlError`|
|FMの状態などに何らかの異常が発生した|`ControlObjectHWControlError`|
|FMプラグインの内部エラーが発生した|`InternalHWControlError`|
|原因不明のエラーが発生した(非推奨)|`UnknownHWControlError`|

既定で使用できる例外は、`app.common.basic_exceptions`パッケージに定義されています。  
また、新たにプラグイン固有の例外を設定することが可能です。
詳細は[7. 例外処理](07_Handling_Exceptions.md)を参照ください。  

- 注意事項
  - **引数で指定されたポートにデバイスが存在しない場合には、片方のデバイスが存在しないことが判明した時点で例外を送出してください。`HostCPUAndDeviceNotFoundHWControlError`を使用している場合は修正してください。**  
  - **引数の`cpu_id`が示すデバイスが存在しないケースで`HostCPUNotFoundHWControlError`を使用していた場合は、`UpstreamDeviceNotFoundHWControlError`を使用するように修正してください。**
  - **引数の`device_id`が示すデバイスが存在しないケースで`DeviceNotFoundHWControlError`を使用していた場合は、`DownstreamDeviceNotFoundHWControlError`を使用するように修正してください。**

### 6.1.3. 動作確認手順

以下の手順で[HW制御機能のREST API](02_HWControlFunction.md#21-hw制御機能のrest-api)を実行します。

1. `全デバイススペック情報取得`を実行して、全デバイスのスペック情報を取得します。
2. 返却データから、接続したい上流側デバイスと下流側デバイスのデバイスIDを探します。
3. パスパラメータに上流側デバイスのデバイスIDを指定し、リクエストボディを以下のように指定して`構成変更制御（デバイスとデバイス）`による接続を実行します。

    ```JSON
    {"action": "connect", "destinationDeviceID": "<接続したい下流側デバイスのデバイスID>"}
    ```

本操作により、引数にデバイスIDに対応するFMポートIDが指定された状態で`connect`メソッドが呼び出されます。  
REST APIで返却されるデバイスIDはHW制御機能により生成された一意な文字列になります。  
この値は、FMポートIDは別の値ですが、HW制御機能でFMポートIDに変換されFMプラグインのメソッドの引数に指定されます。

## 6.2. `disconnect(cpu_id, device_id)`

```python
disconnect(cpu_id: str, device_id: str) -> None:
```

スイッチ、または、ファブリックのUSP(Upstream Switch Port)とDSP(Downstream Switch Port)のbind状態を解除する機能を持つメソッド

### 6.2.1. 引数

- `cpu_id`  
USP側のFMポートIDを指定します。  
- `device_id`  
DSP側のFMポートIDを指定します。  

FMポートIDは、FMプラグインがポート情報として返却する識別子です。  
ポート情報については[6.3. `get_port_info`](#63-get_port_infotarget_idnone)を参照ください。  
USP側のFMポートにはCPU装置が、DSP側のFMポートにはデバイスがそれぞれ結線されている想定です。  

### 6.2.2. 返り値

正常終了時は何も返却しません。  
`device_id`で指定したFMポートがどこともbindされていない場合は正常終了してください。  
異常時は、`BaseHWControlError`を継承した例外を発生させます。  
`disconnect`メソッドが既定で使用できる例外は以下の表に記載のとおりです。  

|状況|例外クラス|
|----|----|
|コンストラクタで指定された情報に不備がある|`ConfigurationHWControlError`|
|FMで認証に失敗した|`AuthenticationHWControlError`|
|引数の`cpu_id`が存在しない|`UpstreamDeviceNotFoundHWControlError`|
|引数の`device_id`が存在しない|`DownstreamDeviceNotFoundHWControlError`|
|`device_id`で指定したDSP側のFMポートが、`cpu_id`で指定したUSP側FMポートとは異なるFMポートと接続済み|`RequestConflictHWControlError`|
|FMは指定されたcpu_idとdevice_idの切断に失敗した|`FMDisconnectFailureHWControlError`|
|FMの状態などに何らかの異常が発生した|`ControlObjectHWControlError`|
|FMプラグインの内部エラーが発生した|`InternalHWControlError`|
|原因不明のエラーが発生した(非推奨)|`UnknownHWControlError`|

既定で使用できる例外は、`app.common.basic_exceptions`パッケージに定義されています。  
また、新たにプラグイン固有の例外を設定することが可能です。
詳細は[7. 例外処理](07_Handling_Exceptions.md)を参照ください。  

- 注意事項
  - **引数で指定されたポートにデバイスが存在しない場合には、片方のデバイスが存在しないことが判明した時点で例外を送出してください。`HostCPUAndDeviceNotFoundHWControlError`を使用している場合は修正してください。**  
  - **引数の`cpu_id`が示すデバイスが存在しないケースで`HostCPUNotFoundHWControlError`を使用していた場合は、`UpstreamDeviceNotFoundHWControlError`を使用するように修正してください。**
  - **引数の`device_id`が示すデバイスが存在しないケースで`DeviceNotFoundHWControlError`を使用していた場合は、`DownstreamDeviceNotFoundHWControlError`を使用するように修正してください。**

### 6.2.3. 動作確認手順

以下の手順で[HW制御機能のREST API](02_HWControlFunction.md#21-hw制御機能のrest-api)を実行します。

1. `全デバイススペック情報取得`を実行して、全デバイスのスペック情報を取得します。
2. 返却データから、切断したい上流側デバイスと下流側デバイスのデバイスIDを探します。
3. パスパラメータに上流側デバイスのデバイスIDを指定し、リクエストボディを以下のように指定して`構成変更制御（デバイスとデバイス）`による切断を実行します。

    ```JSON
    {"action": "disconnect", "destinationDeviceID": "<切断したい下流側デバイスのデバイスID>"}
    ```

本操作により、引数にデバイスIDに対応するFMポートIDが指定された状態で`disconnect`メソッドが呼び出されます。  
REST APIで返却されるデバイスIDはHW制御機能により生成された一意な文字列になります。  
この値は、FMポートIDは別の値ですが、HW制御機能でFMポートIDに変換されFMプラグインのメソッドの引数に指定されます。

## 6.3. `get_port_info(target_id=None)`

```python
get_port_info(target_id: str = None) -> dict[str, list[FMPortData]]:
```

FMが管理しているスイッチが持つポートの情報を取得する機能を持つメソッド

### 6.3.1. 引数

- `target_id`  
FMポートIDを指定します。省略が可能です。  
引数を指定した場合、指定したFMポートIDのポート情報を返却します。  
引数を省略した場合、FMが管理するすべてのスイッチのすべてのポート情報を返却します。  

### 6.3.2. 返り値

dataキーを持つ辞書型を返却します。  
dataキーの値は対象のポート情報(ポート情報クラス型)のリスト(リスト型)を返します。  
引数を指定した場合、指定したポートのポート情報を返却します。  
引数を省略した場合、すべてのポートのポート情報を返却します。  

ポート情報の詳細は[6.3.4. ポート情報](#634-ポート情報)を参照ください。  
返却対象のすべてのポートを取得できた場合は、それらのポートに対するポート情報を返却します。  
障害などで、取得出来ていないポート(id)があった場合は異常とします。  
取得時に障害はなくても、設置時の不備などで有効なポート(id)が1つもない場合も、異常とします。  
異常時は、`BaseHWControlError`を継承した例外を発生させます。  
`get_port_info`メソッドが既定で使用できる例外は以下の表に記載のとおりです。  

|状況|例外クラス|
|----|----|
|コンストラクタで指定された情報に不備がある|`ConfigurationHWControlError`|
|FMで認証に失敗した|`AuthenticationHWControlError`|
|引数`target_id`が指定されているデバイスが存在しない|`ResourceNotFoundHWControlError`|
|FMの状態などに何らかの異常が発生した|`ControlObjectHWControlError`|
|FMプラグインの内部エラーが発生した|`InternalHWControlError`|
|原因不明のエラーが発生した(非推奨)|`UnknownHWControlError`|

既定で使用できる例外は、`app.common.basic_exceptions`パッケージに定義されています。  
また、新たにプラグイン固有の例外を設定することが可能です。
詳細は[7. 例外処理](07_Handling_Exceptions.md)を参照ください。  

### 6.3.3. 動作確認手順

以下の手順で[HW制御機能のREST API](02_HWControlFunction.md#21-hw制御機能のrest-api)を実行します。

1. `全デバイススペック情報取得`を実行して、全デバイスのスペック情報を取得します。

本操作により`get_port_info`メソッドが引数なし、および、返却した各ポートに対応する引数を指定して呼び出されます。  
また、REST APIの返却情報に`get_port_info`メソッドで返却したポート情報の一部が含まれます。  

### 6.3.4. ポート情報

ポート情報データはポート情報クラス型 (FMPortData) のデータです。  
FMPortDataクラスは`app.common.utils.fm_plugin_base`モジュールで定義されています。  
FMPortDataクラスの各フィールドの情報は以下のとおり。  
なお、不適合なデータを指定した場合、pydantic.ValidationErrorが発生します。  

| No | フィールド名 | 型 | 概要 |
| -- | -- | -- | -- |
|  1 | id | str | FMポートIDを表す1文字以上の文字列。`get_port_info`/`connect`/`disconnect`の引数で使用できます。<BR>`get_port_info`で`target_id`を指定された場合、指定されたID。<BR>FMプラグインが対象のポートを識別するために使用する。<BR>FMポートIDはFM単位で一意とします。 |
|  2 | switch_id | Optional[str] | スイッチの識別子を1文字以上の文字列で返却します。<BR>`get_switch_info`の`switch_id`の指定に使用できます。<BR>FMから取得できない場合、または、取得時にエラー発生した場合Noneを返却します。<BR>未指定時はNoneが設定されます。 |
|  3 | switch_port_number | Optional[str] | スイッチのポート番号を文字列で返却します。<BR>switch_port_numberはスイッチ単位で一意の値とします。<BR>FMから取得できない場合、または、取得時にエラー発生した場合Noneを返却します。<BR>未指定時はNoneが設定されます。 |
|  4 | switch_port_type | Optional[str] | ポートがUSP側かDSP側か。USP側(ホスト)の場合"USP"、DSP側(デバイス)の場合"DSP"の文字列を返却します。<BR>取得時にエラー発生時Noneを返却します。<BR>未指定時はNoneが設定されます。 |
|  5 | fabric_id | Optional[str] | ファブリックを識別するための識別子を文字列で返却します。<BR>fabricIdはシステム単位で一意の値とします。<BR>他のFMプラグインで管理するfabricIdとの衝突を避けるため、fabricIdにはFMの製造元、モデル名、ファブリックに含まれるスイッチのシリアル番号を含めてください。<BR>FMにスイッチのシリアル番号を取得する機能がなく、ファブリックの識別が論理的な情報しかない場合は、コンストラクタから取得したFMへの接続情報などのFMを識別できる情報をを含めることで、衝突しない識別子を作成してください。<BR>構築後の運用時に、識別子に変更がないようにします。ただし、ファブリックを構成するスイッチの交換を行った場合は、識別子の更新が可能です。<BR>同じfabricIdを返却したFMポートID同士(USPとDSP)は接続が可能となります。<BR>スイッチの相互接続情報の取得に失敗した場合Noneを返却します。<BR>未指定時はNoneが設定されます。 |
|  6 | link | Optional[List[str]] | USP側の場合、USPとbindされているDSP側のFMポートID、<BR>DSP側の場合、DSPとbindされているUSP側のFMポートID。<BR>要素数にかかわらず、リスト形式で返却します。<BR>どこにもbindされていない場合、空のリストを返却します。<BR>取得時にエラー発生時Noneを返却します。<BR>`connect`/`disconnect`メソッドでbind/bind状態の解除をおこなうことで情報が更新されます。<BR>未指定時はNoneが設定されます。 |
|  7 | device_type | Optional[str] | デバイスの種類("CXL-Type1"/"CXL-Type2"/"CXL-Type3"/"CXL-Type3-MLD"/"PCIe"/"Undetected"/"Other"/"Unknown")を文字列で返却します。<BR>FMから取得できない場合、または、取得時にエラー発生した場合Noneを返却します。<BR>未指定時はNoneが設定されます。 |
|  8 | pci_class_code | Optional[Dict[str,int]] | DSP側に接続されているデバイスのPCIクラスコードを、"base","sub","prog"の3つの要素と0-255の整数の値を持つ辞書データで返却します。<BR>USP側の場合、または、デバイスが接続されていない場合、または、FMから取得できない場合、または、取得時にエラー発生した場合Noneを返却します。<BR>未指定時はNoneが設定されます。 |
|  9 | pcie_vendor_id | Optional[str] | DSP側に接続されているデバイスのPCIeベンダIDを4桁の16進数文字列で返却します。<BR>USP側の場合、または、デバイスが接続されていない場合、または、FMから取得できない場合、または、取得時にエラー発生した場合Noneを返却します。<BR>注意: USP側でNone以外を返却するとデバイスが正しく認識されません。<BR>未指定時はNoneが設定されます。 |
| 10 | pcie_device_id | Optional[str] | DSP側に接続されているデバイスのPCIeデバイスIDを4桁の16進数文字列で返却します。<BR>USP側の場合、または、デバイスが接続されていない場合、または、FMから取得できない場合、または、取得時にエラー発生した場合Noneを返却します。<BR>注意: USP側でNone以外を返却するとデバイスが正しく認識されません。<BR>未指定時はNoneが設定されます。 |
| 11 | pcie_device_serial_number | Optional[str] | DSP側に接続されているデバイスのPCIeデバイスシリアル番号を16桁の16進数文字列で返却します。<BR>USP側の場合、または、デバイスが接続されていない場合、または、FMから取得できない場合、または、取得時にエラー発生した場合Noneを返却します。<BR>注意: USP側でNone以外を返却するとデバイスが正しく認識されません。<BR>未指定時はNoneが設定されます。 |
| 12 | cpu_manufacturer | Optional[str] | USP側に接続されているCPUデバイス(ホスト)のベンダ名を1文字以上の文字列で返却します。<BR>DSP側の場合、または、FMから取得できない場合、または、取得時にエラー発生した場合Noneを返却します。<BR>注意: DSP側でNone以外を返却するとデバイスが正しく認識されません。<BR>未指定時はNoneが設定されます。 |
| 13 | cpu_model | Optional[str] | USP側に接続されているCPUデバイス(ホスト)のモデル名を1文字以上の文字列で返却します。<BR>DSP側の場合、または、FMから取得できない場合、または、取得時にエラー発生した場合Noneを返却します。<BR>注意: DSP側でこの情報を返却するとデバイスが正しく認識されません。<BR>未指定時はNoneが設定されます。 |
| 14 | cpu_serial_number | Optional[str] | USP側に接続されているCPUデバイス(ホスト)のシリアル番号を1文字以上の文字列で返却します。<BR>DSP側の場合、または、FMから取得できない場合、または、取得時にエラー発生した場合Noneを返却します。<BR>注意: DSP側でNone以外を返却するとデバイスが正しく認識されません。<BR>未指定時はNoneが設定されます。 |
| 15 | ltssm_state | Optional[str] | ポートのLTSSM状態("L0"/"L0s"/"L2"/"Detect"/"Polling"/"Configuration"/"Recovery"/"HotReset"/"Disable"/"Loopback")を文字列で返却します。<BR>FMから取得できない場合、または、取得時にエラー発生した場合Noneを返却します。<BR>未指定時はNoneが設定されます。 |
| 16 | device_keys | dict | デバイスを一意に識別可能な、FMから取得可能な固有の情報を、辞書形式で返却します。<BR>OOBプラグインが返却するデバイス情報との紐づけに使用します。<BR>返却するキーは可変ですが、デバイスの種類などに応じてFMとOOBであらかじめ決めておく必要があり、該当のキーは必ず返却する必要があります。<BR>決められたキーの情報を取得できない場合は、値をNoneとした辞書データを返却します。<BR>詳細は[9.1 注意事項 デバイスの紐づけ](09_Special_Notes.md#デバイスの紐づけ)を参照ください。<BR>未指定時は{}が設定されます。 |
| 17 | port_keys | dict | スイッチのポートを一意に識別可能な、FMから取得可能な固有の情報を、辞書形式で返却します。<BR>OOBプラグインが返却するデバイス情報との紐づけに使用します。<BR>返却するキーは可変ですが、デバイスの種類などに応じてFMとOOBであらかじめ決めておく必要があり、該当のキーは必ず返却する必要があります。<BR>決められたキーの情報を取得できない場合は、値をNoneとした辞書データを返却します。<BR>詳細は[9.1 注意事項 デバイスの紐づけ](09_Special_Notes.md#デバイスの紐づけ)を参照ください。<BR>未指定時は{}が設定されます。 |
| 18 | capacity | Optional[Dict[str,int]] | 容量に関する情報を"volatile"、"persistent"、"total"のうち1～3個のキーを持つ辞書データまたはNoneで返却します。<BR>"volatile"、"persistent"、"total"はそれぞれ揮発性容量(byte)、不揮発性容量(byte)、合計容量(byte)を0以上の数値型で返却します。<BR>"volatile" のみの辞書が指定された場合、"persistent"が0で"total"が"volatile"と同じデータに補完されます。<BR>"persistent" のみの辞書が指定された場合、"volatile"が0で"total"が"persistent"と同じデータに補完されます。<BR>2つのキーの辞書が指定された場合、"volatile"+"persistent"="total" になるように指定されなかったキーが補完されます。<BR>"total"のみの指定、2つのキーの計算結果が負、または、"volatile"+"persistent"が"total"に一致しない値は指定はできません。<BR>デバイス種別がCXL-Type3で情報の取得に失敗した場合、capacityの値はNoneを返却します。<BR>未指定時はNoneが設定されます。 |

## 6.4. `get_switch_info(switch_id=None)`

```python
get_switch_info(target_id: str = None) -> dict[str, list[FMSwitchData]]:
```

FMが管理しているスイッチの情報を取得する機能を持つメソッド

### 6.4.1. 引数

- `switch_id`  
スイッチの識別子を指定します。省略が可能です。  
引数を指定した場合、指定したスイッチの情報を返却します。  
引数を省略した場合、FMが管理するすべてのスイッチの情報を返却します。  

### 6.4.2. 返り値

dataキーを持つ辞書型を返却します。  
dataキーの値は対象のスイッチ情報(スイッチ情報クラス型)のリスト(リスト型)を返します。  
引数を指定した場合、指定したスイッチのスイッチ情報を返却します。  
引数を省略した場合、すべてのスイッチのスイッチ情報を返却します。  

スイッチ情報の詳細は[6.4.4. スイッチ情報](#644-スイッチ情報)を参照ください。  
返却対象のすべての スイッチが取得できた場合は、それらのスイッチに対するスイッチ情報を返却します。  
障害などで、取得出来ていないスイッチ(switchId)があった場合は異常とします。  
取得時に障害はなくても、設置時の不備などで有効なスイッチ(switchId)が1つもない場合も、異常とします。  
異常時は、`BaseHWControlError`を継承した例外を発生させます。  
`get_switch_info`メソッドが既定で使用できる例外は以下の表に記載のとおりです。  

|状況|例外クラス|
|----|----|
|コンストラクタで指定された情報に不備がある|`ConfigurationHWControlError`|
|FMで認証に失敗した|`AuthenticationHWControlError`|
|引数`switch_id`で指定されたスイッチが存在しない|`SwitchNotFoundHWControlError`|
|FMの状態などに何らかの異常が発生した|`ControlObjectHWControlError`|
|FMプラグインの内部エラーが発生した|`InternalHWControlError`|
|原因不明のエラーが発生した(非推奨)|`UnknownHWControlError`|

既定で使用できる例外は、`app.common.basic_exceptions`パッケージに定義されています。  
また、新たにプラグイン固有の例外を設定することが可能です。
詳細は[7. 例外処理](07_Handling_Exceptions.md)を参照ください。  

### 6.4.3. 動作確認手順

以下の手順で[HW制御機能のREST API](02_HWControlFunction.md#21-hw制御機能のrest-api)を実行します。

1. `デバイスID一覧情報取得`を実行して、デバイスIDの一覧を取得します。

本操作により返却される情報にスイッチの情報は含まれませんが、`get_switch_info`メソッドが引数なしで呼び出されます。  
なお、現時点でHW制御機能から引数を指定して実行されることはありません。  

### 6.4.4. スイッチ情報

スイッチ情報データはスイッチ情報クラス型 (FMSwitchData) のデータです。  
FMSwitchDataクラスは`app.common.utils.fm_plugin_base`モジュールで定義されています。  
FMSwitchDataクラスの各フィールドの情報は以下のとおり。  
なお、不適合なデータを指定した場合、pydantic.ValidationErrorが発生します。  

| No | フィールド名 | 型 | 概要 |
| -- | -- | -- | -- |
|  1 | switch_id | str | スイッチの識別子を1文字以上の文字列で返却します。<BR>ポート情報のswitchIdと同じ値。`get_switch_info`で`switch_id`を指定された場合、指定されたスイッチの識別子。<BR>FMプラグインがスイッチを識別するために使用します。<BR>switchIdはFM単位で一意の値とします。 |
|  2 | switch_manufacturer | Optional[str] | スイッチの製造元を1文字以上の文字列で返却します。<BR>FMから取得できない場合、または、取得時にエラー発生した場合Noneを返却します。<BR>未指定時はNoneが設定されます。 |
|  3 | switch_model | Optional[str] | スイッチのモデルを1文字以上の文字列で返却します。<BR>FMから取得できない場合、または、取得時にエラー発生した場合Noneを返却します。<BR>未指定時はNoneが設定されます。 |
|  4 | switch_serial_number | Optional[str] | スイッチのシリアル番号を1文字以上の文字列で返却します。<BR>FMから取得できない場合、または、取得時にエラー発生した場合Noneを返却します。<BR>未指定時はNoneが設定されます。 |
|  5 | link | Optional[List[str]] | ケーブルで直接接続されているスイッチの識別子をリスト形式で返却します。<BR>スイッチが他のスイッチと接続されていない場合、空のリストを返却します。<BR>FMから取得できない場合、または、取得時にエラー発生した場合Noneを返却します。<BR>未指定時はNoneが設定されます。 |
