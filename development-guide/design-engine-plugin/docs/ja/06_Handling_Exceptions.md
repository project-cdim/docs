# 6. 例外処理

本章ではプラグインでの例外処理の実装方法について説明します。  
プラグインの実行中に発生したエラーは、```PluginProcessException```、または本例外クラスを継承したクラスにエラー情報を設定して返却する必要があります。  
エラー情報は、構成案設計機能を呼び出した上位のモジュールに返却するエラー情報として使用されます。  
構成案設計機能で用意されている例外クラスは```PluginProcessException```のみです。

## 6.1. 例外クラスの構造

構成案設計機能で使用する例外クラス```PluginProcessException```は構成案設計機能の```src.common.exceptions```パッケージに定義されています。

```python
class PluginProcessException(Exception):
```

この例外クラスはPython組み込みの```Exception```クラスを継承しています。  
本例外クラスは以下の```import```文から利用できます。

``` python
from common.exceptions import PluginProcessException
```

### 属性

- ```message: str```  
    - エラー時に構成案設計機能のHTTPレスポンスのbodyに用いるエラーメッセージ。
    - エラーメッセージにフォーマットの指定は特にありません。

- ```status_code: int```  
    - エラー時に構成案設計機能のHTTPレスポンスに用いるHTTPステータスコード。
    - デフォルト値は```500``` (```Internal Server Error```) です。

### メソッド

- ```__init__(self, message, status_code=HTTPStatus.INTERNAL_SERVER_ERROR.value)```  
    - 本例外クラスのコンストラクタ。
    - ```status_code```の初期値に使用している```HTTPStatus```はPython組み込みの```http```モジュールに定義されているクラスです。

### HTTPステータスコード

構成案設計へ返却するHTTPステータスコードは、プラグインの要件に応じて`4XX`または`5XX`を設定してください。  
以下はHTTPステータスの例とその方針です。これらは参考例であり、必要に応じて自由に選択・拡張してください。

| HTTPステータスコード | 概要 |  方針 |
| --- | --- | --- |
| 400 | Bad Request | 入力情報に不正がある場合 |
| 404 | Not Found | 指定された設計IDが存在しない場合 |
| 409 | Conflict | 構成案設計キャンセル要求に対して設計状態遷移不可の場合 |
| 500 | Internal Server Error | プラグインまたは設計機構の処理でエラーになった場合<br>他コンポーネントでエラーが発生した場合 |

## 6.2. 例外の追加

プラグインを実装する際に定義されている```PluginProcessException```以外の例外クラスが必要な場合は、プラグインモジュール内に新たな例外クラスを追加してください。  
例外クラスを追加する際は```PluginProcessException```を継承してください。