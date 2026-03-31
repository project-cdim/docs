# 8. 特記事項

## 8.1. 注意事項

### プラグインに必要なパッケージの追加

プラグインを実装する上で必要な場合、サードパーティー製のPythonパッケージを追加できます。

パッケージを追加する場合、以下のパスに配置されている構成案設計の`pyproject.toml`を編集します。
- `layout-design-compose/layout-design/layout-design/pyproject.toml`

`pyproject.toml`のうち、`project`セクションの`dependencies`に必要なパッケージを追加してください。  
このとき、構成案設計側で定義されている依存パッケージおよびそのバージョン制約と整合するよう依存関係を遵守してください。

以下は構成案設計の`pyproject.toml`の抜粋です。

``` toml
[project]
name = "layoutdesign"
version = "0.1.0"
description = ""
authors = [
    {name = "NEC corporation."},
]
dependencies = [        # ここに必要なパッケージを追加
    "jsonschema<5.0.0,>=4.23.0",
    "uvicorn<1.0.0,>=0.30.6",
    "fastapi<1.0.0,>=0.115.0",
    "requests>=2.32.3",
    "pyyaml",
    "tenacity>=9.0.0",
]
requires-python = "<4.0,>=3.14.0"
readme = "README.md"
license = {text = "LICENSE"}
```

パッケージの追加を行った際は、以下のコマンドで構成案設計のコンテナの再ビルドを実行してください。

``` shell
cd <任意のディレクトリパス>/layout-design-compose
docker compose up [-d] --build
```
