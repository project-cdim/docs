# 環境を準備する

## 1. 前提条件

前提条件を記載します。

- Operating System をインストールしていること。

## 2. Git をインストールする

Git をインストールします。

```sh
sudo dnf install git
```

`git` コマンドが実行できることを確認します。
下記のコマンドで Git のバージョンが表示されることを確認してください。

```sh
git version
```

## 3. Docker をインストールする。

Docker のドキュメントを参照して Docker Engine をインストールします。

- https://docs.docker.com/engine/install/

インストール作業に使用するユーザに `docker` コマンドを実行権限を付与するため、
ユーザを docker グループに追加します。

現在のユーザがインストール作業に使用するユーザの場合は下記のコマンドを実行します。

```sh
sudo gpasswd -a $USER docker
```

docker グループに指定したユーザが追加されていることを確認します。
下記のコマンドで指定したユーザ名が表示されることを確認してください。

```sh
getent group docker
```

## 4. Docker ネットワークを作成する

CDIM とエミュレーターが利用する Docker ネットワークを作成します。

```sh
docker network create cdim-net
```

Docker ネットワークが作成されるいることを確認します。
下記コマンドで cdim-net が表示されることを確認してください。

```sh
docker network ls
```
