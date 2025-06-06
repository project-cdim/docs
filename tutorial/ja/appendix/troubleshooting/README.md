### Troubleshooting <!-- omit in toc -->
ここでは、Composable Disaggregated Infrastructure Manager(略称:CDIM)のトラブルシューティングについて説明する。
- [1. CDIMのパスワードを忘れた/CDIMに入れなくなった場合](#1-cdimのパスワードを忘れたcdimに入れなくなった場合)
- [2. ダッシュボード画面にネットワークのエラーが表示されている場合](#2-ダッシュボード画面にネットワークのエラーが表示されている場合)
  - [401エラーと表示されている場合](#401エラーと表示されている場合)
  - [ネットワークエラーと表示されている場合](#ネットワークエラーと表示されている場合)
  - [500エラーと表示されている場合](#500エラーと表示されている場合)
  - [502エラーと表示されている場合](#502エラーと表示されている場合)
  - [kongの設定を初期化する](#kongの設定を初期化する)
- [3. CDIMのダッシュボードに接続できない/ダッシュボード画面が真っ白になる](#3-cdimのダッシュボードに接続できないダッシュボード画面が真っ白になる)
- [4. 特定のコンポーネントを再起動したい場合](#4-特定のコンポーネントを再起動したい場合)
- [5. 初期化したい場合](#5-初期化したい場合)

<!-- ユースケースの実装時に問題があった場合この項目に記載する -->
#### 1. CDIMのパスワードを忘れた/CDIMに入れなくなった場合
[Getting started](../../../../getting-started/ja/setup/setup.md#2-フロントエンド)の手順を参照ください。  
keycloakの管理URLからログインすることでCDIMの認証情報を確認・変更することが可能です。  
デフォルトのログイン情報は以下の通りです。
```
url : http://<ipアドレス>:8287
ユーザ : admin
パスワード : admin
```

#### 2. ダッシュボード画面にネットワークのエラーが表示されている場合

##### 401エラーと表示されている場合
認証の設定が適切にできていない可能性があります。
認証には、以下の3つでclientの名称が揃っている必要があります。
- keycloakのclient
- mf-coreの.env  NEXT_PUBLIC_AUTH_CLIENT_ID
- kongの設定 
kongの設定に関しては使用しているpublic_keyが適切かを
set-up-toolsディレクトリ内のpublic_key.pemの形式が間違っていないか、鍵の内容がcdimのpublic keyのものと同じか確認してください。  
間違いがある場合は修正した後、[kongの設定を初期化する](#kongの設定を初期化する)を実施したのちに、再度[set-up-toolsの設定](../../../../getting-started/ja/setup/setup.md#12-gateway-の初期設定)を行ってください。  

##### ネットワークエラーと表示されている場合
kongに接続できず404エラーと表示されている可能性があります。  
作成したdockerコンテナのネットワークにプロキシ設定やルーティング設定が入っていないかを確認してください。  
コンテナ内にプロキシ設定が入っていると動かなくなることがあります。    

##### 500エラーと表示されている場合  
kongと他コンポーネントが接続できなくなっている可能性があります。  
作成したdockerコンテナにプロキシ設定やルーティング設定が入っていないかを確認してください。  
コンテナ内にプロキシ設定が入っていると動かなくなることがあります。  

##### 502エラーと表示されている場合
以下のコマンドでkongの再起動を実施してください。
```
$ cd ~/cdim/base-compose
$ docker-compose down
$ docker-compose up -d --build
```

##### kongの設定を初期化する
以下のコマンドでkongの設定が入っているvolumeを削除し、作り直してください。

```
$ cd ~/cdim/base-compose
$ docker-compose down
$ docker volume ls
$ docker volume rm base-compose_gateway-db
$ docker-compose up -d --build
```
#### 3. CDIMのダッシュボードに接続できない/ダッシュボード画面が真っ白になる
mf-core/.envファイルを確認ください。  
IPアドレスやポート番号がコンテナの情報が一致しているかを確認する必要があります。  
```sh
コンテナ情報の確認方法
$ docker ps
IPアドレスの確認方法
$ ip address [| grep ens]
```

#### 4. 特定のコンポーネントを再起動したい場合
コンポーネント1つ1つを再起動する方法を示します。  
全てのコンポーネントを再起動する必要がある場合は、[初期化する](#5-初期化したい場合)の内容を参照してください。  
```sh
再起動したいコンポーネントのディレクトリに移動しコンテナを停止します
$ cd ~/cdim/base-compose
$ docker compose down
コンテナの停止が確認出来たらコンテナを再起動します
$ docker compose up -d --build
```

#### 5. 初期化したい場合
CDIMを初期化する方法を説明します。
下のコマンドにはdockerの全コンテナを停止、削除するコマンドを用いるため、注意して実行してください。  
```sh
全コンテナを停止・削除する
$ docker stop $( docker ps -q )
$ docker rm $( docker ps -aq )
全コンテナのイメージとボリュームを削除する
$ docker image rm $( docker image ls -q )
$ docker volume rm $( docker volume ls -q )
コンテナを立ち上げる
$ cd ~/cdim
$ ./install --up
```
