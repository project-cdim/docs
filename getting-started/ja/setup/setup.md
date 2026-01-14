# CDIM の初期設定を行う

> [!NOTE]
> `cdim-server` は[CDIM をインストールする](../install/install.md)の設定ファイルで使用したものと同じ値を使用します。

> [!NOTE]
> 本章の手順におけるカレントディレクトリは [CDIM をインストールする](../install/install.md) で clone したインストーラーの installer となります。

## 1. gateway (Kong)

### 1.1. Public key の確認

Keycloakにおける Public Key の確認方法は以下のとおりです。

Keycloak にログインします。
初期状態では、ユーザ名: admin, パスワード: admin でログイン可能です。

```sh
http://cdim-server:8287/
```

1. Realm を「CDIM」に切り替えます。
2. 「Realm settings」をクリックします。
3. 「Keys」タブをクリックします。
4. 「RS256」の「Public key」をクリックします。

![fig 1-1 realm settings keys](img/public_key_01.png)

Public Key が表示されるので、内容をコピーしておきます。

![fig 1-1 realm settings keys](img/public_key_02.png)

### 1.2. gateway の初期設定

コピーした Public key を使用して、`set-up-tools/gateway/tools/` ディレクトリ配下に `public_key.pem` ファイルを作成します。
形式は以下のとおりです。

```txt:public_key.pem
-----BEGIN PUBLIC KEY-----
(ここにコピーした Public key を貼り付けます)
-----END PUBLIC KEY-----
```

ファイルの作成例を記載します。

```txt:public_key.pem
-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8A (中略) 79FWBtfKyuQTmnN2mp78N+gwp1LywIDAQAB
-----END PUBLIC KEY-----
```

`post_install` スクリプトを実行して初期設定を行います。

```sh
./post_install
```

基盤のgatewayコンテナを再起動します。

```sh
cd base-compose
docker compose down gateway-dapr
docker compose down gateway
docker compose up -d --build
```

## 2. フロントエンド

### 2.1. client 作成

Keycloak にログインします。
初期状態では、ユーザ名: admin, パスワード: admin でログイン可能です。

```sh
http://cdim-server:8287/
```

Realmを「CDIM」に切り替えます。

「Clients」をクリックし、「Create client」をクリックします。
![fig 2-1 Clients Create client](img/add_client1.png)

「General settings」で以下のように設定を行い「Next」をクリックします。

| 項目 | 値 |
|---|---|
| Client type | OpenID Connect|
| Client ID | cdim-client |
| Name | (空欄のまま) |
| Description | (空欄のまま) |
| Always display in UI | Off |

![fig 2-2 Clients Create client](img/add_client2.png)

「Capability config」で「Authentication flow」の「Standard flow」だけ選択した状態にして「Next」をクリックします。

![fig 2-3 Clients Create client](img/add_client3.png)

「Login settings」で以下のように指定します。

| 項目 | 値 |
|------|------|
|Root URL| <http://cdim-server:3000/>  |
|Home URL| <http://cdim-server:3000/>  |
|Valid redirect URIs| <http://cdim-server:3000/*> |
|Valid post logout redirect URIs| <http://cdim-server:3000/*> |
|Web origins| * |

![fig 2-4 Clients Create client](img/add_client4.png)

「Save」をクリックして設定を保存します。

### 2.2. User 作成

CDIM のユーザーを作成します。
ここでは管理者ユーザーの作成を例に説明します。

#### 2.2.1. User の追加

「Users」をクリックし、「Add User」をクリックします。
![fig 2-1 Users Add user](img/add_user1.png)

「Username」を入力し、「Create」ボタンをクリックします。
![fig 2-2 Users Add user](img/add_user2.png)

#### 2.2.2. User にパスワードを設定する

「Credentials」タブをクリックし、表示された画面で「Set password」ボタンをクリックします。
![fig 2-3 Users Add user](img/add_user3.png)

Password を入力します。Temporary は「Off」にします。「Save」ボタンをクリックします。
![fig 2-4 Users Add user](img/add_user4.png)

「Save password」ボタンをクリックします。
![fig 2-5 Users Add user](img/add_user5.png)

#### 2.2.3. User にロールを付与する

「Role mapping」タブをクリックし、「Assign role」ボタンをクリックします。
![fig 2-6 Users Add user](img/add_user6.png)

フィルターの条件を「Filter by realm roles」に切り替えます。
![fig 2-7 Users Add user](img/add_user7.png)

一覧の中で付与するロールにチェックを付けます。
ここでは管理者権限を表す「cdim-administrator」にチェックを付けます。
「Assign」ボタンをクリックします。
![fig 2-8 Users Add user](img/add_user8.png)

## 3. 動作確認

作成したユーザーで CDIM にログインします。

```sh
http://cdim-server:3000/
```

以下のようにダッシュボード画面にエミュレーターから取得したリソース情報が表示されていれば正常に動作しています。

![fig 3-1 CDIM Dashboard](img/cdim_dashboard.png)

[Next step: CDIM を使用する](../use/use.md)
