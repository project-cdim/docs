# CDIM をインストールする

## 1. Prerequisites

- Docker
- Git

## 2. インストーラーを取得する

インストーラーを取得します。

```sh
git clone https://github.com/project-cdim/installer.git
```

`pre_install` スクリプトを実行して各コンポーネントを取得します。

```sh
cd installer
./pre_install
```

各コンポーネントのリポジトリが clone されていることを確認します。

## 3. 設定ファイルを修正する

### 3.1. フロントエンド

#### 3.1.1. 設定ファイルの作成

mf-core コンポーネントに移動します。

```sh
cd mf-core
```

サンプルファイル `.env.sample` を元に設定ファイル `.env` を作成します。

```sh
cp .env.example .env
```

#### 3.1.2. 設定ファイルの修正

`.env` ファイルを自身の環境に合わせて修正します。
通常は `cdim-server` を Docker がインストールされているサーバーのホスト名または IP アドレスに変更します。

以下は変更箇所の抜粋です。

```sh: .env
# Micro frontend URL settings
NEXT_PUBLIC_URL_CORE      = 'http://cdim-server:3000'
NEXT_PUBLIC_URL_RESOURCE  = 'http://cdim-server:3003'
NEXT_PUBLIC_URL_LAYOUT    = 'http://cdim-server:3004'
NEXT_PUBLIC_URL_USER      = 'http://cdim-server:3005'

# URL of the authentication server
NEXT_PUBLIC_URL_IDP        = 'http://cdim-server:8287'

# API endpoint of the configuration design backend
NEXT_PUBLIC_URL_BE_LAYOUT_DESIGN = 'http://cdim-server:8014/cdim/api/v1/layout-design'
# API endpoint of the configuration apply backend
NEXT_PUBLIC_URL_BE_LAYOUT_APPLY = 'http://cdim-server:8014/cdim/api/v1/layout-apply'
# API endpoint of the constraint management backend
NEXT_PUBLIC_URL_BE_POLICY_MANAGER = 'http://cdim-server:8014/cdim/api/v1/policy-manager'
# API endpoint of the configuration information management backend
NEXT_PUBLIC_URL_BE_CONFIGURATION_MANAGER = 'http://cdim-server:8014/cdim/api/v1/configuration-manager'
# API endpoint of the performance information management backend (VictoriaMetrics)
NEXT_PUBLIC_URL_BE_PERFORMANCE_MANAGER = 'http://cdim-server:8014/cdim/api/v1/performance-manager'
```

### 3.2. 構成情報

変更が不要な場合は以下の修正は不要です。

下記のファイルを修正することで HW の情報取得の収集間隔を環境に合わせて変更できます。

```sh
configuration-collector-compose/configuration-collector/configuration-collector/config/collect.yaml
```

hw_collect_configs の「interval」、「timeout」を修正します。
以下は 120 秒に修正した例です。

```sh
global:
  max_jobs: 200
  job_interval: 600
  job_timeout: 600
hw_collect_configs:
  - job_name: 'Hardware-Sync'
    interval: 120
    timeout: 120
    collect:
      url: 'http://configuration-exporter:8080/cdim/api/v1/devices'
    forwarding:
      url: 'http://configuration-manager:8080/cdim/api/v1/devices'
```

## 4. コンテナを起動する

`install` スクリプトを実行してビルドとコンテナの起動を行います。

```sh
./install --up
```

[Next step: CDIM の初期設定を行う](../setup/setup.md)
