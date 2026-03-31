# 2. 構成案設計機能概要

本章では、構成案設計機能のREST APIを概説したのち、プラグインが実装する機能を示します。

## 2.1. 構成案設計機能のREST API

構成案設計機能のREST APIでプラグインに関わるものを以下に示します。

| No. | 名称 | URI | HTTPメソッド | 概要 |
| --- | --- | --- | --- | --- |
| 1 | 構成案設計要求 | /cdim/api/v1/layout-designs | POST | サービスの定義情報、リソース要求を受け付け、設計処理を開始して設計IDを返却します。 |
| 2 | 構成案設計結果取得 | /cdim/api/v1/layout-designs/{designID} | GET | 指定された設計IDの設計結果を返却します。 |
| 3 | 設計結果一覧取得 | /cdim/api/v1/layout-designs | GET | 設計結果の一覧を返却します。 |
| 4 | 構成案設計キャンセル | /cdim/api/v1/layout-designs/{designID}?action=cancel | PUT | 指定された設計IDの設計処理をキャンセルします。 |
| 5 | 構成案設計結果削除 | /cdim/api/v1/layout-designs/{designID} | DELETE | 指定された設計IDの設計結果を削除します。 |

## 2.2. プラグインの概要

プラグインはクラスとして実装します([4.2. クラス構成](04_Configuration.md#42-クラス構成)参照)。  
構成案設計機能のREST APIは、各種要求に対して指定された設計機構に依存する処理をプラグインへ委譲し、プラグインから設計機構の機能を呼び出します。

以下にプラグインが実装するメソッドを示します。

### プラグインのメソッド

| No. | 名称 | メソッド | 概要 |
| --- | --- | --- | --- |
| 1 | 構成案設計要求 | request_design | サービスの定義情報、リソース要求、リソース性能情報、ノード構成情報を受け付け、設計処理を開始して設計IDを返却します。 |
| 2 | 構成案設計結果取得 | get_design | 指定された設計IDの設計結果を返却します。 |
| 3 | 設計結果一覧取得 | get_all_design | 設計結果の一覧を返却します。 |
| 4 | 構成案設計キャンセル | cancel_design | 指定された設計IDの設計処理をキャンセルします。 |
| 5 | 構成案設計結果削除 | delete_design | 指定された設計IDの設計結果を削除します。 |

### 構成案設計要求への入力情報の概要

構成案設計要求でプラグインに入力される情報の概要を下表にまとめます。  
入力情報の詳細は[付録1. request_design関数へ渡される引数](a01_Args_to_request_design_Function.md)を参照してください。

| No. | データ | パラメータ名 | データ型 | 概要 |
| --- | --- | --- | --- | --- |
| 1 | [要求ID](a01_Args_to_request_design_Function.md#要求id-requestid) | requestID | str | 構成案設計機能の呼び出し元で管理する構成案設計要求を識別するためのID。 |
| 2 | [再設計対象ノード一覧](a01_Args_to_request_design_Function.md#再設計対象ノード一覧-targetnodeids) | targetNodeIDs | list[str] | 全ノード一覧のうち設計対象となるノードのノードIDの一覧。 |
| 3 | [サービスセット要求リソース](a01_Args_to_request_design_Function.md#サービスセット要求リソース-servicesetrequestresources) | serviceSetRequestResources | dict | サービスが要求するリソース種別と性能情報。 |
| 4 | [設計対象サービス一覧](a01_Args_to_request_design_Function.md#設計対象サービス一覧-services) | services | dict | サービスの定義情報。 |
| 5 | [全リソース一覧](a01_Args_to_request_design_Function.md#全リソース一覧-resources) | resources | list[dict] | 構成案設計で構成情報管理機能から取得される全リソースの性能情報。 |
| 6 | [全ノード一覧](a01_Args_to_request_design_Function.md#全ノード一覧-nodes) | nodes | list[dict] | 構成案設計で構成情報管理機能から取得される実行時点での全ノードの構成情報。 |
| 7 | [全ノード対象フラグ](a01_Args_to_request_design_Function.md#全ノード対象フラグ-designallnodes) | designAllNodes | bool | 全ノード一覧で渡された全ノードを設計対象とするフラグ。 |
| 8 | [部分設計フラグ](a01_Args_to_request_design_Function.md#部分設計フラグ-partialdesign) | partialDesign | bool | 指定されたサービス/ノードのみが設計対象となる部分設計か、すべてのサービス/ノードが設計対象となる全体設計かを示すフラグ。 |
| 9 | [移行条件スキップフラグ](a01_Args_to_request_design_Function.md#移行条件スキップフラグ-nocondition) | noCondition | bool | 構成案の設計結果として移行条件が不要であることを示すフラグ。 |
| 10 | [制約条件一覧](a01_Args_to_request_design_Function.md#制約条件一覧-policies) | policies | dict | 構成案設計で制約条件管理機能から取得されるリソース選定に関する制約事項の一覧。 |

### 構成案設計結果取得の出力結果の概要

構成案設計結果として返却する情報の概要を下表にまとめます。  
構成案、移行条件、移行手順に関する詳細は[付録2. get_design関数から返却される戻り値](a02_Return_Value_from_get_design.md)を参照してください。

| No. | データ | パラメータ名 | データ型 | 概要 |
| --- | --- | --- | --- | --- |
| 1 | [設計状態](a02_Return_Value_from_get_design.md#設計状態-status) | status | str | 構成案の設計状態を示す文字列(IN_PROGRESS: 設計実行中、COMPLETED: 設計完了、FAILED: 設計失敗、CANCELING: 設計処理キャンセル中、CANCELED: 設計処理キャンセル完了)。 |
| 2 | [要求ID](a02_Return_Value_from_get_design.md#要求id-requestid) | requestID | str | 構成案設計機能の呼び出し元で管理する構成案設計要求を識別するためのID。入力情報の要求IDをそのまま返却する。 |
| 3 | [設計開始時刻](a02_Return_Value_from_get_design.md#設計開始時刻-startedat) | startedAt | str | プラグイン/設計機構で設計処理を開始した時刻。 |
| 4 | [設計終了時刻](a02_Return_Value_from_get_design.md#設計終了時刻-endedat) | endedAt | str | プラグイン/設計機構で設計処理が終了した時刻。 |
| 5 | [構成案](a02_Return_Value_from_get_design.md#構成案-design) | design | dict | 入力情報をもとに作成されたノードの構成案。 |
| 6 | [移行条件](a02_Return_Value_from_get_design.md#移行条件-conditions) | conditions | dict | 入力された現ノード構成から作成された構成案へ移行する際に許容されるノード負荷の条件。 |
| 7 | [移行手順](a02_Return_Value_from_get_design.md#移行手順-procedures) | procedures | list[dict] | 入力された現ノード構成から作成された構成案へ移行するための手順。 |
| 8 | [設計失敗理由](a02_Return_Value_from_get_design.md#設計失敗理由-cause) | cause | str | 構成案の設計に失敗した(設計状態がFAILED)場合の失敗理由。 |