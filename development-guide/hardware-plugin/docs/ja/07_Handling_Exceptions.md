# 7. 例外処理

プラグインの実行中に発生したエラーは、`BaseHWControlError`を継承したクラスにエラー情報を設定して返す必要があります。  
これらのエラー情報は、多くの場合、HW制御機能を呼び出した上位のモジュールに返却するエラー情報として使用されます。  
さまざまな HW Control Errorを確認して、エラー状況に最適なものを使用してください。  

本章では、以下について記載します。

* [7.1. 例外クラスの構造](#71-例外クラスの構造): HW制御機能が定義する異常時に発生させる例外クラスの構造
* [7.2. 定義済み例外](#72-定義済み例外): プラグインで発生する異常に対して定義されている例外クラスの一覧
* [7.3. 例外の追加](#73-例外の追加): プラグインで新たな例外クラスを作成する方法

なお、例外処理については、現在仕様を策定中の部分があり、次期リリース以降で非互換の更新可能性があります。

## 7.1. 例外クラスの構造

HW制御機能で使用する例外はHW制御機能の`app.common.basic_exceptions`パッケージに定義されています。  
HW制御機能で使用する例外は以下に定義したクラスから派生しています。  

### 基底の例外クラス

```python
class BaseHWControlError(Exception):
```

この例外クラスはPythonに組み込みの`Exception`クラスを継承しています。  
この例外クラスは以下の属性を持ちます。  

* `http_code(int)`
  * エラーの時のHTTPレスポンスに用いるHTTPステータスコード。
* `error_code(str)`
  * エラーの時のHTTPレスポンスのbodyに用いるエラーコード。
  * 詳細は[エラーコード](#エラーコード)を参照ください。
* `default_error_message(str)`
  * 例外クラスに設定されるデフォルトエラーメッセージ。
* `message(str)`
  * エラーの時のHTTPレスポンスのbodyに用いるエラーメッセージ。
  * 例外クラスに設定されたエラーメッセージを参照する際に使用できます。

この例外クラスは以下のメソッドを持ちます。

* `__init__(*args: object, additional_message: str = "")`
  * この例外クラスのコンストラクタ。
  * 引数:
    * `args(object)`: トレースバックに出力するエラー情報として継承元のコンストラクタに引き渡されます。
    * `additional_message(str)`: 追加のエラーメッセージとして`default_error_message`に結合されます。結合されたメッセージは`message`によって参照できます。

### エラーコード

エラーコードは、以下の項目から構成されたエラーを識別する情報で合計11文字から生成される文字列です。
エラーコードの構成要素は以下となります。

|設定項目|位置|説明|
|--------|----|----|
|エラーレベル|1|'C': 致命的な障害が発生してHW制御機能のサービスの継続が困難な状態<BR>'E': 障害葉発生したが、HW制御機能サービスは継続可能な状態|
|リトライ可否|2|'F': 同じ要求を再度実行しても成功しない状態<BR>'R': 同じ要求を再度実行して成功する可能性がある状態(リソース不足や競合など)|
|ベース例外クラスコード|3-5|3桁の10進数表記を文字列で表した、エラーの内容を大きく分類した例外クラス<BR>具体的な種類については[ベース例外クラス](#ベース例外クラス)を参照ください。|
|ベンダ依存拡張例外クラスコード|6-8|プラグインで追加したエラーコードを識別するための3文字の大文字アルファベット<BR>HW制御機能で定義している例外は"BAS"とする<BR>各プラグインで他のプラグインと重ならない文字列を使用する。<BR>プラグインでの例外追加については[7.3 例外の追加](#73-例外の追加)を参照ください。|
|詳細例外クラスコード|9-11|3桁の10進数表記の文字列で同一のベース例外クラス/ベンダ依存拡張例外クラス内で例外を識別するためのコード|

### ベース例外クラス

ベース例外クラスは、エラーコードで分類されるベースの例外で、基底の例外クラスを継承しています。  
以下が定義されています。

* `UnknownHWControlError`
  * この例外は、原因不明な致命的なエラーが発生した際に送出してください。たとえば、処理の継続によりハードウェアの破壊につながりかねないようなケースなどを想定しています。
  * ベース例外クラスコード: `"001"`
  * エラーコード: `"CF001BAS000"`
  * HTTPステータスコード: `500`
  * デフォルトエラーメッセージ: `"The server encountered an internal error and was unable to complete your request."`

* `AuthenticationHWControlError`
  * この例外は、認証関連のエラーが発生した際に送出してください。
  * ベース例外クラスコード: `"002"`
  * エラーコード: `"EF002BAS000"`
  * HTTPステータスコード: `401`
  * デフォルトエラーメッセージ: `"Authentication failed."`

* `BadRequestHWControlError`
  * この例外は、リクエスト内容の不備によるエラーが発生した際に送出してください。たとえば、電源制御をサポートしていないデバイスに電源制御をリクエストされたケースなどを想定します。
  * ベース例外クラスコード: `"003"`
  * エラーコード: `"EF003BAS000"`
  * HTTPステータスコード: `400`
  * デフォルトエラーメッセージ: `"Your request is invalid."`

* `ControlObjectHWControlError`
  * この例外は、OOBコントローラー、Fabric Managerがエラーを起こした際に送出してください。
  * ベース例外クラスコード: `"004"`
  * エラーコード: `"EF004BAS000"`
  * HTTPステータスコード: `500`
  * デフォルトエラーメッセージ: `"Failed to operate the specified device."`

* `ResourceBusyHWControlError`
  * この例外は、指定されたリソースの状態がビジーであり、リクエストされた処理を実行できないときに送出してください。
  * ベース例外クラスコード: `"005"`
  * エラーコード: `"ER005BAS000"`
  * HTTPステータスコード: `503`
  * デフォルトエラーメッセージ: `"The specified resource is busy."`

* `ConfigurationHWControlError`
  * この例外は、hw-controlの設定または構成の不備が原因でエラーが起きた際に送出してください。たとえば、プラグイン設定ファイルの不備によって処理が実行できないケースなどを想定します。
  * ベース例外クラスコード: `"007"`
  * エラーコード: `"EF007BAS000"`
  * HTTPステータスコード: `500`
  * デフォルトエラーメッセージ: `"Your request failed due to the missing required system configuration."`

* `InternalHWControlError`
  * この例外は、プラグインも含めたhw-controlアプリケーションの内部エラーが起きた際に送出してください。
  * ベース例外クラスコード: `"010"`
  * エラーコード: `"EF010BAS000"`
  * HTTPステータスコード: `500`
  * デフォルトエラーメッセージ: `"The server encountered an internal error."`

* `RequestConflictHWControlError`
  * この例外は、指定されたリソースの状態がリクエスト内容と競合した場合に送出してください。たとえば、すでに他のデバイスと接続されているデバイスに対して、さらに別のデバイスへの接続が要求された場合などを想定します。
  * ベース例外クラスコード: `"011"`
  * エラーコード: `"EF011BAS000"`
  * HTTPステータスコード: `409`
  * デフォルトエラーメッセージ: `"The request conflicts with the current resource state."`

* `DependencyServiceHWControlError`
  * この例外は、hw-controlの外部にあるCDIMコンポーネントでエラーが発生したことが原因で、処理が失敗した場合に送出してください。
  * ベース例外クラスコード: `"012"`
  * エラーコード: `"EF012BAS000"`
  * HTTPステータスコード: `500`
  * デフォルトエラーメッセージ: `"Operation could not be completed due to a failure in external dependencies."`

* `DeviceNotFoundHWControlError`
  * この例外は、制御または情報取得対象のデバイスが存在しない場合に送出してください。。
  * ベース例外クラスコード: `"013"`
  * エラーコード: `"EF013BAS000"`
  * HTTPステータスコード: `404`
  * デフォルトエラーメッセージ: `"The specified target device is not found."`

## 7.2. 定義済み例外

以下に記載する例外クラスは、プラグインで異常を検出したときに使用することを想定した例外クラスで、ベース例外クラスコードが同じベース例外クラスを継承しています。  
ベース例外クラスを継承したこれらのクラスを詳細例外クラスと呼びます。  

* `OOBAuthenticationHWControlError`
  * OOBコントローラーへの認証に失敗した際に送出してください。
  * ベースクラス：`AuthenticationHWControlError`
  * 対象プラグイン: OOB
  * エラーコード：`"EF002BAS002"`
  * HTTPステータスコード:`401`
  * デフォルトエラーメッセージ:`"Authentication to the Out-of-Band Controller failed."`

* `HostCPUNotFoundHWControlError`
  * **非推奨**
  * このクラスは従来のプラグインとの互換性維持のため現状残していますが、次期リリースで削除予定です。`UpstreamDeviceNotFoundHWControlError`の使用をするようにしてください。
  * ベースクラス：`DeviceNotFoundHWControlError`
  * 対象プラグイン: FM
  * エラーコード: `"EF013BAS001"`
  * HTTPステータスコード: `404`
  * デフォルトエラーメッセージ: `"The specified Host CPU is not found."`

* `HostCPUAndDeviceNotFoundHWControlError`
  * **非推奨**
  * このクラスは従来のプラグインとの互換性維持のため現状残していますが、次期リリースで削除予定です。FMプラグインの`connect`または`disconnect`メソッドで、対象デバイスが存在しないことが判明した時点で`UpstreamDeviceNotFoundHWControlError`または`DownstreamDeviceNotFoundHWControlError`を`raise`するようにしてください。
  * ベースクラス：`DeviceNotFoundHWControlError`
  * 対象プラグイン: FM
  * エラーコード: `"EF013BAS002"`
  * HTTPステータスコード: `404`
  * デフォルトエラーメッセージ: `"The specified Host CPU and target device are not found."`

* `UpstreamDeviceNotFoundHWControlError`
  * FMプラグインの`connect`または`disconnect`メソッドで、指定されたUSPにデバイスが存在しなかった場合に送出してください。
  * ベースクラス：`DeviceNotFoundHWControlError`
  * 対象プラグイン: FM
  * エラーコード: `"EF013BAS000"`（継承元の値をそのまま利用する）
  * HTTPステータスコード: `404`
  * デフォルトエラーメッセージ: `"The specified target device is not found."`（継承元の値をそのまま利用する）

* `DownstreamDeviceNotFoundHWControlError`
  * FMプラグインの`connect`または`disconnect`メソッドで、指定されたDSPにデバイスが存在しなかった場合に送出してください。
  * ベースクラス：`DeviceNotFoundHWControlError`
  * 対象プラグイン: FM
  * エラーコード: `"EF013BAS000"`（継承元の値をそのまま利用する）
  * HTTPステータスコード: `404`
  * デフォルトエラーメッセージ: `"The specified target device is not found."`（継承元の値をそのまま利用する）

* `ResourceNotFoundHWControlError`
  * FMプラグインで、指定されたリソースが存在しない場合に送出してください。
  * ベースクラス：`DeviceNotFoundHWControlError`
  * 対象プラグイン: FM
  * エラーコード: `"EF013BAS003"`
  * HTTPステータスコード: `404`
  * デフォルトエラーメッセージ: `"The specified resource is not found."`

* `SwitchNotFoundHWControlError`
  * FMプラグインで、指定されたスイッチが存在しない場合に送出してください。
  * ベースクラス：`DeviceNotFoundHWControlError`
  * 対象プラグイン: FM
  * エラーコード: `"EF013BAS004"`
  * HTTPステータスコード: `404`
  * デフォルトエラーメッセージ: `"The specified switch is not found."`

* `RequestNotSupportedHWControlError`
  * 指定されたデバイスに対してサポートされていない処理がリクエストされた場合に送出してください。
  * ベースクラス：`DeviceNotFoundHWControlError`
  * 対象プラグイン: OOB
  * エラーコード: `"EF003BAS010"`
  * HTTPステータスコード: `400`
  * デフォルトエラーメッセージ: `"Your request is not supported for the specified target device."`

* `FMConnectFailureHWControlError`
  * Fabric Managerが指定されたHost CPUとデバイス間の接続に失敗した場合に送出してください。
  * ベースクラス：`ControlObjectHWControlError`
  * 対象プラグイン: FM
  * エラーコード: `"EF004BAS001"`
  * HTTPステータスコード: `500`
  * デフォルトエラーメッセージ: `"The Fabric Manager failed to establish a connection between the specified Host CPU and target device."`

* `FMDisconnectFailureHWControlError`
  * Fabric Managerが指定されたHost CPUとデバイスの切断に失敗した場合に送出してください。
  * ベースクラス：`ControlObjectHWControlError`
  * 対象プラグイン: FM
  * エラーコード: `"EF004BAS002"`
  * HTTPステータスコード: `500`
  * デフォルトエラーメッセージ: `"The Fabric Manager failed to disconnect a connection between the specified Host CPU and the target device."`

* `PowerOnFailureHWControlError`
  * OOBコントローラーが、指定されたデバイスの電源Onに失敗した場合に送出してください。
  * ベースクラス：`ControlObjectHWControlError`
  * 対象プラグイン: OOB
  * エラーコード: `"EF004BAS003"`
  * HTTPステータスコード: `500`
  * デフォルトエラーメッセージ: `"The Out-of-Band Controller failed to power on the specified device."`

* `PowerOffFailureHWControlError`
  * OOBコントローラーが、指定されたデバイスの電源Offに失敗した場合に送出してください。
  * ベースクラス：`ControlObjectHWControlError`
  * 対象プラグイン: OOB
  * エラーコード: `"EF004BAS004"`
  * HTTPステータスコード: `500`
  * デフォルトエラーメッセージ: `"The Out-of-Band Controller failed to power off the specified device."`

* `CPUResetFailureHWControlError`
  * OOBコントローラーが、指定されたHost CPUのリセットに失敗した場合に送出してください。
  * ベースクラス：`ControlObjectHWControlError`
  * 対象プラグイン: OOB
  * エラーコード: `"EF004BAS005"`
  * HTTPステータスコード: `500`
  * デフォルトエラーメッセージ: `"The Out-of-Band Controller failed to reset the specified Host CPU."`

* `InvalidDeviceTypeParameterHWControlError`
  * OOBプラグインで、指定されたデバイスタイプが不正な場合に送出してください。
  * ベースクラス：`ConfigurationHWControlError`
  * 対象プラグイン: OOB
  * エラーコード: `"EF007BAS016"`
  * HTTPステータスコード: `500`
  * デフォルトエラーメッセージ: `"The specified Device Type is invalid."`

## 7.3. 例外の追加

定義されているエラーの状況に当てはまらない場合や、上位に返却する情報を変更したい場合は、プラグインモジュール内に新たな例外を追加してください。  
プラグインが定義した例外クラスを拡張例外クラスと呼びます。

例外を追加するには、以下の情報を決定します。

* ベンダ依存拡張例外コード  
アルファベットの大文字3文字で構成されます。  
ベンダ依存拡張例外クラスコードは、各プラグインで他のプラグインと重ならない文字列を想定していますが、
現在公開されているプラグインはありませんので、"BAS"以外の任意のアルファベットの大文字3文字を決めてください。  
詳細は[9.2. 制限事項 ベンダ依存拡張例外クラスコード](09_Special_Notes.md#ベンダ依存拡張例外クラスコード)を参照ください。  

* 継承元の例外クラス  
[ベース例外クラス](#ベース例外クラス)、または、[定義済み例外](#72-定義済み例外)から近い例外を1つ選択します。  

* エラーレベル  
エラーの内容が致命的かどうか確認します。  

* リトライ可否  
時間をおいて同じ内容のリクエストを処理して、成功する可能性があるかどうか確認します。  

* HTTPステータスコード  
上位に返却するHTTPステータスコードを決めます。  
RFC9110のStatus Codeに準じます。  

* デフォルトエラーメッセージ  
上位に返却する英語のデフォルトエラーメッセージを決めます。  

* 例外クラス名  
クラス名は任意ですが、末尾に`HWControlError`を付けます。  

* 詳細例外クラスコード  
継承元のベース例外クラス内で一意に識別できる3桁の数字を決めます。  

次のような例外をクラスのを追加する例を示します。

|項目名|例|
|--|--|
|ベンダ依存拡張例外コード|"SPL"|
|継承元例外クラス|`BadRequestHWControlError`|
|エラーレベル|致命的ではない|
|リトライ可否|継続するエラーでリトライの意味はない|
|HTTPステータスコード|400|
|デフォルトエラーメッセージ|"Sample exception message."|
|例外クラス名|`SampleHWControlError`|
|詳細例外クラスコード|"001"|

```python
import app.common.basic_exceptions as exc


class SampleHWControlError(exc.BadRequestHWControlError):
    """Sample extended exception class

    sample docstring
    """
    # HTTPステータスコードを継承クラスから変更する場合、クラス変数 http_code を設定します。
    # 例では継承元と同じ値を使用するので設定は不要です。
    # http_code: int = http.HTTPStatus.BAD_REQUEST.value

    # エラーコードをクラス変数 error_code に設定します。
    # 例では エラーコードは "EF003SPL001" となります。
    #  - エラーレベル: 致命的ではない "E"
    #  - リトライ可否: リトライで成功する可能性がない "F"
    #  - ベース例外クラスコード: BadRequestHWControlError "003"
    #  - ベンダ依存拡張例外クラスコード: "SPL"
    #  - 詳細例外クラスコード: "001"
    error_code: str = "EF003SPL001"

    # デフォルトエラーメッセージをクラス変数 default_error_message に設定します。
    # 継承元と同じ値を使用する場合は設定は不要です。
    default_error_message: str = "Sample exception message."
```
