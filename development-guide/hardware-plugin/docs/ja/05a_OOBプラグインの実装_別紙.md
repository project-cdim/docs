# 5. OOBプラグインの実装(別紙)

- [表5-1. デバイス種別](#表5-1-デバイス種別)
- [表5-2. `get_device_info`の返り値](#表5-2-get_device_infoの返り値)
- [表5-3. 引数`key_values`](#表5-3-引数key_values)
- [表5-4. `get_spec_info`の返り値](#表5-4-get_spec_infoの返り値)
  - [スペック情報: プロセッサ](#スペック情報-プロセッサ)
  - [スペック情報: メモリ](#スペック情報-メモリ)
  - [スペック情報: ストレージ](#スペック情報-ストレージ)
  - [スペック情報: ネットワークインターフェース](#スペック情報-ネットワークインターフェース)
  - [スペック情報: グラフィックコントローラ](#スペック情報-グラフィックコントローラ)
- [表5-5. スペック情報とREST APIの項目名対応](#表5-5-スペック情報とrest-apiの項目名対応)
  - [スペック情報(項目名対応): プロセッサ](#スペック情報項目名対応-プロセッサ)
  - [スペック情報(項目名対応): メモリ](#スペック情報項目名対応-メモリ)
  - [スペック情報(項目名対応): ストレージ](#スペック情報項目名対応-ストレージ)
  - [スペック情報(項目名対応): ネットワークインターフェース](#スペック情報項目名対応-ネットワークインターフェース)
  - [スペック情報(項目名対応): グラフィックコントローラ](#スペック情報項目名対応-グラフィックコントローラ)
- [表5-6. `get_metric_info`の返り値](#表5-6-get_metric_infoの返り値)
  - [メトリック情報: プロセッサ](#メトリック情報-プロセッサ)
  - [メトリック情報: メモリ](#メトリック情報-メモリ)
  - [メトリック情報: ストレージ](#メトリック情報-ストレージ)
  - [メトリック情報: ネットワークインターフェース](#メトリック情報-ネットワークインターフェース)
- [表5-7.メトリック情報とREST APIの項目名対応](#表5-7-メトリック情報とrest-apiの項目名対応)
  - [メトリック情報(項目名対応): プロセッサ](#メトリック情報項目名対応-プロセッサ)
  - [メトリック情報(項目名対応): メモリ](#メトリック情報項目名対応-メモリ)
  - [メトリック情報(項目名対応): ストレージ](#メトリック情報項目名対応-ストレージ)
  - [メトリック情報(項目名対応): ネットワークインターフェース](#メトリック情報項目名対応-ネットワークインターフェース)
- [表5-8. `get_power_state`の返り値](#表5-8-get_power_stateの返り値)
- [表5-9. 更新メソッドの返り値](#表5-9-更新メソッドの返り値)

## 表5-1. デバイス種別

|No.|デバイス種別      |説明
|:-:|------------------|--------------------------------------------------------
| 1 |Accelerator       |プロセッサ
| 2 |CPU               |プロセッサ
| 3 |DSP               |プロセッサ
| 4 |FPGA              |プロセッサ
| 5 |GPU               |プロセッサ
| 6 |memory            |メモリ
| 7 |storage           |ストレージ
| 8 |networkInterface  |ネットワークインターフェース
| 9 |graphicController |グラフィックコントローラ

## 表5-2. `get_device_info`の返り値

`get_device_info`の返り値は下表の項目を持つ`OOBDeviceListItem`のリストです。

- `OOBDeviceListItem`はPydanticの`BaseModel`を継承しており、辞書と相互に変換することができます。辞書のキーを`辞書キー`列に示します。
- `deviceType`と`oobDeviceID`は必須です。  
  他の項目はOOBプラグインとFMプラグインの連携のために必要な情報です。詳細は[9.1. 注意事項 デバイスの紐づけ](09_特記事項.md#デバイスの紐づけ)を参照してください。

|No.|属性                      |辞書キー               |型   |値
|:-:|--------------------------|-----------------------|-----|----------------------------------------------------------
| 1 |pcie_vendor_id            |PCIeVendorId           |str  |PCIeベンダID
| 2 |pcie_device_id            |PCIeDeviceId           |str  |PCIeデバイスID
| 3 |pcie_device_serial_number |PCIeDeviceSerialNumber |str  |PCIeデバイスシリアル番号
| 4 |cpu_serial_number         |CPUSerialNumber        |str  |プロセッサのシリアル番号
| 5 |cpu_manufacturer          |CPUManufacturer        |str  |プロセッサの製造元
| 6 |cpu_model                 |CPUModel               |str  |プロセッサのモデル番号
| 7 |port_keys                 |portKeys               |dict |スイッチのポートをシステムで一意に識別する情報を格納した辞書
| 8 |device_keys               |deviceKeys             |dict |デバイスをシステムで一意に識別する情報を格納した辞書
| 9 |device_type               |deviceType             |str  |デバイス種別 ([表5-1. デバイス種別](#表5-1-デバイス種別)参照)
|10 |oob_device_id             |oobDeviceID            |str  |デバイスをマネージャーで一意に識別するID

## 表5-3. 引数`key_values`

引数`key_values: list[dict[str, str]]`は下表の項目を持つ辞書のリストです。

|No.|キー           |型    |値
|:-:|---------------|------|--------------------------------------------------------------------------------------------
| 1 |oob_device_id  |str   |OOBデバイスID ([`get_device_info`](05_OOBプラグインの実装.md#51-get_device_info)で取得したもの)
| 2 |device_type    |str   |デバイス種別 ([表5-1. デバイス種別](#表5-1-デバイス種別)参照)

## 表5-4. `get_spec_info`の返り値

`get_spec_info`の返り値は下表の項目を持つ辞書です。

|No.|キー        |型         |値
|:-:|------------|-----------|--------------------------------------------------
| 1 |devices     |list[dict] |デバイスのスペック情報を格納した辞書のリスト

リストの各要素は引数[`key_values`](#表5-3-引数key_values)の各要素に対応し、[デバイス種別](#表5-1-デバイス種別)ごとに異なる項目を持つ辞書です。  
以下にデバイス種別ごとの辞書の項目を示します。

- 入れ子の辞書のキーをドット区切りで表しています。例えばキーが`a.b.c`のとき辞書の値は`辞書["a"]["b"]["c"]`です。
- `deviceID`、`type`、`time`は必須です。他の項目はデバイスから情報を取得できた場合に設定します。

### スペック情報: プロセッサ

|No.|キー                                             |型         |値
|:-:|-------------------------------------------------|-----------|-----------------------------------------------------
| 1 |deviceID                                         |str        |OOBデバイスID
| 2 |type                                             |str        |デバイス種別
| 3 |schema                                           |dict       |プロセッサ情報
| 4 |schema.BaseSpeedMHz                              |int        |プロセッサのベース(公称)クロック速度(MHz)
| 5 |schema.OperatingSpeedMHz                         |int        |動作中のプロセッサーのクロック速度(MHz)
| 6 |schema.TDPWatts                                  |int        |公称熱設計電力(TDP)(W)
| 7 |schema.TotalCores                                |int        |このプロセッサが含むコアの総数
| 8 |schema.TotalEnabledCores                         |int        |このプロセッサに含まれる有効なコアの総数
| 9 |schema.TotalThreads                              |int        |このプロセッサがサポートする実行スレッドの総数
|10 |schema.ProcessorMemory                           |list[dict] |このプロセッサに取り付けられているか統合されているメモリ
|11 |schema.ProcessorMemory.CapacityMiB               |int        |メモリ容量(MiB)
|12 |schema.ProcessorMemory.IntegratedMemory          |bool       |メモリがプロセッサ内に統合されているかどうか
|13 |schema.ProcessorMemory.MemoryType                |str        |プロセッサが使用するメモリのタイプ
|14 |schema.ProcessorMemory.SpeedMHz                  |int        |メモリの動作速度(MHz)
|15 |schema.MemorySummary                             |dict       |このプロセッサに関連するすべてのメモリの概要
|16 |schema.MemorySummary.ECCModeEnabled              |bool       |メモリ ECC モードが有効であるかどうか
|17 |schema.MemorySummary.TotalCacheSizeMiB           |int        |キャッシュメモリの合計サイズ(MiB)
|18 |schema.MemorySummary.TotalMemorySizeMiB          |int        |接続されている揮発性メモリの合計サイズ(MiB)
|19 |schema.InstructionSet                            |str        |プロセッサの命令セット
|20 |schema.ProcessorArchitecture                     |str        |プロセッサのアーキテクチャ
|21 |schema.ProcessorId                               |dict       |このプロセッサの識別情報
|22 |schema.ProcessorId.EffectiveFamily               |str        |有効なファミリ
|23 |schema.ProcessorId.EffectiveModel                |str        |有効なモデル
|24 |schema.ProcessorId.IdentificationRegisters       |str        |プロセッサの製造元が提供する生のプロセッサ識別レジスタ
|25 |schema.ProcessorId.MicrocodeInfo                 |str        |マイクロコード情報
|26 |schema.ProcessorId.ProtectedIdentificationNumber |str        |PPIN (保護されたプロセッサー識別番号)
|27 |schema.ProcessorId.Step                          |str        |ステップ値
|28 |schema.ProcessorId.VendorId                      |str        |ベンダーの識別情報
|29 |schema.SerialNumber                              |str        |プロセッサのシリアル番号
|30 |schema.Socket                                    |str        |プロセッサのソケット
|31 |schema.Manufacturer                              |str        |プロセッサの製造元
|32 |schema.Model                                     |str        |このデバイスの製品モデル番号
|33 |schema.Status                                    |dict       |プロセッサのステータス情報
|34 |schema.Status.State                              |str        |リソース状態
|35 |schema.Status.Health                             |str        |リソースのヘルス状態
|36 |schema.PowerState                                |str        |プロセッサの現在の電源状態
|37 |schema.PowerCapability                           |bool       |電源制御機能が有効かどうか
|38 |link                                             |list[dict] |プロセッサに関連する他のリソースのデバイス情報
|39 |link.type                                        |str        |デバイス種別
|40 |link.deviceID                                    |str        |OOBデバイスID
|41 |time                                             |str        |情報取得日時 (UTC, ISO 8601形式)

### スペック情報: メモリ

|No.|キー                                       |型         |値
|:-:|-------------------------------------------|-----------|-----------------------------------------------------------
| 1 |deviceID                                   |str        |OOBデバイスID
| 2 |type                                       |str        |デバイス種別
| 3 |schema                                     |dict       |メモリ情報
| 4 |schema.CapacityMiB                         |int        |メモリ容量(MiB)
| 5 |schema.LogicalSizeMiB                      |int        |論理メモリの合計サイズ(MiB)
| 6 |schema.NonVolatileSizeMiB                  |int        |不揮発性領域の合計サイズ(MiB)
| 7 |schema.PersistentRegionNumberLimit         |int        |メモリデバイスがサポートできる永続領域の総数
| 8 |schema.PersistentRegionSizeLimitMiB        |int        |永続領域の合計サイズ(MiB)
| 9 |schema.PersistentRegionSizeMaxMiB          |int        |1つの永続領域の最大サイズ(MiB)
|10 |schema.VolatileRegionSizeLimitMiB          |int        |揮発性領域の合計サイズ(MiB)
|11 |schema.VolatileRegionSizeMaxMiB            |int        |1つの揮発性領域の最大サイズ(MiB)
|12 |schema.AllocationAlignmentMiB              |int        |メモリ領域が割り当てられる境界(MiB)
|13 |schema.AllocationIncrementMiB              |int        |メモリ領域の割り当ての最小単位のサイズ(MiB)
|14 |schema.AllowedSpeedsMHz                    |list[int]  |メモリデバイスでサポートされている速度
|15 |schema.OperatingSpeedMHz                   |int        |メモリの動作速度(MHz)
|16 |schema.BusWidthBits                        |int        |ビット単位のバス幅
|17 |schema.DataWidthBits                       |int        |ビット単位のデータ幅
|18 |schema.MaxTDPMilliWatts                    |list[int]  |メモリデバイスがサポートする最大電力バジェットのセット(ミリワット)
|19 |schema.Enabled                             |bool       |メモリが有効になっているかどうか
|20 |schema.MemoryMedia                         |list[str]  |メモリデバイスのメディア
|21 |schema.MemoryType                          |str        |メモリデバイスのタイプ
|22 |schema.MemoryDeviceType                    |str        |メモリデバイスの詳細タイプ入力
|23 |schema.MemoryLocation                      |dict       |ソケットおよびメモリコントローラへのメモリ接続情報
|24 |schema.MemoryLocation.Channel              |int        |メモリ デバイスが接続されているチャネル番号
|25 |schema.MemoryLocation.MemoryController     |int        |メモリ デバイスが接続されているメモリ コントローラ番号
|26 |schema.MemoryLocation.Slot                 |int        |メモリ デバイスが接続されているスロット番号
|27 |schema.MemoryLocation.Socket               |int        |メモリ デバイスが接続されているソケット番号
|28 |schema.SerialNumber                        |str        |メモリのシリアル番号
|29 |schema.Manufacturer                        |str        |メモリデバイスの製造元
|30 |schema.Model                               |str        |このデバイスの製品モデル番号
|31 |schema.Status                              |dict       |メモリのステータス情報
|32 |schema.Status.State                        |str        |リソース状態
|33 |schema.Status.Health                       |str        |リソースのヘルス状態
|34 |schema.PowerState                          |str        |メモリの現在の電源状態
|35 |schema.PowerCapability                     |bool       |電源制御機能が有効かどうか
|36 |link                                       |list[dict] |メモリデバイスに関連するCPUのデバイス情報
|37 |link.type                                  |str        |デバイス種別(CPU固定)
|38 |link.deviceID                              |str        |OOBデバイスID
|39 |time                                       |str        |情報取得日時 (UTC, ISO 8601形式)

### スペック情報: ストレージ

|No.|キー                                             |型         |値
|:-:|-------------------------------------------------|-----------|-----------------------------------------------------
| 1 |deviceID                                         |str        |OOBデバイスID
| 2 |type                                             |str        |デバイス種別
| 3 |schema                                           |dict       |ストレージ情報
| 4 |schema.Storage                                   |dict       |ストレージ情報
| 5 |schema.Storage.Redundancy                        |list[dict] |ストレージサブシステムの冗長性情報
| 6 |schema.Storage.Redundancy.RedundancyEnabled      |bool       |冗長性が有効になっているかどうか
| 7 |schema.Storage.Redundancy.Mode                   |str        |冗長モード
| 8 |schema.Storage.Redundancy.Name                   |str        |リソースまたは配列メンバーの名前
| 9 |schema.Storage.Redundancy.MaxNumSupported        |int        |この特定の冗長グループに許可されるメンバーの最大数
|10 |schema.Storage.Redundancy.MinNumNeeded           |int        |このグループが冗長になるために必要なメンバーの最小数
|11 |schema.Storage.Redundancy.RedundancySet          |list[str]  |冗長メンバー情報(デバイス情報の固有ID)
|12 |schema.Volume                                    |dict       |ボリューム情報
|13 |schema.Volume.AccessCapabilities                 |list[str]  |このボリュームでサポートされているIOアクセス機能
|14 |schema.Volume.OptimumIOSizeBytes                 |int        |このボリュームの最適なIOサイズのバイト数
|15 |schema.Volume.Capacity                           |dict       |このボリュームに対する容量情報
|16 |schema.Volume.Capacity.Data                      |dict       |ユーザーデータに関連する容量情報
|17 |schema.Volume.Capacity.Data.AllocatedBytes       |int        |ストレージによって現在割り当てられているバイト数
|18 |schema.Volume.Capacity.Data.ConsumedBytes        |int        |消費されたバイト数
|19 |schema.Volume.Capacity.Data.GuaranteedBytes      |int        |ストレージで保証されるバイト数
|20 |schema.Volume.Capacity.Data.ProvisionedBytes     |int        |割り当てることができる最大バイト数
|21 |schema.Volume.Capacity.Metadata                  |dict       |メタデータに関連する容量情報
|22 |schema.Volume.Capacity.Metadata.AllocatedBytes   |int        |ストレージによって現在割り当てられているバイト数
|23 |schema.Volume.Capacity.Metadata.ConsumedBytes    |int        |消費されたバイト数
|24 |schema.Volume.Capacity.Metadata.GuaranteedBytes  |int        |ストレージで保証されるバイト数
|25 |schema.Volume.Capacity.Metadata.ProvisionedBytes |int        |割り当てることができる最大バイト数
|26 |schema.Volume.CapacitySnapshot                   |dict       |スナップショットまたはバックアップデータに関連する容量情報
|27 |schema.Volume.Capacity.Snapshot.AllocatedBytes   |int        |ストレージによって現在割り当てられているバイト数
|28 |schema.Volume.Capacity.Snapshot.ConsumedBytes    |int        |消費されたバイト数
|29 |schema.Volume.Capacity.Snapshot.GuaranteedBytes  |int        |ストレージで保証されるバイト数
|30 |schema.Volume.Capacity.Snapshot.ProvisionedBytes |int        |割り当てることができる最大バイト数
|31 |schema.Volume.CapacityBytes                      |int        |このボリュームのバイト単位のサイズ
|32 |schema.Volume.MaxBlockSizeBytes                  |int        |このボリュームのバイト単位の最大ブロックサイズ
|33 |schema.Volume.RecoverableCapacitySourceCount     |int        |このボリュームの代替として使用可能な容量リソースの現在の数
|34 |schema.Volume.RemainingCapacityPercent           |int        |このボリュームに残っている容量のパーセンテージ
|35 |schema.Volume.Manufacturer                       |str        |ボリュームの製造元
|36 |schema.Volume.Model                              |str        |ボリュームのモデル番号
|37 |schema.Volume.Identifiers                        |list[dict] |ボリュームの識別子
|38 |schema.Volume.Identifiers.DurableNameFormat      |str        |永続的な名前プロパティの形式
|39 |schema.Volume.Identifiers.DurableName            |str        |リソースのワールドワイドで永続的な名前
|40 |schema.Drive                                     |dict       |ドライブ情報
|41 |schema.Drive.PredictedMediaLifeLeftPercent       |float      |このドライブで使用できると予測される読み取りと書き込みの割合
|42 |schema.Drive.CapacityBytes                       |int        |このドライブのサイズ(バイト)
|43 |schema.Drive.CapableSpeedGbs                     |float      |このドライブが理想的な状態でストレージと通信する速度
|44 |schema.Drive.NegotiatedSpeedGbs                  |float      |このドライブが現在ストレージと通信する速度
|45 |schema.Drive.HotspareType                        |str        |このドライブが機能するホットスペアのタイプ
|46 |schema.Drive.SerialNumber                        |str        |ドライブのシリアル番号
|47 |schema.Drive.Manufacturer                        |str        |ドライブの製造元
|48 |schema.Drive.Model                               |str        |ドライブのモデル番号
|49 |schema.Drive.Identifiers                         |list[dict] |ドライブの識別子
|50 |schema.Drive.Identifiers.DurableNameFormat       |str        |永続的な名前プロパティの形式
|51 |schema.Drive.Identifiers.DurableName             |str        |リソースのワールドワイドで永続的な名前
|52 |schema.Drive.Status                              |dict       |ストレージのステータス情報
|53 |schema.Drive.Status.State                        |str        |リソース状態
|54 |schema.Drive.Status.Health                       |str        |リソースのヘルス状態
|55 |schema.Drive.PowerState                          |str        |ドライブの現在の電源状態
|56 |schema.Drive.PowerCapability                     |bool       |電源制御機能が有効かどうか
|57 |link                                             |list[dict] |ドライブに関連するCPUのデバイス情報
|58 |link.type                                        |str        |デバイス種別(CPU固定)
|59 |link.deviceID                                    |str        |OOBデバイスID
|60 |time                                             |str        |情報取得日時 (UTC, ISO 8601形式)

### スペック情報: ネットワークインターフェース

|No.|キー                                                                         |型         |値
|:-:|-----------------------------------------------------------------------------|-----------|-------------------------
| 1 |deviceID                                                                     |str        |OOBデバイスID
| 2 |type                                                                         |str        |デバイス種別
| 3 |schema                                                                       |dict       |ネットワークインターフェース情報
| 4 |schema.SerialInterfaces                                                      |dict       |シリアルインターフェース情報
| 5 |schema.SerialInterfaces.BitRate                                              |str        |シリアルインターフェースのデータフローの受信速度と送信速度
| 6 |schema.Network                                                               |dict       |ネットワーク情報
| 7 |schema.Network.Controllers                                                   |list[dict] |ネットワークアダプタを構成するネットワークコントローラ情報
| 8 |schema.Network.Controllers.ControllerCapabilities                            |dict       |コントローラーの機能
| 9 |schema.Network.Controllers.ControllerCapabilities.DataCenterBridging         |dict       |データセンターブリッジング(DCB)
|10 |schema.Network.Controllers.ControllerCapabilities.DataCenterBridging.Capable |bool       |データセンターブリッジング(DCB)に対応しているかどうか
|11 |schema.Network.Controllers.ControllerCapabilities.NetworkDeviceFunctionCount |int        |使用可能な物理機能の最大数
|12 |schema.Network.Controllers.ControllerCapabilities.NetworkPortCount           |int        |物理ポートの数
|13 |schema.Network.Controllers.ControllerCapabilities.NPAR                       |dict       |NICパーティショニング(NPAR)機能
|14 |schema.Network.Controllers.ControllerCapabilities.NPAR.NparCapable           |bool       |NIC機能のパーティショニングをサポートしているかどうか
|15 |schema.Network.Controllers.ControllerCapabilities.NPAR.NparEnabled           |bool       |NIC機能のパーティショニングがアクティブかどうか
|16 |schema.Network.Controllers.ControllerCapabilities.NPIV                       |dict       |N_PortID仮想化(NPIV)機能
|17 |schema.Network.Controllers.ControllerCapabilities.NPIV.MaxDeviceLogins       |int        |全てのポートから同時に許可されるNPIVログインの最大数
|18 |schema.Network.Controllers.ControllerCapabilities.NPIV.MaxPortLogins         |int        |物理ポートごとに許可されるNPIVログインの最大数
|19 |schema.Network.Controllers.ControllerCapabilities.VirtualizationOffload      |dict       |仮想化オフロード
|20 |schema.Network.Controllers.ControllerCapabilities.VirtualizationOffload.VirtualFunction                        |dict  |コントローラの仮想機能
|21 |schema.Network.Controllers.ControllerCapabilities.VirtualizationOffload.VirtualFunction.DeviceMaxCount         |int   |サポートする仮想機能の最大数
|22 |schema.Network.Controllers.ControllerCapabilities.VirtualizationOffload.VirtualFunction.NetworkPortMaxCount    |int   |ポート毎にサポートされる仮想機能の最大数
|23 |schema.Network.Controllers.ControllerCapabilities.VirtualizationOffload.VirtualFunction.MinAssignmentGroupSize |int   |割り当てまたは移動できる仮想機能の最小数
|24 |schema.Network.Controllers.ControllerCapabilities.VirtualizationOffload.SRIOV                                  |dict  |シングルルート入出力仮想化(SR-IOV)機能
|25 |schema.Network.Controllers.ControllerCapabilities.VirtualizationOffload.SRIOV.SRIOVVEPACapable                 |bool  |仮想VEPAモードでSR-IOVをサポートするかどうか
|26 |schema.Network.Controllers.FirmwarePackageVersion                            |str        |ファームウェアパッケージのバージョン
|27 |schema.Network.Controllers.Identifiers                                       |list[dict] |ネットワークアダプターコントローラーの永続的な名前
|28 |schema.Network.Controllers.Identifiers.DurableNameFormat                     |str        |永続的な名前プロパティの形式
|29 |schema.Network.Controllers.Identifiers.DurableName                           |str        |リソースのワールドワイドで永続的な名前
|30 |schema.Network.Controllers.Location                                          |dict       |コントローラーの場所
|31 |schema.Network.Controllers.Location.PartLocation                             |dict       |エンクロージャー内のリソースのパーツの場所
|32 |schema.Network.Controllers.Location.PartLocation.ServiceLabel                |str        |部品の場所のラベル
|33 |schema.Network.Controllers.Location.PartLocation.LocationType                |str        |部品の位置のタイプ
|34 |schema.Network.Controllers.Location.PartLocation.LocationOrdinalValue        |int        |部品の位置を表す番号
|35 |schema.Network.Controllers.Location.PartLocation.Reference                   |str        |パーツ位置の基準点
|36 |schema.Network.Controllers.Location.PartLocation.Orientation                 |str        |LocationOrdinalValueで使用されるスロット列挙の順序
|37 |schema.Network.Controllers.PCIeInterface                                     |dict       |コントローラーのPCIeインターフェイスの詳細
|38 |schema.Network.Controllers.PCIeInterface.LanesInUse                          |int        |このデバイスで使用されているPCIeレーンの数
|39 |schema.Network.Controllers.PCIeInterface.MaxLanes                            |int        |このデバイスがサポートするPCIeレーンの数
|40 |schema.Network.Controllers.PCIeInterface.PCIeType                            |str        |このデバイスで使用されているPCIe仕様のバージョン
|41 |schema.Network.Controllers.PCIeInterface.MaxPCIeType                         |str        |このデバイスがサポートする PCIe 仕様の最新バージョン
|42 |schema.Network.SerialNumber                                                  |str        |このネットワークアダプタのシリアル番号
|43 |schema.Network.Manufacturer                                                  |str        |このネットワークアダプタの製造元
|44 |schema.Network.Model                                                         |str        |このネットワークアダプタの製品モデル番号
|45 |schema.Network.Status                                                        |dict       |ネットワークのステータス情報
|46 |schema.Network.Status.State                                                  |str        |リソース状態
|47 |schema.Network.Status.Health                                                 |str        |リソースのヘルス状態
|48 |schema.Network.PowerState                                                    |str        |ネットワーク機能の現在の電源状態
|49 |schema.Network.PowerCapability                                               |bool       |電源制御機能が有効かどうか
|50 |schema.NetworkDeviceFunctions                                                |dict       |ネットワークデバイス機能
|51 |schema.NetworkDeviceFunctions.DeviceEnabled                                  |bool       |このネットワークデバイス機能が有効になっているかどうか
|52 |schema.NetworkDeviceFunctions.Ethernet                                       |dict       |ネットワークデバイスのイーサネット機能、ステータス、構成値
|53 |schema.NetworkDeviceFunctions.Ethernet.MACAddress                            |str        |現在設定されているMACアドレス
|54 |schema.NetworkDeviceFunctions.Ethernet.MTUSize                               |int        |構成された最大伝送ユニット(MTU)
|55 |schema.NetworkDeviceFunctions.Ethernet.MTUSizeMaximum                        |int        |サポートされている最大最大伝送ユニット(MTU)サイズ
|56 |schema.NetworkDeviceFunctions.Ethernet.PermanentMACAddress                   |str        |永続的なMACアドレス
|57 |schema.NetworkDeviceFunctions.Ethernet.VLAN                                  |dict       |このインターフェイスのVLAN情報
|58 |schema.NetworkDeviceFunctions.Ethernet.VLAN.VLANEnable                       |bool       |このVLANが有効になっているかどうか
|59 |schema.NetworkDeviceFunctions.Ethernet.VLAN.VLANId                           |int        |このVLANのID
|60 |schema.NetworkDeviceFunctions.Limits                                         |list[dict] |ネットワークデバイス機能のバイト制限とパケット制限
|61 |schema.NetworkDeviceFunctions.Limits.BurstBytesPerSecond                     |int        |バーストにおける1秒あたりの最大バイト数
|62 |schema.NetworkDeviceFunctions.Limits.BurstPacketsPerSecond                   |int        |バーストにおける1秒あたりの最大パケット数
|63 |schema.NetworkDeviceFunctions.Limits.Direction                               |str        |この制限が適用されるデータの方向
|64 |schema.NetworkDeviceFunctions.Limits.SustainedBytesPerSecond                 |int        |1秒あたりの持続バイトの最大数
|65 |schema.NetworkDeviceFunctions.Limits.SustainedPacketsPerSecond               |int        |1秒あたりの持続パケットの最大数
|66 |schema.Port                                                                  |dict       |ポート情報
|67 |schema.Port.FunctionMaxBandwidth                                             |list[dict] |このポートに関連付けられた機能の最大帯域幅割り当て率
|68 |schema.Port.FunctionMaxBandwidth.AllocationPercent                           |int        |ネットワークデバイス機能の最大帯域幅割り当て率
|69 |schema.Port.FunctionMinBandwidth                                             |list[dict] |このポートに関連付けられた機能の最小帯域幅割り当て率
|70 |schema.Port.FunctionMinBandwidth.AllocationPercent                           |int        |ネットワークデバイス機能の最小帯域幅割り当て率
|71 |schema.Port.MaxSpeedGbps                                                     |float      |現在構成されているこのポートの最大速度(Gbit/s)
|72 |schema.Port.LinkConfiguration                                                |list[dict] |このポートのリンク構成
|73 |schema.Port.LinkConfiguration.CapableLinkSpeedGbps                           |list[float]|このポートのリンク速度機能(Gbit/s)のセット
|74 |link                                                                         |list[dict] |ネットワークアダプタに関連するCPUのデバイス情報
|75 |link.type                                                                    |str        |デバイス種別(CPU固定)
|76 |link.deviceID                                                                |str        |OOBデバイスID
|77 |time                                                                         |str        |情報取得日時 (UTC, ISO 8601形式)

### スペック情報: グラフィックコントローラ

|No.|キー                         |型         |値
|:-:|-----------------------------|-----------|-------------------------------------------------------------------------
| 1 |deviceID                     |str        |OOBデバイスID
| 2 |type                         |str        |デバイス種別
| 3 |schema                       |dict       |グラフィックコントローラ情報
| 4 |schema.SchemaBiosVersion     |str        |グラフィックスコントローラーBIOSまたはプライマリグラフィックスコントローラーファームウェアのバージョン
| 5 |schema.DriverVersion         |str        |グラフィックスコントローラードライバーのバージョン
| 6 |schema.SerialNumber          |str        |グラフィックスコントローラーのシリアル番号
| 7 |schema.Manufacturer          |str        |グラフィックスコントローラーの製造元
| 8 |schema.Model                 |str        |グラフィックスコントローラーの製品モデル番号
| 9 |schema.Status                |dict       |グラフィックコントローラのステータス情報
|10 |schema.Status.State          |str        |リソース状態
|11 |schema.Status.Health         |str        |リソースのヘルス状態
|12 |time                         |str        |情報取得日時 (UTC, ISO 8601形式)

## 表5-5. スペック情報とREST APIの項目名対応

`get_spec_info`の返り値に格納されるスペック情報と、HW制御機能のREST APIの項目名の対応を以下に示します。

- スペック情報の項目名では、入れ子の辞書のキーをドット区切りで表しています。例えば項目名が`a.b.c`のとき辞書の値は`辞書["a"]["b"]["c"]`です。
- REST APIの項目名も同様に入れ子のオブジェクトのプロパティ名をドット区切りで表しています。

### スペック情報(項目名対応): プロセッサ

|No.|スペック情報                                     |REST API
|:-:|-------------------------------------------------|-----------------------------------------------------------------
| 1 |deviceID                                         |deviceID
| 2 |type                                             |type
| 3 |schema                                           |-
| 4 |schema.BaseSpeedMHz                              |baseSpeedMHz
| 5 |schema.OperatingSpeedMHz                         |operatingSpeedMHz
| 6 |schema.TDPWatts                                  |TDPWatts
| 7 |schema.TotalCores                                |totalCores
| 8 |schema.TotalEnabledCores                         |totalEnabledCores
| 9 |schema.TotalThreads                              |totalThreads
|10 |schema.ProcessorMemory                           |processorMemories
|11 |schema.ProcessorMemory.CapacityMiB               |processorMemories.capacityMiB
|12 |schema.ProcessorMemory.IntegratedMemory          |processorMemories.integrated
|13 |schema.ProcessorMemory.MemoryType                |processorMemories.type
|14 |schema.ProcessorMemory.SpeedMHz                  |processorMemories.speedMHz
|15 |schema.MemorySummary                             |memorySummary
|16 |schema.MemorySummary.ECCModeEnabled              |memorySummary.ECCModeEnabled
|17 |schema.MemorySummary.TotalCacheSizeMiB           |memorySummary.totalCacheSizeMiB
|18 |schema.MemorySummary.TotalMemorySizeMiB          |memorySummary.totalMemorySizeMiB
|19 |schema.InstructionSet                            |instructionSet
|20 |schema.ProcessorArchitecture                     |processorArchitecture
|21 |schema.ProcessorId                               |processorID
|22 |schema.ProcessorId.EffectiveFamily               |processorID.effectiveFamily
|23 |schema.ProcessorId.EffectiveModel                |processorID.effectiveModel
|24 |schema.ProcessorId.IdentificationRegisters       |processorID.identificationRegister
|25 |schema.ProcessorId.MicrocodeInfo                 |processorID.microcodeInfo
|26 |schema.ProcessorId.ProtectedIdentificationNumber |processorID.protectedIdentificationNumber
|27 |schema.ProcessorId.Step                          |processorID.step
|28 |schema.ProcessorId.VendorId                      |processorID.vendorID
|29 |schema.SerialNumber                              |serialNumber
|30 |schema.Socket                                    |socketNum
|31 |schema.Manufacturer                              |manufacturer
|32 |schema.Model                                     |model
|33 |schema.Status                                    |status
|34 |schema.Status.State                              |status.state
|35 |schema.Status.Health                             |status.health
|36 |schema.PowerState                                |powerState
|37 |schema.PowerCapability                           |powerCapability
|38 |link                                             |links
|39 |link.type                                        |links.type
|40 |link.deviceID                                    |links.deviceID

### スペック情報(項目名対応): メモリ

|No.|スペック情報                               |REST API
|:-:|-------------------------------------------|-----------------------------------------------------------------------
| 1 |deviceID                                   |deviceID
| 2 |type                                       |type
| 3 |schema                                     |-
| 4 |schema.CapacityMiB                         |capacityMiB
| 5 |schema.LogicalSizeMiB                      |logicalSizeMiB
| 6 |schema.NonVolatileSizeMiB                  |nonVolatileSizeMiB
| 7 |schema.PersistentRegionNumberLimit         |persistentRegionNumberLimit
| 8 |schema.PersistentRegionSizeLimitMiB        |persistentRegionSizeLimitMiB
| 9 |schema.PersistentRegionSizeMaxMiB          |persistentRegionSizeMaxMiB
|10 |schema.VolatileRegionSizeLimitMiB          |volatileRegionSizeLimitMiB
|11 |schema.VolatileRegionSizeMaxMiB            |volatileRegionSizeMaxMiB
|12 |schema.AllocationAlignmentMiB              |allocationAlignmentMiB
|13 |schema.AllocationIncrementMiB              |allocationIncrementMiB
|14 |schema.AllowedSpeedsMHz                    |allowedSpeedsMHz
|15 |schema.OperatingSpeedMHz                   |operatingSpeedMHz
|16 |schema.BusWidthBits                        |busWidthBits
|17 |schema.DataWidthBits                       |dataWidthBits
|18 |schema.MaxTDPMilliWatts                    |maxTDPsMilliWatts
|19 |schema.Enabled                             |enabled
|20 |schema.MemoryMedia                         |memoryMedia
|21 |schema.MemoryType                          |memoryType
|22 |schema.MemoryDeviceType                    |memoryDeviceType
|23 |schema.MemoryLocation                      |memoryLocation
|24 |schema.MemoryLocation.Channel              |memoryLocation.channel
|25 |schema.MemoryLocation.MemoryController     |memoryLocation.memoryController
|26 |schema.MemoryLocation.Slot                 |memoryLocation.slot
|27 |schema.MemoryLocation.Socket               |memoryLocation.socket
|28 |schema.SerialNumber                        |serialNumber
|29 |schema.Manufacturer                        |manufacturer
|30 |schema.Model                               |model
|31 |schema.Status                              |status
|32 |schema.Status.State                        |status.state
|33 |schema.Status.Health                       |status.health
|34 |schema.PowerState                          |powerState
|35 |schema.PowerCapability                     |powerCapability
|36 |link                                       |links
|37 |link.type                                  |links.type
|38 |link.deviceID                              |links.deviceID

### スペック情報(項目名対応): ストレージ

|No.|スペック情報                                     |REST API
|:-:|-------------------------------------------------|-----------------------------------------------------------------
| 1 |deviceID                                         |deviceID
| 2 |type                                             |type
| 3 |schema                                           |-
| 4 |schema.Storage                                   |-
| 5 |schema.Storage.Redundancy                        |storageRedundancies
| 6 |schema.Storage.Redundancy.RedundancyEnabled      |storageRedundancies.enabled
| 7 |schema.Storage.Redundancy.Mode                   |storageRedundancies.mode
| 8 |schema.Storage.Redundancy.Name                   |storageRedundancies.name
| 9 |schema.Storage.Redundancy.MaxNumSupported        |storageRedundancies.maxNumSupported
|10 |schema.Storage.Redundancy.MinNumNeeded           |storageRedundancies.minNumNeeded
|11 |schema.Storage.Redundancy.RedundancySet          |storageRedundancies.sets
|12 |schema.Volume                                    |-
|13 |schema.Volume.AccessCapabilities                 |volumeAccessCapabilities
|14 |schema.Volume.OptimumIOSizeBytes                 |volumeOptimumIOSizeBytes
|15 |schema.Volume.Capacity                           |volumeCapacity
|16 |schema.Volume.Capacity.Data                      |volumeCapacity.data
|17 |schema.Volume.Capacity.Data.AllocatedBytes       |volumeCapacity.data.allocatedBytes
|18 |schema.Volume.Capacity.Data.ConsumedBytes        |volumeCapacity.data.consumedBytes
|19 |schema.Volume.Capacity.Data.GuaranteedBytes      |volumeCapacity.data.guaranteedBytes
|20 |schema.Volume.Capacity.Data.ProvisionedBytes     |volumeCapacity.data.provisionedBytes
|21 |schema.Volume.Capacity.Metadata                  |volumeCapacity.metadata
|22 |schema.Volume.Capacity.Metadata.AllocatedBytes   |volumeCapacity.metadata.allocatedBytes
|23 |schema.Volume.Capacity.Metadata.ConsumedBytes    |volumeCapacity.metadata.consumedBytes
|24 |schema.Volume.Capacity.Metadata.GuaranteedBytes  |volumeCapacity.metadata.guaranteedBytes
|25 |schema.Volume.Capacity.Metadata.ProvisionedBytes |volumeCapacity.metadata.provisionedBytes
|26 |schema.Volume.CapacitySnapshot                   |volumeCapacity.snapshot
|27 |schema.Volume.Capacity.Snapshot.AllocatedBytes   |volumeCapacity.snapshot.allocatedBytes
|28 |schema.Volume.Capacity.Snapshot.ConsumedBytes    |volumeCapacity.snapshot.consumedBytes
|29 |schema.Volume.Capacity.Snapshot.GuaranteedBytes  |volumeCapacity.snapshot.guaranteedBytes
|30 |schema.Volume.Capacity.Snapshot.ProvisionedBytes |volumeCapacity.snapshot.provisionedBytes
|31 |schema.Volume.CapacityBytes                      |volumeCapacityBytes
|32 |schema.Volume.MaxBlockSizeBytes                  |volumeMaxBlockSizeBytes
|33 |schema.Volume.RecoverableCapacitySourceCount     |volumeRecoverableCapacitySourceCount
|34 |schema.Volume.RemainingCapacityPercent           |volumeRemainingCapacityPercent
|35 |schema.Volume.Manufacturer                       |volumeManufacturer
|36 |schema.Volume.Model                              |volumeModel
|37 |schema.Volume.Identifiers                        |volumeIdentifiers
|38 |schema.Volume.Identifiers.DurableNameFormat      |volumeIdentifiers.durableNameFormat
|39 |schema.Volume.Identifiers.DurableName            |volumeIdentifiers.durableName
|40 |schema.Drive                                     |-
|41 |schema.Drive.PredictedMediaLifeLeftPercent       |drivePredictedMediaLifeLeftPercent
|42 |schema.Drive.CapacityBytes                       |driveCapacityBytes
|43 |schema.Drive.CapableSpeedGbs                     |driveCapableSpeedGbs
|44 |schema.Drive.NegotiatedSpeedGbs                  |driveNegotiatedSpeedGbs
|45 |schema.Drive.HotspareType                        |driveHotspareType
|46 |schema.Drive.SerialNumber                        |driveSerialNumber
|47 |schema.Drive.Manufacturer                        |driveManufacturer
|48 |schema.Drive.Model                               |driveModel
|49 |schema.Drive.Identifiers                         |driveIdentifiers
|50 |schema.Drive.Identifiers.DurableNameFormat       |driveIdentifiers.durableNameFormat
|51 |schema.Drive.Identifiers.DurableName             |driveIdentifiers.durableName
|52 |schema.Drive.Status                              |status
|53 |schema.Drive.Status.State                        |status.state
|54 |schema.Drive.Status.Health                       |status.health
|55 |schema.Drive.PowerState                          |powerState
|56 |schema.Drive.PowerCapability                     |powerCapability
|57 |link                                             |links
|58 |link.type                                        |links.type
|59 |link.deviceID                                    |links.deviceID

### スペック情報(項目名対応): ネットワークインターフェース

|No.|スペック情報                                                                 |REST API
|:-:|-----------------------------------------------------------------------------|-------------------------------------
| 1 |deviceID                                                                     |deviceID
| 2 |type                                                                         |type
| 3 |schema                                                                       |-
| 4 |schema.SerialInterfaces                                                      |-
| 5 |schema.SerialInterfaces.BitRate                                              |bitRate
| 6 |schema.Network                                                               |-
| 7 |schema.Network.Controllers                                                   |controllers
| 8 |schema.Network.Controllers.ControllerCapabilities                            |controllers.capability
| 9 |schema.Network.Controllers.ControllerCapabilities.DataCenterBridging         |controllers.capability.dataCenterBridging
|10 |schema.Network.Controllers.ControllerCapabilities.DataCenterBridging.Capable |controllers.capability.dataCenterBridging.capable
|11 |schema.Network.Controllers.ControllerCapabilities.NetworkDeviceFunctionCount |controllers.capability.networkDeviceFunctionCount
|12 |schema.Network.Controllers.ControllerCapabilities.NetworkPortCount           |controllers.capability.networkPortCount
|13 |schema.Network.Controllers.ControllerCapabilities.NPAR                       |controllers.capability.npar
|14 |schema.Network.Controllers.ControllerCapabilities.NPAR.NparCapable           |controllers.capability.npar.capable
|15 |schema.Network.Controllers.ControllerCapabilities.NPAR.NparEnabled           |controllers.capability.npar.enabled
|16 |schema.Network.Controllers.ControllerCapabilities.NPIV                       |controllers.capability.npiv
|17 |schema.Network.Controllers.ControllerCapabilities.NPIV.MaxDeviceLogins       |controllers.capability.npiv.maxDeviceLogins
|18 |schema.Network.Controllers.ControllerCapabilities.NPIV.MaxPortLogins         |controllers.capability.npiv.maxPortLogins
|19 |schema.Network.Controllers.ControllerCapabilities.VirtualizationOffload      |controllers.capability.virtualizationOffload
|20 |schema.Network.Controllers.ControllerCapabilities.VirtualizationOffload.VirtualFunction                        |controllers.capability.virtualizationOffload.virtualFunction
|21 |schema.Network.Controllers.ControllerCapabilities.VirtualizationOffload.VirtualFunction.DeviceMaxCount         |controllers.capability.virtualizationOffload.virtualFunction.deviceMaxCount
|22 |schema.Network.Controllers.ControllerCapabilities.VirtualizationOffload.VirtualFunction.NetworkPortMaxCount    |controllers.capability.virtualizationOffload.virtualFunction.networkPortMaxCount
|23 |schema.Network.Controllers.ControllerCapabilities.VirtualizationOffload.VirtualFunction.MinAssignmentGroupSize |controllers.capability.virtualizationOffload.virtualFunction.minAssignmentGroupSize
|24 |schema.Network.Controllers.ControllerCapabilities.VirtualizationOffload.SRIOV                                  |controllers.capability.virtualizationOffload.sriov
|25 |schema.Network.Controllers.ControllerCapabilities.VirtualizationOffload.SRIOV.SRIOVVEPACapable                 |controllers.capability.virtualizationOffload.sriov.VEPACapable
|26 |schema.Network.Controllers.FirmwarePackageVersion                            |controllers.firmwarePackageVersion
|27 |schema.Network.Controllers.Identifiers                                       |controllers.identifiers
|28 |schema.Network.Controllers.Identifiers.DurableNameFormat                     |controllers.identifiers.durableNameFormat
|29 |schema.Network.Controllers.Identifiers.DurableName                           |controllers.identifiers.durableName
|30 |schema.Network.Controllers.Location                                          |controllers.location
|31 |schema.Network.Controllers.Location.PartLocation                             |controllers.location.partLocation
|32 |schema.Network.Controllers.Location.PartLocation.ServiceLabel                |controllers.location.partLocation.serviceLabel
|33 |schema.Network.Controllers.Location.PartLocation.LocationType                |controllers.location.partLocation.type
|34 |schema.Network.Controllers.Location.PartLocation.LocationOrdinalValue        |controllers.location.partLocation.ordinalValue
|35 |schema.Network.Controllers.Location.PartLocation.Reference                   |controllers.location.partLocation.reference
|36 |schema.Network.Controllers.Location.PartLocation.Orientation                 |controllers.location.partLocation.orientation
|37 |schema.Network.Controllers.PCIeInterface                                     |controllers.PCIeInterface
|38 |schema.Network.Controllers.PCIeInterface.LanesInUse                          |controllers.PCIeInterface.lanesInUse
|39 |schema.Network.Controllers.PCIeInterface.MaxLanes                            |controllers.PCIeInterface.maxLanes
|40 |schema.Network.Controllers.PCIeInterface.PCIeType                            |controllers.PCIeInterface.PCIeType
|41 |schema.Network.Controllers.PCIeInterface.MaxPCIeType                         |controllers.PCIeInterface.maxPCIeType
|42 |schema.Network.SerialNumber                                                  |networkAdapterSerialNumber
|43 |schema.Network.Manufacturer                                                  |networkAdapterManufacturer
|44 |schema.Network.Model                                                         |networkAdapterModel
|45 |schema.Network.Status                                                        |status
|46 |schema.Network.Status.State                                                  |status.state
|47 |schema.Network.Status.Health                                                 |status.health
|48 |schema.Network.PowerState                                                    |powerState
|49 |schema.Network.PowerCapability                                               |powerCapability
|50 |schema.NetworkDeviceFunctions                                                |-
|51 |schema.NetworkDeviceFunctions.DeviceEnabled                                  |deviceEnabled
|52 |schema.NetworkDeviceFunctions.Ethernet                                       |ethernet
|53 |schema.NetworkDeviceFunctions.Ethernet.MACAddress                            |ethernet.MACAddress
|54 |schema.NetworkDeviceFunctions.Ethernet.MTUSize                               |ethernet.MTUSize
|55 |schema.NetworkDeviceFunctions.Ethernet.MTUSizeMaximum                        |ethernet.MTUSizeMaximum
|56 |schema.NetworkDeviceFunctions.Ethernet.PermanentMACAddress                   |ethernet.permanentMACAddress
|57 |schema.NetworkDeviceFunctions.Ethernet.VLAN                                  |ethernet.vlan
|58 |schema.NetworkDeviceFunctions.Ethernet.VLAN.VLANEnable                       |ethernet.vlan.enable
|59 |schema.NetworkDeviceFunctions.Ethernet.VLAN.VLANId                           |ethernet.vlan.id
|60 |schema.NetworkDeviceFunctions.Limits                                         |limits
|61 |schema.NetworkDeviceFunctions.Limits.BurstBytesPerSecond                     |limits.burstBytesPerSecond
|62 |schema.NetworkDeviceFunctions.Limits.BurstPacketsPerSecond                   |limits.burstPacketsPerSecond
|63 |schema.NetworkDeviceFunctions.Limits.Direction                               |limits.direction
|64 |schema.NetworkDeviceFunctions.Limits.SustainedBytesPerSecond                 |limits.sustainedBytesPerSecond
|65 |schema.NetworkDeviceFunctions.Limits.SustainedPacketsPerSecond               |limits.sustainedPacketsPerSecond
|66 |schema.Port                                                                  |-
|67 |schema.Port.FunctionMaxBandwidth                                             |functionMaxBandwidths
|68 |schema.Port.FunctionMaxBandwidth.AllocationPercent                           |functionMaxBandwidths.allocationPercent
|69 |schema.Port.FunctionMinBandwidth                                             |functionMinBandwidths
|70 |schema.Port.FunctionMinBandwidth.AllocationPercent                           |functionMinBandwidths.allocationPercent
|71 |schema.Port.MaxSpeedGbps                                                     |maxSpeedGbps
|72 |schema.Port.LinkConfiguration                                                |linkConfigurations
|73 |schema.Port.LinkConfiguration.CapableLinkSpeedGbps                           |linkConfigurations.capableLinkSpeedsGbps
|74 |link                                                                         |links
|75 |link.type                                                                    |links.type
|76 |link.deviceID                                                                |links.deviceID

### スペック情報(項目名対応): グラフィックコントローラ

|No.|スペック情報                 |REST API
|:-:|-----------------------------|-------------------------------------------------------------------------------------
| 1 |deviceID                     |deviceID
| 2 |type                         |type
| 3 |schema                       |-
| 4 |schema.SchemaBiosVersion     |biosVersion
| 5 |schema.DriverVersion         |driverVersion
| 6 |schema.SerialNumber          |serialNumber
| 7 |schema.Manufacturer          |manufacturer
| 8 |schema.Model                 |model
| 9 |schema.Status                |status
|10 |schema.Status.State          |status.state
|11 |schema.Status.Health         |status.health

## 表5-6. `get_metric_info`の返り値

`get_metric_info`の返り値は下表の項目を持つ辞書です。

|No.|キー        |型         |値
|:-:|------------|-----------|--------------------------------------------------
| 1 |devices     |list[dict] |デバイスのメトリック情報を格納した辞書のリスト

リストの各要素は引数[`key_values`](#表5-3-引数key_values)の各要素に対応し、[デバイス種別](#表5-1-デバイス種別)ごとに異なる項目を持つ辞書です。  
以下にデバイス種別ごとの辞書の項目を示します。

- 入れ子の辞書のキーをドット区切りで表しています。例えばキーが`a.b.c`のとき辞書の値は`辞書["a"]["b"]["c"]`です。
- `deviceID`、`type`、`time`は必須です。他の項目はデバイスから情報を取得できた場合に設定します。

### メトリック情報: プロセッサ

|No.|キー                                             |型         |値
|:-:|-------------------------------------------------|-----------|-----------------------------------------------------
| 1 |deviceID                                         |str        |OOBデバイスID
| 2 |type                                             |str        |デバイス種別
| 3 |schema                                           |dict       |プロセッサ情報
| 4 |schema.Status                                    |dict       |プロセッサのステータス情報
| 5 |schema.Status.State                              |str        |リソース状態
| 6 |schema.Status.Health                             |str        |リソースのヘルス状態
| 7 |schema.PowerState                                |str        |プロセッサの現在の電源状態
| 8 |schema.PowerCapability                           |bool       |電源制御機能が有効かどうか
| 9 |metric                                           |dict       |メトリック情報
|10 |metric.BandwidthPercent                          |float      |プロセッサの帯域幅の使用率(%)
|11 |metric.OperatingSpeedMHz                         |int        |プロセッサーの動作速度(MHz)
|12 |metric.LocalMemoryBandwidthBytes                 |int        |ローカルメモリ帯域の使用量(バイト単位)
|13 |metric.RemoteMemoryBandwidthBytes                |int        |リモートメモリ帯域の使用量(バイト単位)
|14 |metric.Cache                                     |list[dict] |プロセッサキャッシュの測定値
|15 |metric.Cache.CacheMiss                           |float      |百万単位のキャッシュラインミスの数
|16 |metric.Cache.CacheMissesPerInstruction           |float      |命令ごとのキャッシュミスの数
|17 |metric.Cache.HitRatio                            |float      |キャッシュラインヒット率
|18 |metric.Cache.OccupancyBytes                      |int        |合計キャッシュレベル占有量(バイト単位)
|19 |metric.Cache.OccupancyPercent                    |float      |合計キャッシュ占有率
|20 |metric.CoreMetrics                               |list[dict] |プロセッサコアの測定値
|21 |metric.CoreMetrics.CoreId                        |str        |プロセッサ コア識別子
|22 |metric.CoreMetrics.InstructionsPerCycle          |float      |このコアのクロックサイクルあたりの命令数
|23 |metric.CoreMetrics.CoreCache                     |list[dict] |プロセッサ内のコアのキャッシュ測定値
|24 |metric.CoreMetrics.CoreCache.OccupancyBytes      |int        |合計キャッシュレベル占有量(バイト単位)
|25 |metric.CoreMetrics.CoreCache.OccupancyPercent    |float      |合計キャッシュ占有率
|26 |environment                                      |dict       |エネルギー消費量(J)
|27 |environment.Sensor                               |dict       |センサー情報
|28 |environment.Sensor.SensorResetTime               |str        |時間のプロパティが最後にリセットされた日時(UTC, ISO 8601形式)
|29 |environment.Sensor.SensingInterval               |int        |センサーの読み取り間の時間間隔(秒)
|30 |environment.Sensor.ReadingTime                   |str        |センサーから測定値が取得された日時(UTC, ISO 8601形式)
|31 |environment.EnergyJoules                         |dict       |エネルギー消費量
|32 |environment.EnergyJoules.Reading                 |float      |エネルギー消費量の計測値(J)
|33 |time                                             |str        |情報取得日時 (UTC, ISO 8601形式)

### メトリック情報: メモリ

|No.|キー                                             |型         |値
|:-:|-------------------------------------------------|-----------|-----------------------------------------------------
| 1 |deviceID                                         |str        |OOBデバイスID
| 2 |type                                             |str        |デバイス種別
| 3 |schema                                           |dict       |メモリ情報
| 4 |schema.Enabled                                   |bool       |メモリが有効になっているかどうか
| 5 |schema.Status                                    |dict       |メモリのステータス情報
| 6 |schema.Status.State                              |str        |リソース状態
| 7 |schema.Status.Health                             |str        |リソースのヘルス状態
| 8 |schema.PowerState                                |str        |メモリの現在の電源状態
| 9 |schema.PowerCapability                           |bool       |電源制御機能が有効かどうか
|10 |metric                                           |dict       |メトリック情報
|11 |metric.BandwidthPercent                          |float      |メモリの帯域幅の使用率(%)
|12 |metric.BlockSizeBytes                            |int        |バイト単位のブロックサイズ
|13 |metric.OperatingSpeedMHz                         |int        |必要に応じたMHzまたはMT/s単位のメモリの動作速度
|14 |metric.HealthData                                |dict       |メモリ健全性情報
|15 |metric.HealthData.DataLossDetected               |bool       |データ損失が検出されたかどうか
|16 |metric.HealthData.LastShutdownSuccess            |bool       |最後のシャットダウンが成功したかどうか
|17 |metric.HealthData.PerformanceDegraded            |bool       |パフォーマンスが低下したかどうか
|18 |metric.HealthData.PredictedMediaLifeLeftPercent  |float      |メディアで読み込み／書き込みに使用できると予測される割合
|19 |environment                                      |dict       |エネルギー消費量(J)
|20 |environment.Sensor                               |dict       |センサー情報
|21 |environment.Sensor.SensorResetTime               |str        |時間のプロパティが最後にリセットされた日時(UTC, ISO 8601形式)
|22 |environment.Sensor.SensingInterval               |int        |センサーの読み取り間の時間間隔(秒)
|23 |environment.Sensor.ReadingTime                   |str        |センサーから測定値が取得された日時(UTC, ISO 8601形式)
|24 |environment.EnergyJoules                         |dict       |エネルギー消費量
|25 |environment.EnergyJoules.Reading                 |float      |エネルギー消費量の計測値(J)
|26 |time                                             |str        |情報取得日時 (UTC, ISO 8601形式)

### メトリック情報: ストレージ

|No.|キー                                             |型         |値
|:-:|-------------------------------------------------|-----------|-----------------------------------------------------
| 1 |deviceID                                         |str        |OOBデバイスID
| 2 |type                                             |str        |デバイス種別
| 3 |schema                                           |dict       |ストレージ情報
| 4 |schema.Volume                                    |dict       |ボリューム情報
| 5 |schema.Volume.Capacity                           |dict       |このボリュームに対する容量情報
| 6 |schema.Volume.Capacity.Data                      |dict       |ユーザーデータに関連する容量情報
| 7 |schema.Volume.Capacity.Data.AllocatedBytes       |int        |ストレージによって現在割り当てられているバイト数
| 8 |schema.Volume.Capacity.Data.ConsumedBytes        |int        |消費されたバイト数
| 9 |schema.Volume.Capacity.Data.GuaranteedBytes      |int        |ストレージで保証されるバイト数
|10 |schema.Volume.Capacity.Data.ProvisionedBytes     |int        |割り当てることができる最大バイト数
|11 |schema.Volume.Capacity.Metadata                  |dict       |メタデータに関連する容量情報
|12 |schema.Volume.Capacity.Metadata.AllocatedBytes   |int        |ストレージによって現在割り当てられているバイト数
|13 |schema.Volume.Capacity.Metadata.ConsumedBytes    |int        |消費されたバイト数
|14 |schema.Volume.Capacity.Metadata.GuaranteedBytes  |int        |ストレージで保証されるバイト数
|15 |schema.Volume.Capacity.Metadata.ProvisionedBytes |int        |割り当てることができる最大バイト数
|16 |schema.Volume.Capacity.Snapshot                  |dict       |スナップショットまたはバックアップデータに関連する容量情報
|17 |schema.Volume.Capacity.Snapshot.AllocatedBytes   |int        |ストレージによって現在割り当てられているバイト数
|18 |schema.Volume.Capacity.Snapshot.ConsumedBytes    |int        |消費されたバイト数
|19 |schema.Volume.Capacity.Snapshot.GuaranteedBytes  |int        |ストレージで保証されるバイト数
|20 |schema.Volume.Capacity.Snapshot.ProvisionedBytes |int        |割り当てることができる最大バイト数
|21 |schema.Volume.RemainingCapacityPercent           |int        |このボリュームに残っている容量のパーセンテージ
|22 |schema.Drive                                     |dict       |ドライブ情報
|23 |schema.Drive.NegotiatedSpeedGbs                  |float      |このドライブが現在ストレージと通信する速度
|24 |schema.Drive.Status                              |dict       |ストレージのステータス情報
|25 |schema.Drive.Status.State                        |str        |リソース状態
|26 |schema.Drive.Status.Health                       |str        |リソースのヘルス状態
|27 |schema.Drive.PowerState                          |str        |ドライブの現在の電源状態
|28 |schema.Drive.PowerCapability                     |bool       |電源制御機能が有効かどうか
|29 |environment                                      |dict       |エネルギー消費量(J)
|30 |environment.Sensor                               |dict       |センサー情報
|31 |environment.Sensor.SensorResetTime               |str        |時間のプロパティが最後にリセットされた日時(UTC, ISO 8601形式)
|32 |environment.Sensor.SensingInterval               |int        |センサーの読み取り間の時間間隔(秒)
|33 |environment.Sensor.ReadingTime                   |str        |センサーから測定値が取得された日時(UTC, ISO 8601形式)
|34 |environment.EnergyJoules                         |dict       |エネルギー消費量
|35 |environment.EnergyJoules.Reading                 |float      |エネルギー消費量の計測値(J)
|36 |time                                             |str        |情報取得日時 (UTC, ISO 8601形式)

### メトリック情報: ネットワークインターフェース

|No.|キー                                                 |型         |値
|:-:|-----------------------------------------------------|-----------|-------------------------------------------------
| 1 |deviceID                                             |str        |OOBデバイスID
| 2 |type                                                 |str        |デバイス種別
| 3 |schema                                               |dict       |ネットワークインターフェース情報
| 4 |schema.NetworkDeviceFunctions                        |dict       |ネットワークデバイス機能
| 5 |schema.NetworkDeviceFunctions.DeviceEnabled          |bool       |このネットワークデバイス機能が有効になっているかどうか
| 6 |schema.Network.Status                                |dict       |ネットワークのステータス情報
| 7 |schema.Network.Status.State                          |str        |リソース状態
| 8 |schema.Network.Status.Health                         |str        |リソースのヘルス状態
| 9 |schema.Network.PowerState                            |str        |ネットワーク機能の現在の電源状態
|10 |schema.Network.PowerCapability                       |bool       |電源制御機能が有効かどうか
|11 |metric                                               |dict       |メトリック情報
|12 |metric.Network                                       |dict       |ネットワーク
|13 |metric.Network.CPUCorePercent                        |float      |デバイスのCPUコア使用率(%)
|14 |metric.Network.HostBusRXPercent                      |float      |PCIeなどのホストバス、RX使用率(%)
|15 |metric.Network.HostBusTXPercent                      |float      |PCIeなどのホストバス、TX使用率(%)
|16 |metric.NetworkDeviceFunctions                        |dict       |ネットワークデバイス機能
|17 |metric.NetworkDeviceFunctions.RXAvgQueueDepthPercent |float      |RX平均キュー深度
|18 |metric.NetworkDeviceFunctions.TXAvgQueueDepthPercent |float      |TX平均キュー深度
|19 |metric.NetworkDeviceFunctions.RXBytes                |int        |ネットワーク機能で受信された合計バイト数
|20 |metric.NetworkDeviceFunctions.RXFrames               |int        |ネットワーク機能で受信したフレームの総数
|21 |metric.NetworkDeviceFunctions.TXBytes                |int        |ネットワーク機能で送信された合計バイト数
|22 |metric.NetworkDeviceFunctions.TXFrames               |int        |ネットワーク機能で送信されたフレームの総数
|23 |environment                                          |dict       |エネルギー消費量(J)
|24 |environment.Sensor                                   |dict       |センサー情報
|25 |environment.Sensor.SensorResetTime                   |str        |時間のプロパティが最後にリセットされた日時(UTC, ISO 8601形式)
|26 |environment.Sensor.SensingInterval                   |int        |センサーの読み取り間の時間間隔(秒)
|27 |environment.Sensor.ReadingTime                       |str        |センサーから測定値が取得された日時(UTC, ISO 8601形式)
|28 |environment.EnergyJoules                             |dict       |エネルギー消費量
|29 |environment.EnergyJoules.Reading                     |float      |エネルギー消費量の計測値(J)
|30 |time                                                 |str        |情報取得日時 (UTC, ISO 8601形式)

## 表5-7. メトリック情報とREST APIの項目名対応

### メトリック情報(項目名対応): プロセッサ

|No.|メトリック情報                                   |REST API
|:-:|-------------------------------------------------|-----------------------------------------------------------------
| 1 |deviceID                                         |deviceID
| 2 |type                                             |type
| 3 |schema                                           |-
| 4 |schema.Status                                    |status
| 5 |schema.Status.State                              |status.state
| 6 |schema.Status.Health                             |status.health
| 7 |schema.PowerState                                |powerState
| 8 |schema.PowerCapability                           |powerCapability
| 9 |metric                                           |-
|10 |metric.BandwidthPercent                          |metricBandwidthPercent
|11 |metric.OperatingSpeedMHz                         |metricOperatingSpeedMHz
|12 |metric.LocalMemoryBandwidthBytes                 |metricLocalMemoryBandwidthBytes
|13 |metric.RemoteMemoryBandwidthBytes                |metricRemoteMemoryBandwidthBytes
|14 |metric.Cache                                     |metricCaches
|15 |metric.Cache.CacheMiss                           |metricCaches.miss
|16 |metric.Cache.CacheMissesPerInstruction           |metricCaches.missesPerInstruction
|17 |metric.Cache.HitRatio                            |metricCaches.hitRatio
|18 |metric.Cache.OccupancyBytes                      |metricCaches.occupancyBytes
|19 |metric.Cache.OccupancyPercent                    |metricCaches.occupancyPercent
|20 |metric.CoreMetrics                               |metricCoreMetrics
|21 |metric.CoreMetrics.CoreId                        |metricCoreMetrics.coreID
|22 |metric.CoreMetrics.InstructionsPerCycle          |metricCoreMetrics.instructionsPerCycle
|23 |metric.CoreMetrics.CoreCache                     |metricCoreMetrics.coreCaches
|24 |metric.CoreMetrics.CoreCache.OccupancyBytes      |metricCoreMetrics.coreCaches.occupancyBytes
|25 |metric.CoreMetrics.CoreCache.OccupancyPercent    |metricCoreMetrics.coreCaches.occupancyPercent
|26 |environment                                      |metricEnergyJoules
|27 |environment.Sensor                               |-
|28 |environment.Sensor.SensorResetTime               |metricEnergyJoules.sensorResetTime
|29 |environment.Sensor.SensingInterval               |metricEnergyJoules.sensingInterval
|30 |environment.Sensor.ReadingTime                   |metricEnergyJoules.readingTime
|31 |environment.EnergyJoules                         |-
|32 |environment.EnergyJoules.Reading                 |metricEnergyJoules.reading

### メトリック情報(項目名対応): メモリ

|No.|メトリック情報                                   |REST API
|:-:|-------------------------------------------------|-----------------------------------------------------------------
| 1 |deviceID                                         |deviceID
| 2 |type                                             |type
| 3 |schema                                           |-
| 4 |schema.Enabled                                   |enabled
| 5 |schema.Status                                    |status
| 6 |schema.Status.State                              |status.state
| 7 |schema.Status.Health                             |status.health
| 8 |schema.PowerState                                |powerState
| 9 |schema.PowerCapability                           |powerCapability
|10 |metric                                           |-
|11 |metric.BandwidthPercent                          |metricBandwidthPercent
|12 |metric.BlockSizeBytes                            |metricBlockSizeBytes
|13 |metric.OperatingSpeedMHz                         |metricOperatingSpeedMHz
|14 |metric.HealthData                                |metricHealthData
|15 |metric.HealthData.DataLossDetected               |metricHealthData.dataLossDetected
|16 |metric.HealthData.LastShutdownSuccess            |metricHealthData.lastShutdownSuccess
|17 |metric.HealthData.PerformanceDegraded            |metricHealthData.performanceDegraded
|18 |metric.HealthData.PredictedMediaLifeLeftPercent  |metricHealthData.predictedMediaLifeLeftPercent
|19 |environment                                      |metricEnergyJoules
|20 |environment.Sensor                               |-
|21 |environment.Sensor.SensorResetTime               |metricEnergyJoules.sensorResetTime
|22 |environment.Sensor.SensingInterval               |metricEnergyJoules.sensingInterval
|23 |environment.Sensor.ReadingTime                   |metricEnergyJoules.readingTime
|24 |environment.EnergyJoules                         |-
|25 |environment.EnergyJoules.Reading                 |metricEnergyJoules.reading

### メトリック情報(項目名対応): ストレージ

|No.|メトリック情報                                   |REST API
|:-:|-------------------------------------------------|-----------------------------------------------------------------
| 1 |deviceID                                         |deviceID
| 2 |type                                             |type
| 3 |schema                                           |-
| 4 |schema.Volume                                    |-
| 5 |schema.Volume.Capacity                           |volumeCapacity
| 6 |schema.Volume.Capacity.Data                      |volumeCapacity.data
| 7 |schema.Volume.Capacity.Data.AllocatedBytes       |volumeCapacity.data.allocatedBytes
| 8 |schema.Volume.Capacity.Data.ConsumedBytes        |volumeCapacity.data.consumedBytes
| 9 |schema.Volume.Capacity.Data.GuaranteedBytes      |volumeCapacity.data.guaranteedBytes
|10 |schema.Volume.Capacity.Data.ProvisionedBytes     |volumeCapacity.data.provisionedBytes
|11 |schema.Volume.Capacity.Metadata                  |volumeCapacity.metadata
|12 |schema.Volume.Capacity.Metadata.AllocatedBytes   |volumeCapacity.metadata.allocatedBytes
|13 |schema.Volume.Capacity.Metadata.ConsumedBytes    |volumeCapacity.metadata.consumedBytes
|14 |schema.Volume.Capacity.Metadata.GuaranteedBytes  |volumeCapacity.metadata.guaranteedBytes
|15 |schema.Volume.Capacity.Metadata.ProvisionedBytes |volumeCapacity.metadata.provisionedBytes
|16 |schema.Volume.Capacity.Snapshot                  |volumeCapacity.snapshot
|17 |schema.Volume.Capacity.Snapshot.AllocatedBytes   |volumeCapacity.snapshot.allocatedBytes
|18 |schema.Volume.Capacity.Snapshot.ConsumedBytes    |volumeCapacity.snapshot.consumedBytes
|19 |schema.Volume.Capacity.Snapshot.GuaranteedBytes  |volumeCapacity.snapshot.guaranteedBytes
|20 |schema.Volume.Capacity.Snapshot.ProvisionedBytes |volumeCapacity.snapshot.provisionedBytes
|21 |schema.Volume.RemainingCapacityPercent           |volumeRemainingCapacityPercent
|22 |schema.Drive                                     |-
|23 |schema.Drive.NegotiatedSpeedGbs                  |driveNegotiatedSpeedGbs
|24 |schema.Drive.Status                              |status
|25 |schema.Drive.Status.State                        |status.state
|26 |schema.Drive.Status.Health                       |status.health
|27 |schema.Drive.PowerState                          |powerState
|28 |schema.Drive.PowerCapability                     |powerCapability
|29 |environment                                      |metricEnergyJoules
|30 |environment.Sensor                               |-
|31 |environment.Sensor.SensorResetTime               |metricEnergyJoules.sensorResetTime
|32 |environment.Sensor.SensingInterval               |metricEnergyJoules.sensingInterval
|33 |environment.Sensor.ReadingTime                   |metricEnergyJoules.readingTime
|34 |environment.EnergyJoules                         |-
|35 |environment.EnergyJoules.Reading                 |metricEnergyJoules.reading

### メトリック情報(項目名対応): ネットワークインターフェース

|No.|メトリック情報                                       |REST API
|:-:|-----------------------------------------------------|-------------------------------------------------------------
| 1 |deviceID                                             |deviceID
| 2 |type                                                 |type
| 3 |schema                                               |-
| 4 |schema.NetworkDeviceFunctions                        |-
| 5 |schema.NetworkDeviceFunctions.DeviceEnabled          |deviceEnabled
| 6 |schema.Network.Status                                |status
| 7 |schema.Network.Status.State                          |status.state
| 8 |schema.Network.Status.Health                         |status.health
| 9 |schema.Network.PowerState                            |powerState
|10 |schema.Network.PowerCapability                       |powerCapability
|11 |metric                                               |-
|12 |metric.Network                                       |-
|13 |metric.Network.CPUCorePercent                        |metricsCPUCorePercent
|14 |metric.Network.HostBusRXPercent                      |metricsHostBusRXPercent
|15 |metric.Network.HostBusTXPercent                      |metricsHostBusTXPercent
|16 |metric.NetworkDeviceFunctions                        |-
|17 |metric.NetworkDeviceFunctions.RXAvgQueueDepthPercent |metricsRXAvgQueueDepthPercent
|18 |metric.NetworkDeviceFunctions.TXAvgQueueDepthPercent |metricsTXAvgQueueDepthPercent
|19 |metric.NetworkDeviceFunctions.RXBytes                |metricsRXBytes
|20 |metric.NetworkDeviceFunctions.RXFrames               |metricsRXFrames
|21 |metric.NetworkDeviceFunctions.TXBytes                |metricsTXBytes
|22 |metric.NetworkDeviceFunctions.TXFrames               |metricsTXFrames
|23 |environment                                          |metricEnergyJoules
|24 |environment.Sensor                                   |-
|25 |environment.Sensor.SensorResetTime                   |metricEnergyJoules.sensorResetTime
|26 |environment.Sensor.SensingInterval                   |metricEnergyJoules.sensingInterval
|27 |environment.Sensor.ReadingTime                       |metricEnergyJoules.readingTime
|28 |environment.EnergyJoules                             |-
|29 |environment.EnergyJoules.Reading                     |metricEnergyJoules.reading

## 表5-8. `get_power_state`の返り値

`get_power_state`の返り値は下表の項目を持つ辞書です。

|No.|キー        |型         |値
|:-:|------------|-----------|--------------------------------------------------
| 1 |devices     |list[dict] |デバイスの電源状態を格納した辞書のリスト

リストの各要素は引数[`key_values`](#表5-3-引数key_values)の各要素に対応します。  
以下に辞書の項目を示します。

- `deviceID`、`type`、`time`は必須です。`powerState`はデバイスから取得できた場合に設定します。

|No.|キー                   |型   |値
|:-:|-----------------------|-----|-------------------------------------------------------------------------------------
| 1 |deviceID               |str  |OOBデバイスID
| 2 |type                   |str  |デバイス種別
| 3 |powerState             |str  |電源状態(`On`, `Off`, `Paused`, `PoweringOff`, `PoweringOn`, `Unknown`のいずれか)
| 4 |time                   |str  |情報取得日時 (UTC, ISO 8601形式)

## 表5-9. 更新メソッドの返り値

更新メソッドの返り値は下表の項目を持つ辞書のリストです。

|No.|キー      |型   |値
|:-:|----------|-----|----------------------------------------------------------
| 1 |deviceID  |str  |OOBデバイスID
| 2 |type      |str  |デバイス種別
| 3 |status    |int  |REST APIのHTTPレスポンスステータスコード
| 4 |time      |str  |処理実行日時 (UTC, ISO 8601形式)
