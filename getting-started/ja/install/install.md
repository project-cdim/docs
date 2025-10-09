# CDIM をインストールする

## 1. 前提条件

- Docker
- Git

### 1.1. Dockerのproxy設定について

> [!WARNING]
> 以下のDocker公式で紹介されている``~/.docker/config.json`` ファイルを作成・編集する方法は使用しないでください。  
> https://docs.docker.jp/network/proxy.html#id2  
> 上記方法によるproxy設定はビルド時およびすべての起動したコンテナに反映されるため、Dapr side carの通信ができなくなります。

#### 1.1.1. docker image pull時のproxy設定  

以下のDocker公式で紹介されている ``~/.config/systemd/user/docker.service.d/`` で設定する方法を推奨します。  
https://docs.docker.jp/config/daemon/systemd.html#id6

#### 1.1.2. docker image build時のproxy設定  

compose.override.ymlによる設定を推奨します。  
対象は以下です。

| composeレシピ                         | dockerサービス                |
| ------------------------------------- | ----------------------------- |
| base-compose                          | message-broker-setting        |
| configuration-exporter-compose        | configuration-exporter        |
| configuration-manager-compose         | configuration-manager         |
| hw-control-compose                    | hw-control                    |
| job-manager-compose                   | job-manager-setup             |
| layout-apply-compose                  | layout-apply                  |
| migration-procedure-generator-compose | migration-procedure-generator |
| performance-collector-compose         | performance-collector         |
| performance-exporter-compose          | performance-exporter          |
| set-up-tools                          | gateway-set-up-tools          |

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

サンプルファイル `.env.example` を元に設定ファイル `.env` を作成します。

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

Docker がインストールされているサーバーの FQDN に置換する場合は下記のコマンドで変更できます。

```sh
sed -e "/^NEXT_PUBLIC/s/localhost/$(hostname -f)/g" .env.example > .env
```

リポジトリのルートディレクトリに戻ります。

```sh
cd ..
```

### 3.2. ジョブ管理

変更が不要な場合は以下の修正は不要です。

下記のファイルを修正することでHWの情報取得の収集間隔を環境に合わせて変更できます。

```sh
job-manager-compose/job-manager-setup/HW_configuration_information_data_linkage_job.yaml
```

scheduleの「time」を修正します。
以下は5分に修正した例です。

```sh
- defaultTab: nodes
  description: ''
  executionEnabled: true
  id: 9d6fd442-71e3-412d-be58-17487269787a
  loglevel: INFO
  name: HW configuration information data linkage job
  nodeFilterEditable: false
  plugins:
    ExecutionLifecycle: null
  schedule:
    dayofmonth:
      day: '*'
    month: '*'
    time:
      hour: '*'
      minute: '0/5'
      seconds: '0'
    year: '*'
```

## 4. コンテナを起動する

`install` スクリプトを実行してビルドとコンテナの起動を行います。

```sh
./install --up
```

[Next step: CDIM の初期設定を行う](../setup/setup.md)
