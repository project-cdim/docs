# 5. プラグインの実装

本章ではプラグインの仕様をプロパティ、メソッドごとに説明します。

---

## 5.1. プロパティ

### 5.1.1. `design_engine`

``` python
design_engine: str
```

構成案設計のREST API実行時に指定するプラグイン名を保持するプロパティです。

### 5.1.2. `request_params`

``` python
request_params: list[int]
```

プラグインに対応する設計機構で構成案設計要求に必要な[入力情報](a01_Args_to_request_design_Function.md)を示すプロパティです。  
Pythonの[Enum](https://docs.python.org/ja/3/library/enum.html)を使用して、必要となる情報をlist型で定義します。  
定義情報については構成案設計の`layout-design-compose/layout-design/layout-design/src/common/request_params_enum.py`の`RequestParams`クラスに定義されています。  
本プロパティで指定されていない入力情報はプラグインへ渡されません。

```RequestParams```クラスは以下の```import```文から利用できます。

``` python
from common.request_params_enum import RequestParams
```

---

## 5.2. メソッド

### 5.2.1. `request_design`

``` python
request_design(args: dict) -> str
```

プラグインに対応する設計機構に対して、引数で渡された入力情報を渡して設計処理を開始します。  
戻り値として設計IDを文字列で返却します。設計IDの生成はプラグイン、設計機構のどちらで行っても問題ありません。

#### 引数

- `args`  
  設計機構へ渡す入力情報の辞書です。詳細は[付録1. request_design関数へ渡される引数](a01_Args_to_request_design_Function.md)を参照してください。

#### 戻り値

構成案設計要求を識別する設計ID(`designID`)を文字列型で返却します。

プラグイン/設計機構でエラーが発生した場合は、`PluginProcessException`クラス、またはこれを継承した独自の例外クラスを送出します。([6. 例外処理](06_Handling_Exceptions.md))

#### 動作確認手順

以下の手順で[2.1. 構成案設計機能のREST API](02_LayoutDesignFunctions.md#21-構成案設計機能のrest-api)を実行します。

1. 構成案設計要求に渡す[入力情報のサンプル](samples/data/post_request_data.json)を用意します。

2. 1で用意した入力情報をリクエストボディに指定して構成案設計要求を実行します。  
  実行例:
  ``` shell
  curl -X POST -H "Content-Type: application/json" "localhost:8011/cdim/api/v1/layout-designs?designEngine=<design_engine>" -d @post_request_data.json
  ```
  - ```<design_engine>```には[5.1.1. design_engine](05_Implementing_plugin.md#511-design_engine)で作成したプラグイン名を指定します。

3. 構成案設計要求のレスポンスとして以下のJSON形式で設計ID(`designID`)が返却されることを確認します。  
  レスポンス例:
  ``` json
  {"designID": "ca71c4bb-7ba8-41ea-9707-35f46b675857"}
  ```

REST APIで返却される`designID`はプラグインまたは設計機構で生成された一意な文字列になります。  
この`designID`を指定して構成案設計結果取得を実行することで設計結果を確認します。

### 5.2.2. `get_design`

``` python
get_design(design_id: str) -> dict
```

指定された設計IDに紐づく構成案設計結果をプラグインに対応する設計機構から取得します。  
戻り値として設計機構から取得した構成案設計結果を辞書型で返却します。

#### 引数

- `design_id`  
  構成案設計要求実行時に返却された設計IDの文字列です。

#### 戻り値

指定された設計IDの構成案設計結果を辞書型で返却します。詳細は[付録2. get_design関数から返却される戻り値](a02_Return_Value_from_get_design.md)を参照してください。

プラグイン/設計機構でエラーが発生した場合は、`PluginProcessException`クラス、またはこれを継承した独自の例外クラスを送出します。([6. 例外処理](06_Handling_Exceptions.md))

#### 動作確認手順

以下の手順で[2.1. 構成案設計機能のREST API](02_LayoutDesignFunctions.md#21-構成案設計機能のrest-api)を実行します。

1. 取得したい構成案設計結果の設計IDをパスパラメータに含めて構成案設計結果取得を実行します。  
  実行例:
  ``` shell
  curl -X GET "localhost:8011/cdim/api/v1/layout-designs/<designID>?designEngine=<design_engine>"
  ```
  - ```<design_engine>```には[5.1.1. design_engine](05_Implementing_plugin.md#511-design_engine)で作成したプラグイン名を指定します。

2. 構成案設計結果取得のレスポンスとして以下のJSON形式で設計結果が返却されることを確認します。  
  レスポンス例:
  ``` json
  {
    "status": "COMPLETED",
    "requestID": "17d9a80f-1a32-4f5a-9c50-b1c64c259f15",
    "startedAt": "2025-05-10T00:00:00Z",
    "endedAt": "2025-05-10T00:00:00Z",
    "design": {...},
    "conditions": {},
    "procedures": [...]
  }
  ```

### 5.2.3. `get_all_design`

``` python
get_all_design(fields: list[str], limit: int, offset: int, sort_by: str, order_by: str, status: list[str]) -> dict
```

引数で渡された条件を満たす構成案設計結果の一覧をプラグインに対応する設計機構から取得します。  
戻り値として設計機構から取得した構成案設計結果の一覧を辞書型で返却します。

#### 引数

- `fields`  
  設計結果として取得したい情報を示すパラメータです。  
  指定される値は`design`(構成案)、`conditions`(移行条件)、`procedures`(移行手順)の3つで、複数指定可です。
- `limit`  
  取得する設計結果の件数を示すパラメータです。  
  デフォルト値: 100
- `offset`  
  設計結果の取得開始位置を示すパラメータです。  
  デフォルト値: 0
- `sort_by`  
  設計結果のうちソート対象を示すパラメータです。  
  指定される値は`startedAt`(設計開始時刻)、`endedAt`(設計終了時刻)の2つで、複数指定不可です。  
  デフォルト値: startedAt
- `order_by`  
  取得する設計結果の順序を示すパラメータです。  
  指定される値は`desc`(降順)、`asc`(昇順)の2つで、複数指定不可です。  
  デフォルト値: desc
- `status`  
  取得する設計結果の設計状態を示すパラメータです。  
  指定される値は`IN_PROGRESS`(設計実行中)、`COMPLETED`(設計完了)、`FAILED`(設計失敗)、`CANCELING`(設計処理キャンセル中)、`CANCELED`(設計処理キャンセル完了)の5つで、複数指定可です。

#### 戻り値

引数で指定された条件を満たす設計結果の一覧、取得件数、引数の条件を満たす設計結果の数を辞書型で返却します。

プラグイン/設計機構でエラーが発生した場合は、`PluginProcessException`クラス、またはこれを継承した独自の例外クラスを送出します。([6. 例外処理](06_Handling_Exceptions.md))

#### 動作確認手順

以下の手順で[2.1. 構成案設計機能のREST API](02_LayoutDesignFunctions.md#21-構成案設計機能のrest-api)を実行します。

1. 取得したい構成案設計結果の条件をクエリパラメータに含めて設計結果一覧取得を実行します。  
  実行例:
  ``` shell
  curl -X GET "localhost:8011/cdim/api/v1/layout-designs?designEngine=<design_engine>"
  ```
  - ```<design_engine>```には[5.1.1. design_engine](05_Implementing_plugin.md#511-design_engine)で作成したプラグイン名を指定します。

2. 設計結果一覧取得のレスポンスとして以下のJSON形式で設計結果の一覧が返却されることを確認します。  
  レスポンス例:
  ``` json
  {
    "count": 100,         # 取得件数
    "totalCount": 200,    # 引数の条件を満たす設計結果の数
    "designs": [          # 設計結果一覧のリスト
      {
        "status": "COMPLETED",
        "requestID": "17d9a80f-1a32-4f5a-9c50-b1c64c259f15",
        "startedAt": "2025-05-10T00:00:00Z",
        "endedAt": "2025-05-10T00:00:00Z",
        "design": {...},
        "conditions": {},
        "procedures": [...],
        "id": "ca71c4bb-7ba8-41ea-9707-35f46b675857"
      },
      ...
    ]
  }
  ```

以下はクエリパラメータにより取得する設計結果をフィルタリングする場合の実行例です。  
``` shell
curl -X GET "localhost:8011/cdim/api/v1/layout-designs?designEngine=<design_engine>&status=COMPLETED&limit=10&orderBy=asc"
```

上記の実行例では設計状態がCOMPLETEDのものを古い順で10件取得します。

### 5.2.4. `cancel_design`

```python
cancel_design(design_id: str) -> str
```

プラグインに対応する設計機能に対して、引数で指定された設計IDに紐づく構成案設計要求の処理のキャンセル要求を送出します。  
戻り値としてキャンセルを行った結果の設計状態を返却します。

#### 引数

- `design_id`  
  構成案設計要求実行時に返却された設計IDの文字列です。

#### 戻り値

引数で指定された設計IDに対してキャンセル処理を行った結果の設計状態を文字列型で返却します。  
本メソッド実行時の設計状態の遷移と構成案設計機能から返却されるHTTPステータスを下表にまとめます。

| 実行時の設計状態 | 遷移後の設計状態 | HTTPステータスコード | 概要 |
| --- | --- | --- | --- |
| IN_PROGRESS | CANCELING | 202 | Accepted |
| COMPLETED | 設計状態遷移不可 | 409 | Conflict |
| FAILED | 設計状態遷移不可 | 409 | Conflict |
| CANCELING | CANCELING | 202 | Accepted |
| CANCELED | CANCELED | 200 | OK |

実行時の設計状態がCOMPLETEDまたはFAILEDの場合は、構成案の設計処理が正常または異常問わず終了しているため、キャンセル要求を受けても設計状態遷移不可としてHTTPステータス409 Conflictを返却します。

プラグイン/設計機構でエラーが発生した場合は、`PluginProcessException`クラス、またはこれを継承した独自の例外クラスを送出します。([6. 例外処理](06_Handling_Exceptions.md))

#### 動作確認手順

以下の手順で[2.1. 構成案設計機能のREST API](02_LayoutDesignFunctions.md#21-構成案設計機能のrest-api)を実行します。

1. 設計処理をキャンセルしたい構成案設計要求の設計IDをパスパラメータに含めて構成案設計キャンセルを実行します。  
  実行例:
  ``` shell
  curl -X PUT "localhost:8011/cdim/api/v1/layout-designs/<designID>?action=cancel&designEngine=<design_engine>"
  ```
  - ```<design_engine>```には[5.1.1. design_engine](05_Implementing_plugin.md#511-design_engine)で作成したプラグイン名を指定します。

2. 構成案設計キャンセルのレスポンスとして遷移後の設計状態が返却されることを確認します。  
  レスポンス例:
  ``` json
  {"status": "CANCELING"}
  ```

### 5.2.5. `delete_design`

``` python
delete_design(design_id: str)
```

プラグインに対応する設計機構に対して、指定された設計IDの設計結果の削除要求を行います。

#### 引数

- `design_id`  
  構成案設計要求実行時に返却された設計IDの文字列です。

#### 戻り値

なし。

プラグイン/設計機構でエラーが発生した場合は、`PluginProcessException`クラス、またはこれを継承した独自の例外クラスを送出します。([6. 例外処理](06_Handling_Exceptions.md))

#### 動作確認手順

以下の手順で[2.1. 構成案設計機能のREST API](02_LayoutDesignFunctions.md#21-構成案設計機能のrest-api)を実行します。

1. 削除したい構成案設計結果の設計IDをパスパラメータに含めて構成案設計結果削除を実行します。  
  実行例:
  ``` shell
  curl -X DELETE "localhost:8011/cdim/api/v1/layout-designs/<designID>?designEngine=<design_engine>"
  ```
  - ```<design_engine>```には[5.1.1. design_engine](05_Implementing_plugin.md#511-design_engine)で作成したプラグイン名を指定します。

2. 構成案設計結果削除のレスポンスとしてHTTPステータス204 NO CONTENTが返却されることを確認します。

3. 構成案設計結果を削除した設計IDをパスパラメータに指定して構成案設計結果取得を実行し、HTTPステータス404 NOT FOUNDが返却されることを確認します。