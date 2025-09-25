# 8. ログ出力

プラグインでは、Python標準の[ロガーオブジェクト](https://docs.python.org/3.12/library/logging.html#logger-objects)を通じてアプリケーションログを出力できます。ロガーオブジェクトは各モジュールで以下のように引数に`__name__`を指定して[`logging.getLogger`](https://docs.python.org/3.12/library/logging.html#logging.getLogger)を用いて取得してください。

```Python
import logging
logger = logging.getLogger(__name__)
```

アプリケーションログで使用するログレベルとそれぞれの方針は以下の表にしたがってください。

|レベル|方針|
|--|--|
|DEBUG|開発やデバッグのための情報|
|INFO|動作を把握するための情報|
|WARNING|リクエストされた処理は継続可能だが、注意が必要な情報|
|ERROR|リクエストされた処理を実行することが出来ないような場合|
|CRITICAL|hw-controlのサービスが継続できないような非常に重大なエラーが発生した場合|

HW制御機能にはいくつかのログメッセージが`app.common.messages.message`モジュールに定義されています。
出力したいメッセージが、既定のログメッセージに存在する場合、メッセージコードが使用できます。  
詳細は、[8.1. 既定のログメッセージ](#81-既定のログメッセージ)を参照ください。  

## 8.1. 既定のログメッセージ

プラグインからログ出力に使用できるメッセージが定義されています。  

|メッセージコード|ログメッセージ|備考|
|------|----------|----|
|"W00001"|W00001: Unexpected Exception: [(0)例外情報※1]|予期せぬ例外をハンドリング|
|"W00002"|W00002: Unexpected DeviceType: [(0)デバイスタイプ]|予期せぬデバイスタイプの指定|
|"W00006"|W00006: Device information not found: [(0)デバイスID、OOBデバイスID、デバイス種別など]|対象のデバイス情報が見つからない|
|"W00007"|W00007: File does not exist: [(0)ファイルパス]| ファイルが存在しない|
|"W00008"|W00008: Required item does not exist: [(0)項目名など]| 必須項目が存在しない|
|"W00009"|W00009: Invalid type value: [(0)項目名、値、想定データ型など] | データ型エラー|
|"W00010"|W00010: Power Operation Error: [(0)ResetType、ur]|対象のデバイス電源操作エラー|
|"W00011"|W00011: Not Power Operation Device: [(0)ResetType、ur]|電源操作が行えないデバイスの指定|
|"W00012"|W00012: Failed to get OOB Response: [(0)url]|OOBのからのレスポンスエラー|
|"E00001"|E00001: Unexpected Exception: [(0)例外情報※1]|情報取得で失敗した場合の予期せぬ例外をハンドリング|
|"E00002"|E00002: Unexpected DeviceType: [(0)デバイスタイプ]|予期せぬデバイスタイプの指定|
|"E00003"|E00003: Device information not found: [(0)デバイスID、OOBデバイスID、デバイス種別など]|対象のデバイス情報が見つからない|
|"E00004"|E00004: Power Operation Error: [(0)ResetType、url]|対象のデバイス電源操作エラー|
|"E00005"|E00005: Not Power Operation Device: [(0)ResetType、url]|電源操作が行えないデバイスの指定|
|"E00006"|E00006: Failed to get OOB Response: [(0)url]|OOBのからのレスポンスエラー|

※1 `traceback.format_exc()`など

また、ログ出力の整形用に以下の関数が定義されています。

```python
get_log_message(message_code: str, param_list: list) -> str:
```

この関数は以下の引数をとります。

- `message_code`
  - メッセージコードの文字列を指定します。
- `param_list`
  - メッセージコードの [(0)] の部分に出力する文字列をリスト形式で指定します。

この関数は、ログ出力用の文字列を返却します。  
引数に不備がある場合、以下の例外を送出します。  

- InvalidLogMessageParameterHWControlError

これらのメッセージは以下のように呼び出してログ出力することができます。  

```python
from app.common.messages import message
from app.common.utils.log import LOGGER

LOGGER.warning(message.get_log_message(message.W00006, ["device_id: xxx, device_type: xxx"]))
```

以下のように出力されます。

```text
yyyy/mm/dd HH:MM:SS.uuuuuu WARNING {"file":"---/plugins/xx/xxxx/xxxx_plugin.py","line":4,"message":"W00006: Device information not found: device_id: xxx, device_type: xxx"}
```
