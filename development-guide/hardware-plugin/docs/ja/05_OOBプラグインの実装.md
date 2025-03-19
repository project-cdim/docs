# 5. OOBプラグインの実装

本章ではOOBプラグインの仕様をメソッドごとに説明します。

## 5.1. `get_device_info()`

``` python
get_device_info() -> list[OOBDeviceListItem]
```

マネージャーが制御対象とするデバイスの識別情報を取得します。

### 5.1.1. 引数

なし。

### 5.1.2. 返り値

デバイスの識別情報を格納した`OOBDeviceListItem`のリストです([表5-2. `get_device_info`の返り値](05a_OOBプラグインの実装_別紙.md#表5-2-get_device_infoの返り値)参照)。  
異常時は下記の例外を送出します。

|No.|状況                                      |例外
|:-:|------------------------------------------|------------------------------------------------------------------------
| 1 |OOBで認証に失敗した場合                   |[`AuthenticationHwControlError`](07_例外処理.md#71-例外クラスの構造)
| 2 |マネージャーがエラーを応答した場合        |[`ControlObjectHwControlError`](07_例外処理.md#ベース例外クラス)

### 5.1.3. 動作確認手順

以下の手順で[HW制御機能のREST API](02_HW制御機能.md#21-hw制御機能のrest-api)を実行します。

1. `デバイスID一覧情報取得`を実行して、デバイスIDの一覧を取得します。

REST APIで返却される`deviceID`はHW制御機能により生成された一意な文字列になります。  
この`deviceID`がプラグインにより収集されたどのデバイスに対応するかは`スペック情報取得`で確認します。

## 5.2. `get_spec_info(key_values)`

``` python
get_spec_info(key_values: list[dict[str, str]]) -> dict[str, list[dict]]
```

指定されたデバイスのスペック情報を取得します(複数指定可)。

### 5.2.1. 引数

- `key_values`  
  OOBデバイスIDとデバイス種別を格納した辞書のリストです([表5-3. 引数`key_values`](05a_OOBプラグインの実装_別紙.md#表5-3-引数key_values)を参照)。

### 5.2.2. 返り値

デバイスごとのスペック情報を格納した辞書です([表5-4. `get_spec_info`の返り値](05a_OOBプラグインの実装_別紙.md#表5-4-get_spec_infoの返り値)を参照)。  
異常時は下記の例外を送出します。

|No.|状況                                      |例外
|:-:|------------------------------------------|------------------------------------------------------------------------
| 1 |指定されたデバイスのデバイス種別がプラグインのサポート対象外の場合 |[`RequestNotSupportedHwControlError`](07_例外処理.md#72-定義済み例外)
| 2 |デバイスが存在しない場合                  |[`DeviceNotFoundHwControlError`](07_例外処理.md#72-定義済み例外)
| 3 |OOBで認証に失敗した場合                   |[`AuthenticationHwControlError`](07_例外処理.md#71-例外クラスの構造)
| 4 |マネージャーがエラーを応答した場合        |[`ControlObjectHwControlError`](07_例外処理.md#ベース例外クラス)

### 5.2.3. 動作確認手順

以下の手順で[HW制御機能のREST API](02_HW制御機能.md#21-hw制御機能のrest-api)を実行します。

1. `デバイスID一覧情報取得`を実行して、デバイスIDの一覧を取得します。
2. 取得したデバイスIDを指定して`スペック情報取得`を実行し、デバイスのスペック情報を取得します。

プラグインの返り値とREST APIの項目名の対応は[表5-5. スペック情報とREST APIの項目名対応](05a_OOBプラグインの実装_別紙.md#表5-5-スペック情報とrest-apiの項目名対応)を参照してください。

## 5.3. `get_metric_info(key_values)`

``` python
get_metric_info(key_values: list[dict[str, str]]) -> dict[str, list[dict]]
```

指定されたデバイスのメトリック情報を取得します(複数指定可)。

### 5.3.1. 引数

- `key_values`  
  OOBデバイスIDとデバイス種別を格納した辞書のリストです([表5-3. 引数`key_values`](05a_OOBプラグインの実装_別紙.md#表5-3-引数key_values)を参照)。  
  本メソッドの場合、デバイス種別は`CPU`、`GPU`、`memory`、`storage`、`networkInterface`のいずれかとなります。

### 5.3.2. 返り値

デバイスごとのメトリック情報を格納した辞書です([表5-6. `get_metric_info`の返り値](05a_OOBプラグインの実装_別紙.md#表5-6-get_metric_infoの返り値)を参照)。  
異常時は下記の例外を送出します。

|No.|状況                                      |例外
|:-:|------------------------------------------|------------------------------------------------------------------------
| 1 |指定されたデバイスのデバイス種別がプラグインのサポート対象外の場合 |[`RequestNotSupportedHwControlError`](07_例外処理.md#72-定義済み例外)
| 2 |デバイスが存在しない場合                  |[`DeviceNotFoundHwControlError`](07_例外処理.md#72-定義済み例外)
| 3 |OOBで認証に失敗した場合                   |[`AuthenticationHwControlError`](07_例外処理.md#71-例外クラスの構造)
| 4 |マネージャーがエラーを応答した場合        |[`ControlObjectHwControlError`](07_例外処理.md#ベース例外クラス)

### 5.3.3. 動作確認手順

以下の手順で[HW制御機能のREST API](02_HW制御機能.md#21-hw制御機能のrest-api)を実行します。

1. `デバイスID一覧情報取得`を実行して、デバイスIDの一覧を取得します。
2. 取得したデバイスIDを指定して`メトリック情報取得`を実行し、デバイスのメトリック情報を取得します。

プラグインの返り値とREST APIの項目名の対応は[表5-7.メトリック情報とREST APIの項目名対応](05a_OOBプラグインの実装_別紙.md#表5-7-メトリック情報とrest-apiの項目名対応)参照してください。

## 5.4. `get_power_state(key_values)`

``` python
get_power_state(key_values: list[dict[str, str]]) -> dict[str, list[dict]]
```

指定されたデバイスの電源状態を取得します(複数指定可)。

### 5.4.1. 引数

- `key_values`  
  OOBデバイスIDとデバイス種別を格納した辞書のリストです([表5-3. 引数`key_values`](05a_OOBプラグインの実装_別紙.md#表5-3-引数key_values)を参照)。

### 5.4.2. 返り値

デバイスごとの電源状態を格納した辞書です([表5-8. `get_power_state`の返り値](05a_OOBプラグインの実装_別紙.md#表5-8-get_power_stateの返り値)を参照)。  
異常時は下記の例外を送出します。

|No.|状況                                      |例外
|:-:|------------------------------------------|------------------------------------------------------------------------
| 1 |指定されたデバイスのデバイス種別がプラグインのサポート対象外の場合 |[`RequestNotSupportedHwControlError`](07_例外処理.md#72-定義済み例外)
| 2 |デバイスが存在しない場合                  |[`DeviceNotFoundHwControlError`](07_例外処理.md#72-定義済み例外)
| 3 |OOBで認証に失敗した場合                   |[`AuthenticationHwControlError`](07_例外処理.md#71-例外クラスの構造)
| 4 |マネージャーがエラーを応答した場合        |[`ControlObjectHwControlError`](07_例外処理.md#ベース例外クラス)

### 5.4.3. 動作確認手順

以下の手順で[HW制御機能のREST API](02_HW制御機能.md#21-hw制御機能のrest-api)を実行します。

1. デバイス種別に`CPU`を指定して`デバイスID一覧情報取得`を実行し、デバイスIDの一覧を取得します。
2. `OS起動確認`を実行するための設定を行います。  
   ※ `OS起動確認`はデバイスで稼働するエージェントにアクセスします。以下の手順でエージェントを[スタブ](03_開発環境の構築.md#31-スタブのセットアップ)に設定します。
   1. `hw-control/data/device_id_info.json`を開き、`DeviceID`が1.で取得したデバイスIDに一致するオブジェクトを探します。

   2. `fmPortID`に設定されている値を記録します。以下に例を示します。

      ``` json
      {
        "DeviceID":"f1f1c82b-9612-4623-8238-d16906812854",
        "deviceType":"CPU",
        "fmPortID":{
          "FM1":[
            "e4021cb4-79d9-438a-a8e9-60939fe01deb"
          ]
        },
        ..
      ```

      この例では、デバイスIDが`f1f1c82b-9612-4623-8238-d16906812854`、FMマネージャーIDが`FM1`、`fmPortID`が`e4021cb4-79d9-438a-a8e9-60939fe01deb`です。  
      `fmPortID`が設定されていない(空のオブジェクトの)場合は上記の例のように設定します。

   3. `hw-control/config/os_ipaddress.yaml`を開き、記録または設定した`fmPortID`の`IPAddress`を`localhost`に設定します。

      ``` yaml
      OS_IPAddress:
          - fmPortID: "e4021cb4-79d9-438a-a8e9-60939fe01deb"
            IPAddress: "localhost"
      ```

   4. HW制御機能を再起動します。

3. 1.で取得したデバイスIDを指定して`OS起動確認`を実行します。

`OS起動確認`は、デバイスの電源状態が`On`または`PoweringOn`のとき成功します。  
それ以外のとき失敗し、下記のようなエラーを出力します。

``` json
{
  "code": "EF003BAS007",
  "message": "The specified device power state is already off."
}
{
  "code": "EF010BAS000",
  "message": "The server encountered an internal error. The specified device power state is unexpected."
}
```

## 5.5. `post_power_on(key_values)`

``` python
post_power_on(key_values: list[dict[str, str]]) -> dict[str, list[dict]]
```

指定されたデバイスの電源をONにします(複数指定可)。  
デバイスの電源がONの場合は処理をスキップし、ステータスを正常とします。

### 5.5.1. 引数

- `key_values`  
  OOBデバイスIDとデバイス種別を格納した辞書のリストです([表5-3. 引数`key_values`](05a_OOBプラグインの実装_別紙.md#表5-3-引数key_values)を参照)。

### 5.5.2. 返り値

実行結果を格納した辞書です([表5-9. 更新メソッドの返り値](05a_OOBプラグインの実装_別紙.md#表5-9-更新メソッドの返り値)参照)。  
異常時は下記の例外を送出します。

|No.|状況                                      |例外
|:-:|------------------------------------------|------------------------------------------------------------------------
| 1 |指定されたデバイスのデバイス種別がプラグインのサポート対象外の場合 |[`RequestNotSupportedHwControlError`](07_例外処理.md#72-定義済み例外)
| 2 |デバイスが存在しない場合                  |[`DeviceNotFoundHwControlError`](07_例外処理.md#72-定義済み例外)
| 3 |デバイスが電源操作不可の場合              |[`RequestNotSupportedHwControlError`](07_例外処理.md#72-定義済み例外)
| 4 |電源ONに失敗した場合                      |[`PowerOnFailureHwControlError`](07_例外処理.md#72-定義済み例外)
| 5 |OOBで認証に失敗した場合                   |[`AuthenticationHwControlError`](07_例外処理.md#71-例外クラスの構造)
| 6 |マネージャーがエラーを応答した場合        |[`ControlObjectHwControlError`](07_例外処理.md#ベース例外クラス)

### 5.5.3. 動作確認手順

以下の手順で[HW制御機能のREST API](02_HW制御機能.md#21-hw制御機能のrest-api)を実行します。

1. `デバイスID一覧情報取得`を実行して、デバイスIDの一覧を取得します。
2. 取得したデバイスIDを指定し、リクエストボディを`{"action": "on"}`として`電源制御`を実行します。

## 5.6. `post_power_off(key_values)`

``` python
post_power_off(key_values: list[dict[str, str]]) -> dict[str, list[dict]]
```

指定されたデバイスの電源をOFFにします(複数指定可)。  
デバイスの電源がOFFの場合は処理をスキップし、ステータスを正常とします。

### 5.6.1. 引数

- `key_values`  
  OOBデバイスIDとデバイス種別を格納した辞書のリストです([表5-3. 引数`key_values`](05a_OOBプラグインの実装_別紙.md#表5-3-引数key_values)を参照)。

### 5.6.2. 返り値

実行結果を格納した辞書です([表5-9. 更新メソッドの返り値](05a_OOBプラグインの実装_別紙.md#表5-9-更新メソッドの返り値)参照)。  
異常時は下記の例外を送出します。

|No.|状況                                      |例外
|:-:|------------------------------------------|------------------------------------------------------------------------
| 1 |指定されたデバイスのデバイス種別がプラグインのサポート対象外の場合 |[`RequestNotSupportedHwControlError`](07_例外処理.md#72-定義済み例外)
| 2 |デバイスが存在しない場合                  |[`DeviceNotFoundHwControlError`](07_例外処理.md#72-定義済み例外)
| 3 |デバイスが電源操作不可の場合              |[`RequestNotSupportedHwControlError`](07_例外処理.md#72-定義済み例外)
| 4 |電源OFFに失敗した場合                     |[`PowerOffFailureHwControlError`](07_例外処理.md#72-定義済み例外)
| 5 |OOBで認証に失敗した場合                   |[`AuthenticationHwControlError`](07_例外処理.md#71-例外クラスの構造)
| 6 |マネージャーがエラーを応答した場合        |[`ControlObjectHwControlError`](07_例外処理.md#ベース例外クラス)

### 5.6.3. 動作確認手順

以下の手順で[HW制御機能のREST API](02_HW制御機能.md#21-hw制御機能のrest-api)を実行します。

1. `デバイスID一覧情報取得`を実行して、デバイスIDの一覧を取得します。
2. 取得したデバイスIDを指定し、リクエストボディを`{"action": "force-off"}`として`電源制御`を実行します。

## 5.7. `post_cpu_reset(key_values)`

``` python
post_cpu_reset(key_values: list[dict[str, str]]) -> dict[str, list[dict]]
```

指定されたCPUをリセットします(複数指定可)。

### 5.7.1. 引数

- `key_values`  
  OOBデバイスIDとデバイス種別を格納した辞書のリストです([表5-3. 引数`key_values`](05a_OOBプラグインの実装_別紙.md#表5-3-引数key_values)を参照)。

### 5.7.2. 返り値

実行結果を格納した辞書です([表5-9. 更新メソッドの返り値](05a_OOBプラグインの実装_別紙.md#表5-9-更新メソッドの返り値)参照)。  
異常時は下記の例外を送出します。

|No.|状況                                      |例外
|:-:|------------------------------------------|------------------------------------------------------------------------
| 1 |指定されたデバイスのデバイス種別がプラグインのサポート対象外の場合 |[`RequestNotSupportedHwControlError`](07_例外処理.md#72-定義済み例外)
| 2 |デバイスが存在しない場合                  |[`DeviceNotFoundHwControlError`](07_例外処理.md#72-定義済み例外)
| 3 |デバイスが電源操作不可の場合              |[`RequestNotSupportedHwControlError`](07_例外処理.md#72-定義済み例外)
| 4 |デバイスの電源がOFFの場合                 |[`RequestConflictHwControlError`](07_例外処理.md#ベース例外クラス)
| 5 |CPUリセットに失敗した場合                 |[`CpuResetFailureHwControlError`](07_例外処理.md#72-定義済み例外)
| 6 |OOBで認証に失敗した場合                   |[`AuthenticationHwControlError`](07_例外処理.md#71-例外クラスの構造)
| 7 |マネージャーがエラーを応答した場合        |[`ControlObjectHwControlError`](07_例外処理.md#ベース例外クラス)

### 5.7.3. 動作確認手順

以下の手順で[HW制御機能のREST API](02_HW制御機能.md#21-hw制御機能のrest-api)を実行します。

1. デバイス種別に`CPU`を指定して`デバイスID一覧情報取得`を実行し、デバイスIDの一覧を取得します。
2. 取得したデバイスIDを指定し、リクエストボディを`{"action": "reset"}`として`電源制御`を実行します。

## 5.8. `post_os_shutdown(key_values)`

``` python
post_os_shutdown(key_values: list[dict[str, str]]) -> dict[str, list[dict]]
```

指定されたデバイスのOSをシャットダウンします(複数指定可)。  
デバイスの電源がOFFの場合は処理をスキップし、ステータスを正常とします。

### 5.8.1. 引数

- `key_values`  
  OOBデバイスIDとデバイス種別を格納した辞書のリストです([表5-3. 引数`key_values`](05a_OOBプラグインの実装_別紙.md#表5-3-引数key_values)を参照)。

### 5.8.2. 返り値

実行結果を格納した辞書です([表5-9. 更新メソッドの返り値](05a_OOBプラグインの実装_別紙.md#表5-9-更新メソッドの返り値)参照)。  
異常時は下記の例外を送出します。

|No.|状況                                      |例外
|:-:|------------------------------------------|------------------------------------------------------------------------
| 1 |指定されたデバイスのデバイス種別がプラグインのサポート対象外の場合 |[`RequestNotSupportedHwControlError`](07_例外処理.md#72-定義済み例外)
| 2 |デバイスが存在しない場合                  |[`DeviceNotFoundHwControlError`](07_例外処理.md#72-定義済み例外)
| 3 |デバイスが電源操作不可の場合              |[`RequestNotSupportedHwControlError`](07_例外処理.md#72-定義済み例外)
| 4 |OSシャットダウンに失敗した場合            |[`PowerOffFailureHwControlError`](07_例外処理.md#72-定義済み例外)
| 5 |OOBで認証に失敗した場合                   |[`AuthenticationHwControlError`](07_例外処理.md#71-例外クラスの構造)
| 6 |マネージャーがエラーを応答した場合        |[`ControlObjectHwControlError`](07_例外処理.md#ベース例外クラス)

### 5.8.3. 動作確認手順

以下の手順で[HW制御機能のREST API](02_HW制御機能.md#21-hw制御機能のrest-api)を実行します。

1. デバイス種別に`CPU`を指定して`デバイスID一覧情報取得`を実行し、デバイスIDの一覧を取得します。
2. 取得したデバイスIDを指定し、リクエストボディを`{"action": "off"}`として`電源制御`を実行します。

`電源制御`はエージェントにアクセス可能な場合はエージェントに、そうでない場合はプラグインにOSシャットダウンを要求します。  
[`get_power_state`の動作確認](#543-動作確認手順)でデバイスとエージェントの対応づけ(`os_ipaddress.yaml`の編集)を行っている場合、  
その設定を削除してプラグインにOSシャットダウン要求が行われるようにしてください。
