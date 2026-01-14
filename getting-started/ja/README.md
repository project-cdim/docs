# Getting Started

このガイドではComposable Disaggregated Infrastructure Manager (以降、CDIM) をインストール、初期化、動作確認を行い、使用を開始するための一連の手順を説明します。
CDIMの概要を知りたい場合は[コンセプト](../../concepts/ja/README.md)から始めることをお勧めします。

> [!WARNING]
> 本ガイドで提供される構築手順には固定値で設定された認証情報が含まれています。このため、実際の運用環境で利用することは推奨されません。認証情報を変更する手順は今後公開する予定です。

## 導入ステップ

1. [環境を準備する](prepare/prepare.md)  
CDIMの構築に必要な環境を準備します。
2. [エミュレーターをインストールする](emulator/emulator.md)  
CDIMと連携する環境をエミュレーターを使用して構築します。
3. [CDIMをインストールする](install/install.md)  
インストーラーを使用してCDIMをインストールします。
4. [CDIMの初期設定を行う](setup/setup.md)  
CDIMを動作させる環境に合わせて初期設定します。
5. [CDIMを使用する](use/use.md)   
CDIMの機能を使用して動作を確認します。

## 動作要件

本ガイドの推奨要件は以下の表に記載のとおりです。

### ハードウェア

| 要件     | 推奨値        |
| -------- | ------------- |
| CPU      | x64 4コア以上 |
| メモリ   | 8GB以上       |
| ディスク | 64GB以上      |

### ソフトウェア

| 項目                 | ソフトウェア            |
| -------------------- | ----------------------- |
| OS                   | Alma Linux 9            |
| コンテナ管理ツール   | Docker / Docker Compose |
| バージョン管理ツール | git                     |

## ポートとプロトコル

CDIM が使用するポート番号とプロトコルを記載します。

| プロトコル | 方向 | ポート範囲 | 目的 |
| --- | --- | --- | --- |
| TCP | Inbound | 3000,3003-3005 | フロントエンド |
| TCP | Inbound | 3500,3503-3505,3507-3509,3512-3515,3517,50006 | DAPR 通信 |
| TCP | Inbound | 5000 | リファレンスハードウェアエミュレータ |
| TCP | Inbound | 8000 | ハードウェア制御 |
| TCP | Inbound | 8012 | 移行手順生成 |
| TCP | Inbound | 8013 | 構成案反映 |
| TCP | Inbound | 8014 | Gateway(Kong) |
| TCP | Inbound | 8280 | 構成情報管理 |
| TCP | Inbound | 8283 | 構成情報エクスポーター |
| TCP | Inbound | 8284 | 性能情報収集 |
| TCP | Inbound | 8285 | 性能情報エクスポーター |
| TCP | Inbound | 8286 | アラート管理(Alerta) |
| TCP | Inbound | 8287 | IAM(Keycloak) |
| TCP | Inbound | 8288 | ジョブ管理(Rundeck) |
| TCP | Inbound | 8289 | メッセージブローカー(NATS) |
| TCP | Inbound | 8428 | 性能情報管理(VictriaMetrics) |
| TCP | Inbound | 9090 | 性能情報収集(Prometheus) |
| TCP | Inbound | 9094 | アラート管理(AlertManager) |

## 環境概要

構築される環境の全体構成については、下図をご参照ください。

![CDIMの構成図](img/component_diagram.png)

## 学習をさらに進めたい方へ

### [CDIMチュートリアル](../../tutorial/ja/README.md)

チュートリアルに記載された詳細な例とシナリオを通じて、CDIMに関する理解とスキルを向上させましょう。このリソースは、新規ユーザーおよび既存ユーザーの両方がCDIMを習得するのに最適です。

これらの手順に従うことで、CDIMを効果的に使用してインフラストラクチャを展開、管理、最適化する準備が整います。