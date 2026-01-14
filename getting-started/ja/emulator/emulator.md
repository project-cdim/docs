# エミュレーターをインストールする

## 1. エミュレーターを構築する

エミュレーターを取得します。

```sh
git clone --recursive https://github.com/project-cdim/hw-emulator-reference-compose.git
```

以下のコマンドを実行してビルドと起動を行います。

```sh
cd hw-emulator-reference-compose
docker compose up -d --build
```

## 2. エミュレーターの動作確認

以下のコマンドを実行します。

```sh
docker exec hw-emulator curl http://localhost:5000/redfish/v1/Systems/System-1/Processors | python -m json.tool
```

以下のようなレスポンスが取得できれば正常に動作しています。

```json
{
    "@odata.context": "/redfish/v1/$metadata#ProcessorCollection.ProcessorCollection",
    "@odata.id": "/redfish/v1/Systems/System-1/Processors",
    "@odata.type": "#ProcessorCollection.ProcessorCollection",
    "Members": [
        {
            "@odata.id": "/redfish/v1/Systems/System-1/Processors/PROC-0001"
        }
    ],
    "Members@odata.count": 1,
    "Name": "Processors Collection"
}
```

[Next step: CDIM をインストールする](../install/install.md)
