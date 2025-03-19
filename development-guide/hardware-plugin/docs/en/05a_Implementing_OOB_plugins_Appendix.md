# 5. Implementing OOB Plugins (Appendix)

- [Table 5-1. Device Type](#table-5-1-device-type)
- [Table 5-2. Return Value of `get_device_info`](#table-5-2-return-value-of-get_device_info)
- [Table 5-3. Parameter `key_values`](#table-5-3-parameter-key_values)
- [Table 5-4. Return Value of `get_spec_info`](#table-5-4-return-value-of-get_spec_info)
  - [Spec Information: Processor](#spec-information-processor)
  - [Spec Information: Memory](#spec-information-memory)
  - [Spec Information: Storage](#spec-information-storage)
  - [Spec Information: Network Interface](#spec-information-network-interface)
  - [Spec Information: Graphics Controller](#spec-information-graphics-controller)
- [Table 5-5. Mapping from Spec Information to REST API Item Names](#table-5-5-mapping-from-spec-information-to-rest-api-item-names)
  - [Spec Information(Mapping): Processor](#spec-informationmapping-processor)
  - [Spec Information(Mapping): Memory](#spec-informationmapping-memory)
  - [Spec Information(Mapping): Storage](#spec-informationmapping-storage)
  - [Spec Information(Mapping): Network Interface](#spec-informationmapping-network-interface)
  - [Spec Information(Mapping): Graphics Controller](#spec-informationmapping-graphics-controller)
- [Table 5-6. Return Value of `get_metric_info`](#table-5-6-return-value-of-get_metric_info)
  - [Metric Information: Processor](#metric-information-processor)
  - [Metric Information: Memory](#metric-information-memory)
  - [Metric Information: Storage](#metric-information-storage)
  - [Metric Information: Network Interface](#metric-information-network-interface)
- [Table 5-7. Mapping from Metric Information to REST API Item Names](#table-5-7-mapping-from-metric-information-to-rest-api-item-names)
  - [Metric Information(Mapping): Processor](#metric-informationmapping-processor)
  - [Metric Information(Mapping): Memory](#metric-informationmapping-memory)
  - [Metric Information(Mapping): Storage](#metric-informationmapping-storage)
  - [Metric Information(Mapping): Network Interface](#metric-informationmapping-network-interface)
- [Table 5-8. Return Value of `get_power_state`](#table-5-8-return-value-of-get_power_state)
- [Table 5-9. Return Value of Update Methods](#table-5-9-return-value-of-update-methods)

## Table 5-1. Device Type

|No.|Device Type       |Description
|:-:|------------------|--------------------------------------------------------
| 1 |Accelerator       |Processor
| 2 |CPU               |Processor
| 3 |DSP               |Processor
| 4 |FPGA              |Processor
| 5 |GPU               |Processor
| 6 |memory            |Memory
| 7 |storage           |Storage
| 8 |networkInterface  |Network interface
| 9 |graphicController |Graphics controller

## Table 5-2. Return Value of `get_device_info`

The return value of `get_device_info` is a list of `OOBDeviceListItem` with the items in the table below.

- `OOBDeviceListItem` inherits from Pydantic's `BaseModel` and can be converted to and from dictionaries.
  The keys of the dictionary are shown in the `Dictionary Key` column.
- `deviceType` and `oobDeviceID` are required.  
  The other items are necessary information for the linkage between the OOB plugin and the FM plugin.
  For details, refer to [9.1. Notice / Device Linking](09_Special_Notes.md#device-linking).

|No.|Attribute                 |Dictionary Key         |Type |Value
|:-:|--------------------------|-----------------------|-----|----------------------------------------------------------
| 1 |pcie_vendor_id            |PCIeVendorId           |str  |PCIe vendor ID
| 2 |pcie_device_id            |PCIeDeviceId           |str  |PCIe device ID
| 3 |pcie_device_serial_number |PCIeDeviceSerialNumber |str  |PCIe device serial number
| 4 |cpu_serial_number         |CPUSerialNumber        |str  |Processor serial number
| 5 |cpu_manufacturer          |CPUManufacturer        |str  |Processor manufacturer
| 6 |cpu_model                 |CPUModel               |str  |Processor model number
| 7 |port_keys                 |portKeys               |dict |A dictionary containing information to uniquely identify a port on a switch in the system
| 8 |device_keys               |deviceKeys             |dict |A dictionary containing information to uniquely identify the device in the system
| 9 |device_type               |deviceType             |str  |Device type (see [Table 5-1. Device Type](#table-5-1-device-type))
|10 |oob_device_id             |oobDeviceID            |str  |An ID to uniquely identify the device in the manager

## Table 5-3. Parameter `key_values`

The parameter `key_values: list[dict[str, str]]` is a list of dictionaries with the items in the table below.

|No.|Key            |Type  |Value
|:-:|---------------|------|--------------------------------------------------------------------------------------------
| 1 |oob_device_id  |str   |OOB device ID (returned by [`get_device_info`](05_Implementing_OOB_plugins.md#51-get_device_info))
| 2 |device_type    |str   |Device type (see [Table 5-1. Device Type](#table-5-1-device-type))

## Table 5-4. Return Value of `get_spec_info`

The return value of `get_spec_info` is a dictionary with the items in the table below.

|No.|Key         |Type       |Value
|:-:|------------|-----------|--------------------------------------------------
| 1 |devices     |list[dict] |A list of dictionaries containing device spec information

Each element of the list corresponds to each element of the parameter [`key_values`](#table-5-3-parameter-key_values)
and is a dictionary with a different entry for each [Device Type](#table-5-1-device-type).  
The following are dictionary entries for each device type.

- Dotted keys in nested dictionaries. For example, if the key is `a.b.c`, the dictionary value is `dictionary["a"]["b"]["c"]`.
- `deviceID`, `type`, and `time` are required. The other items are set if the information can be retrieved from the device.

### Spec Information: Processor

|No.|Key                                              |Type       |Value
|:-:|-------------------------------------------------|-----------|-----------------------------------------------------
| 1 |deviceID                                         |str        |OOB device ID
| 2 |type                                             |str        |Device type
| 3 |schema                                           |dict       |Processor information
| 4 |schema.BaseSpeedMHz                              |int        |Processor base (nominal) clock speed (MHz)
| 5 |schema.OperatingSpeedMHz                         |int        |The clock speed of the operating processor (MHz)
| 6 |schema.TDPWatts                                  |int        |Thermal design power (TDP) (W)
| 7 |schema.TotalCores                                |int        |The total number of cores this processor contains
| 8 |schema.TotalEnabledCores                         |int        |The total number of active cores in this processor
| 9 |schema.TotalThreads                              |int        |The total number of execution threads supported by this processor
|10 |schema.ProcessorMemory                           |list[dict] |Memory installed or integrated in this processor
|11 |schema.ProcessorMemory.CapacityMiB               |int        |Memory Capacity (MiB)
|12 |schema.ProcessorMemory.IntegratedMemory          |bool       |Whether the memory is integrated into the processor
|13 |schema.ProcessorMemory.MemoryType                |str        |The type of memory used by the processor
|14 |schema.ProcessorMemory.SpeedMHz                  |int        |Memory operating speed (MHz)
|15 |schema.MemorySummary                             |dict       |Overview of all memory associated with this processor
|16 |schema.MemorySummary.ECCModeEnabled              |bool       |Whether memory ECC mode is enabled
|17 |schema.MemorySummary.TotalCacheSizeMiB           |int        |Total size of cache memory (MiB)
|18 |schema.MemorySummary.TotalMemorySizeMiB          |int        |Total size of connected volatile memory (MiB)
|19 |schema.InstructionSet                            |str        |Processor instruction set
|20 |schema.ProcessorArchitecture                     |str        |Processor architecture
|21 |schema.ProcessorId                               |dict       |Identification information for this processor
|22 |schema.ProcessorId.EffectiveFamily               |str        |Effective families
|23 |schema.ProcessorId.EffectiveModel                |str        |Effective models
|24 |schema.ProcessorId.IdentificationRegisters       |str        |Raw processor identification registers provided by the processor manufacturer
|25 |schema.ProcessorId.MicrocodeInfo                 |str        |Microcode information
|26 |schema.ProcessorId.ProtectedIdentificationNumber |str        |PPIN (Protected Processor Identification Number)
|27 |schema.ProcessorId.Step                          |str        |Step values
|28 |schema.ProcessorId.VendorId                      |str        |Vendor identification
|29 |schema.SerialNumber                              |str        |Processor serial number
|30 |schema.Socket                                    |str        |Processor socket
|31 |schema.Manufacturer                              |str        |Processor manufacturer
|32 |schema.Model                                     |str        |Product model number of this device
|33 |schema.Status                                    |dict       |Processor status information
|34 |schema.Status.State                              |str        |Resource state
|35 |schema.Status.Health                             |str        |Resource health state
|36 |schema.PowerState                                |str        |The current power state of the processor
|37 |schema.PowerCapability                           |bool       |Whether the power control function is enabled
|38 |link                                             |list[dict] |Device information for other resources related to the processor
|39 |link.type                                        |str        |Device type
|40 |link.deviceID                                    |str        |OOB device ID
|41 |time                                             |str        |Date and time of information acquisition (UTC, ISO 8601 format)

### Spec Information: Memory

|No.|Key                                        |Type       |Value
|:-:|-------------------------------------------|-----------|-----------------------------------------------------------
| 1 |deviceID                                   |str        |OOB device ID
| 2 |type                                       |str        |Device type
| 3 |schema                                     |dict       |Memory information
| 4 |schema.CapacityMiB                         |int        |Memory capacity (MiB)
| 5 |schema.LogicalSizeMiB                      |int        |Total size of logical memory (MiB)
| 6 |schema.NonVolatileSizeMiB                  |int        |Total size of non-volatile area (MiB)
| 7 |schema.PersistentRegionNumberLimit         |int        |The total number of persistent regions that the memory device can support
| 8 |schema.PersistentRegionSizeLimitMiB        |int        |Total size of persistent space (MiB)
| 9 |schema.PersistentRegionSizeMaxMiB          |int        |Maximum size of a single persistent region (MiB)
|10 |schema.VolatileRegionSizeLimitMiB          |int        |Total size of the volatile region (MiB)
|11 |schema.VolatileRegionSizeMaxMiB            |int        |Maximum size of one volatile region (MiB)
|12 |schema.AllocationAlignmentMiB              |int        |Boundaries at which memory regions are allocated (MiB)
|13 |schema.AllocationIncrementMiB              |int        |Smallest unit size of memory space allocation (MiB)
|14 |schema.AllowedSpeedsMHz                    |list[int]  |Speeds supported by memory devices
|15 |schema.OperatingSpeedMHz                   |int        |Memory operating speed (MHz)
|16 |schema.BusWidthBits                        |int        |Bus width in bits
|17 |schema.DataWidthBits                       |int        |Data width in bits
|18 |schema.MaxTDPMilliWatts                    |list[int]  |The set of maximum power budgets supported by the memory device (mW)
|19 |schema.Enabled                             |bool       |Whether memory is enabled
|20 |schema.MemoryMedia                         |list[str]  |Memory device media
|21 |schema.MemoryType                          |str        |Types of memory devices
|22 |schema.MemoryDeviceType                    |str        |Advanced type input for memory devices
|23 |schema.MemoryLocation                      |dict       |Memory connection information to sockets and memory controllers
|24 |schema.MemoryLocation.Channel              |int        |The channel number to which the memory device is connected
|25 |schema.MemoryLocation.MemoryController     |int        |The memory controller number to which the memory device is connected
|26 |schema.MemoryLocation.Slot                 |int        |The slot number to which the memory device is connected
|27 |schema.MemoryLocation.Socket               |int        |The socket number to which the memory device is connected
|28 |schema.SerialNumber                        |str        |Memory serial number
|29 |schema.Manufacturer                        |str        |Manufacturer of the memory device
|30 |schema.Model                               |str        |Product model number of this device
|31 |schema.Status                              |dict       |Memory status information
|32 |schema.Status.State                        |str        |Resource state
|33 |schema.Status.Health                       |str        |Resource health state
|34 |schema.PowerState                          |str        |The current power state of the memory
|35 |schema.PowerCapability                     |bool       |Whether the power control function is enabled
|36 |link                                       |list[dict] |Device information for the CPU in relation to the memory device
|37 |link.type                                  |str        |Device type (always CPU)
|38 |link.deviceID                              |str        |OOB device ID
|39 |time                                       |str        |Date and time of information acquisition (UTC, ISO 8601 format)

### Spec Information: Storage

|No.|Key                                              |Type       |Value
|:-:|-------------------------------------------------|-----------|-----------------------------------------------------
| 1 |deviceID                                         |str        |OOB device ID
| 2 |type                                             |str        |Device type
| 3 |schema                                           |dict       |storage information
| 4 |schema.Storage                                   |dict       |storage information
| 5 |schema.Storage.Redundancy                        |list[dict] |Storage subsystem redundancy information
| 6 |schema.Storage.Redundancy.RedundancyEnabled      |bool       |Whether redundancy is enabled
| 7 |schema.Storage.Redundancy.Mode                   |str        |Redundancy mode
| 8 |schema.Storage.Redundancy.Name                   |str        |The name of the resource or array member
| 9 |schema.Storage.Redundancy.MaxNumSupported        |int        |Maximum number of members allowed for this particular redundancy group
|10 |schema.Storage.Redundancy.MinNumNeeded           |int        |The minimum number of members required for this group to be redundant
|11 |schema.Storage.Redundancy.RedundancySet          |list[str]  |Redundant member information (unique ID of device information)
|12 |schema.Volume                                    |dict       |Volume information
|13 |schema.Volume.AccessCapabilities                 |list[str]  |IO access features supported by this volume
|14 |schema.Volume.OptimumIOSizeBytes                 |int        |The number of bytes for the optimal IO size for this volume
|15 |schema.Volume.Capacity                           |dict       |Capacity information for this volume
|16 |schema.Volume.Capacity.Data                      |dict       |Capacity information related to user data
|17 |schema.Volume.Capacity.Data.AllocatedBytes       |int        |The number of bytes currently allocated by the storage
|18 |schema.Volume.Capacity.Data.ConsumedBytes        |int        |Number of bytes consumed
|19 |schema.Volume.Capacity.Data.GuaranteedBytes      |int        |Number of bytes guaranteed for storage
|20 |schema.Volume.Capacity.Data.ProvisionedBytes     |int        |Maximum number of bytes that can be allocated
|21 |schema.Volume.Capacity.Metadata                  |dict       |Capacity information related to metadata
|22 |schema.Volume.Capacity.Metadata.AllocatedBytes   |int        |The number of bytes currently allocated by the storage
|23 |schema.Volume.Capacity.Metadata.ConsumedBytes    |int        |Number of bytes consumed
|24 |schema.Volume.Capacity.Metadata.GuaranteedBytes  |int        |Number of bytes guaranteed for storage
|25 |schema.Volume.Capacity.Metadata.ProvisionedBytes |int        |Maximum number of bytes that can be allocated
|26 |schema.Volume.CapacitySnapshot                   |dict       |Capacity information related to snapshot or backup data
|27 |schema.Volume.Capacity.Snapshot.AllocatedBytes   |int        |The number of bytes currently allocated by the storage
|28 |schema.Volume.Capacity.Snapshot.ConsumedBytes    |int        |Number of bytes consumed
|29 |schema.Volume.Capacity.Snapshot.GuaranteedBytes  |int        |Number of bytes guaranteed for storage
|30 |schema.Volume.Capacity.Snapshot.ProvisionedBytes |int        |Maximum number of bytes that can be allocated
|31 |schema.Volume.CapacityBytes                      |int        |Size of this volume in bytes
|32 |schema.Volume.MaxBlockSizeBytes                  |int        |Maximum block size in bytes for this volume
|33 |schema.Volume.RecoverableCapacitySourceCount     |int        |The current number of capacity resources that can be used as replacements for this volume
|34 |schema.Volume.RemainingCapacityPercent           |int        |Percentage of capacity remaining on this volume
|35 |schema.Volume.Manufacturer                       |str        |Volume manufacturer
|36 |schema.Volume.Model                              |str        |Model number of the volume
|37 |schema.Volume.Identifiers                        |list[dict] |Identifier of the volume
|38 |schema.Volume.Identifiers.DurableNameFormat      |str        |Durable name property format
|39 |schema.Volume.Identifiers.DurableName            |str        |Worldwide durable names for resources
|40 |schema.Drive                                     |dict       |Drive information
|41 |schema.Drive.PredictedMediaLifeLeftPercent       |float      |Percentage of reads and writes that are expected to be available on this drive
|42 |schema.Drive.CapacityBytes                       |int        |Size of this drive (bytes)
|43 |schema.Drive.CapableSpeedGbs                     |float      |The speed at which this drive communicates with storage in ideal conditions
|44 |schema.Drive.NegotiatedSpeedGbs                  |float      |The speed at which this drive currently communicates with storage
|45 |schema.Drive.HotspareType                        |str        |The type of hot spare this drive works with
|46 |schema.Drive.SerialNumber                        |str        |Drive serial number
|47 |schema.Drive.Manufacturer                        |str        |Drive manufacturer
|48 |schema.Drive.Model                               |str        |Model number of the drive
|49 |schema.Drive.Identifiers                         |list[dict] |Drive Identifier
|50 |schema.Drive.Identifiers.DurableNameFormat       |str        |Durable Name Property Format
|51 |schema.Drive.Identifiers.DurableName             |str        |Worldwide durable names for resources
|52 |schema.Drive.Status                              |dict       |Storage status information
|53 |schema.Drive.Status.State                        |str        |Resource state
|54 |schema.Drive.Status.Health                       |str        |Resource health state
|55 |schema.Drive.PowerState                          |str        |The current power state of the drive
|56 |schema.Drive.PowerCapability                     |bool       |Whether the power control function is enabled
|57 |link                                             |list[dict] |Device information for the CPU in relation to the drive
|58 |link.type                                        |str        |Device type (always CPU)
|59 |link.deviceID                                    |str        |OOB device ID
|60 |time                                             |str        |Date and time of information acquisition (UTC, ISO 8601 format)

### Spec Information: Network Interface

|No.|Key                                                                          |Type       |Value
|:-:|-----------------------------------------------------------------------------|-----------|-------------------------
| 1 |deviceID                                                                     |str        |OOB device ID
| 2 |type                                                                         |str        |Device type
| 3 |schema                                                                       |dict       |Network interface information
| 4 |schema.SerialInterfaces                                                      |dict       |Serial interface information
| 5 |schema.SerialInterfaces.BitRate                                              |str        |Serial interface data flow receive and transmit speed
| 6 |schema.Network                                                               |dict       |Network Information
| 7 |schema.Network.Controllers                                                   |list[dict] |Network controller information that configures the network adapter
| 8 |schema.Network.Controllers.ControllerCapabilities                            |dict       |Controller Functions
| 9 |schema.Network.Controllers.ControllerCapabilities.DataCenterBridging         |dict       |Data Center Bridging (DCB)
|10 |schema.Network.Controllers.ControllerCapabilities.DataCenterBridging.Capable |bool       |Whether the Data Center Bridging (DCB) is supported
|11 |schema.Network.Controllers.ControllerCapabilities.NetworkDeviceFunctionCount |int        |Maximum number of physical functions available
|12 |schema.Network.Controllers.ControllerCapabilities.NetworkPortCount           |int        |Number of physical ports
|13 |schema.Network.Controllers.ControllerCapabilities.NPAR                       |dict       |NIC Partitioning (NPAR) function
|14 |schema.Network.Controllers.ControllerCapabilities.NPAR.NparCapable           |bool       |Whether it supports partitioning of NIC functions
|15 |schema.Network.Controllers.ControllerCapabilities.NPAR.NparEnabled           |bool       |Whether NIC feature partitioning is active
|16 |schema.Network.Controllers.ControllerCapabilities.NPIV                       |dict       |N_PortID Virtualization (NPIV) Capabilities
|17 |schema.Network.Controllers.ControllerCapabilities.NPIV.MaxDeviceLogins       |int        |Maximum number of NPIV logins allowed from all ports at the same time
|18 |schema.Network.Controllers.ControllerCapabilities.NPIV.MaxPortLogins         |int        |Maximum number of NPIV logins allowed per physical port
|19 |schema.Network.Controllers.ControllerCapabilities.VirtualizationOffload      |dict       |Virtualization Offload
|20 |schema.Network.Controllers.ControllerCapabilities.VirtualizationOffload.VirtualFunction                        |dict  |Controller Virtual Functions
|21 |schema.Network.Controllers.ControllerCapabilities.VirtualizationOffload.VirtualFunction.DeviceMaxCount         |int   |Maximum number of virtual functions to support
|22 |schema.Network.Controllers.ControllerCapabilities.VirtualizationOffload.VirtualFunction.NetworkPortMaxCount    |int   |Maximum number of virtual functions supported per port
|23 |schema.Network.Controllers.ControllerCapabilities.VirtualizationOffload.VirtualFunction.MinAssignmentGroupSize |int   |Minimum number of virtual functions that can be assigned or moved
|24 |schema.Network.Controllers.ControllerCapabilities.VirtualizationOffload.SRIOV                                  |dict  |Single Root Input/Output Virtualization (SR-IOV) capability
|25 |schema.Network.Controllers.ControllerCapabilities.VirtualizationOffload.SRIOV.SRIOVVEPACapable                 |bool  |Whether to support SR-IOV in virtual VEPA mode
|26 |schema.Network.Controllers.FirmwarePackageVersion                            |str        |Firmware package version
|27 |schema.Network.Controllers.Identifiers                                       |list[dict] |Durable name of the network adapter controller
|28 |schema.Network.Controllers.Identifiers.DurableNameFormat                     |str        |Durable name property format
|29 |schema.Network.Controllers.Identifiers.DurableName                           |str        |Worldwide durable names for resources
|30 |schema.Network.Controllers.Location                                          |dict       |Controller Location
|31 |schema.Network.Controllers.Location.PartLocation                             |dict       |Location of parts of resources in the enclosure
|32 |schema.Network.Controllers.Location.PartLocation.ServiceLabel                |str        |Part Location Label
|33 |schema.Network.Controllers.Location.PartLocation.LocationType                |str        |Type of Component Location
|34 |schema.Network.Controllers.Location.PartLocation.LocationOrdinalValue        |int        |A number that represents the location of the part
|35 |schema.Network.Controllers.Location.PartLocation.Reference                   |str        |Reference point for part location
|36 |schema.Network.Controllers.Location.PartLocation.Orientation                 |str        |Order of slot enumeration used in LocationOrdinalValue
|37 |schema.Network.Controllers.PCIeInterface                                     |dict       |Learn more about the controller's PCIe interface
|38 |schema.Network.Controllers.PCIeInterface.LanesInUse                          |int        |Number of PCIe lanes used by this device
|39 |schema.Network.Controllers.PCIeInterface.MaxLanes                            |int        |Number of PCIe lanes this device supports
|40 |schema.Network.Controllers.PCIeInterface.PCIeType                            |str        |Version of PCIe specification used by this device
|41 |schema.Network.Controllers.PCIeInterface.MaxPCIeType                         |str        |PCIe supported by this device Latest version of the specification
|42 |schema.Network.SerialNumber                                                  |str        |Serial number of this network adapter
|43 |schema.Network.Manufacturer                                                  |str        |Manufacturer of this network adapter
|44 |schema.Network.Model                                                         |str        |Product model number of this network adapter
|45 |schema.Network.Status                                                        |dict       |Network status information
|46 |schema.Network.Status.State                                                  |str        |Resource state
|47 |schema.Network.Status.Health                                                 |str        |Resource health state
|48 |schema.Network.PowerState                                                    |str        |The current power state of the network function
|49 |schema.Network.PowerCapability                                               |bool       |Whether the power control function is enabled
|50 |schema.NetworkDeviceFunctions                                                |dict       |Network device capabilities
|51 |schema.NetworkDeviceFunctions.DeviceEnabled                                  |bool       |Whether this network device feature is enabled
|52 |schema.NetworkDeviceFunctions.Ethernet                                       |dict       |Ethernet capabilities, status and configuration values of the network devices
|53 |schema.NetworkDeviceFunctions.Ethernet.MACAddress                            |str        |Currently set MAC address
|54 |schema.NetworkDeviceFunctions.Ethernet.MTUSize                               |int        |Maximum Transmission Unit (MTU) Configured
|55 |schema.NetworkDeviceFunctions.Ethernet.MTUSizeMaximum                        |int        |Maximum Maximum Transmission Unit (MTU) Size Supported
|56 |schema.NetworkDeviceFunctions.Ethernet.PermanentMACAddress                   |str        |Permanent MAC address
|57 |schema.NetworkDeviceFunctions.Ethernet.VLAN                                  |dict       |VLAN information for this interface
|58 |schema.NetworkDeviceFunctions.Ethernet.VLAN.VLANEnable                       |bool       |Whether this VLAN is enabled
|59 |schema.NetworkDeviceFunctions.Ethernet.VLAN.VLANId                           |int        |VLAN ID
|60 |schema.NetworkDeviceFunctions.Limits                                         |list[dict] |Byte and Packet Limits for Network Device Capabilities
|61 |schema.NetworkDeviceFunctions.Limits.BurstBytesPerSecond                     |int        |Maximum number of bytes per second in a burst
|62 |schema.NetworkDeviceFunctions.Limits.BurstPacketsPerSecond                   |int        |Maximum number of packets per second in a burst
|63 |schema.NetworkDeviceFunctions.Limits.Direction                               |str        |The direction of the data to which this restriction applies
|64 |schema.NetworkDeviceFunctions.Limits.SustainedBytesPerSecond                 |int        |Maximum number of persistent bytes per second
|65 |schema.NetworkDeviceFunctions.Limits.SustainedPacketsPerSecond               |int        |Maximum number of persistent packets per second
|66 |schema.Port                                                                  |dict       |Port information
|67 |schema.Port.FunctionMaxBandwidth                                             |list[dict] |Maximum bandwidth allocation percentage for the feature associated with this port
|68 |schema.Port.FunctionMaxBandwidth.AllocationPercent                           |int        |Maximum bandwidth allocation percentage for network device capabilities
|69 |schema.Port.FunctionMinBandwidth                                             |list[dict] |Minimum bandwidth allocation percentage for the feature associated with this port
|70 |schema.Port.FunctionMinBandwidth.AllocationPercent                           |int        |Minimum bandwidth allocation percentage for network device functions
|71 |schema.Port.MaxSpeedGbps                                                     |float      |Maximum speed (Gbit/s) for this port that is currently configured
|72 |schema.Port.LinkConfiguration                                                |list[dict] |Link configuration for this port
|73 |schema.Port.LinkConfiguration.CapableLinkSpeedGbps                           |list[float]|A set of link speed features (Gbit/s) for this port
|74 |link                                                                         |list[dict] |Device information for the CPU in relation to the network adapter
|75 |link.type                                                                    |str        |Device type (always CPU)
|76 |link.deviceID                                                                |str        |OOB device ID
|77 |time                                                                         |str        |Date and time of information acquisition (UTC, ISO 8601 format)

### Spec Information: Graphics Controller

|No.|Key                          |Type       |Value
|:-:|-----------------------------|-----------|-------------------------------------------------------------------------
| 1 |deviceID                     |str        |OOB device ID
| 2 |type                         |str        |Device type
| 3 |schema                       |dict       |Graphics controller information
| 4 |schema.SchemaBiosVersion     |str        |Graphics controller BIOS or primary graphics controller firmware version
| 5 |schema.DriverVersion         |str        |Graphics controller driver version
| 6 |schema.SerialNumber          |str        |Graphics controller serial number
| 7 |schema.Manufacturer          |str        |Graphics controller manufacturer
| 8 |schema.Model                 |str        |Graphics controller product model number
| 9 |schema.Status                |dict       |Graphics controller status information
|10 |schema.Status.State          |str        |Resource state
|11 |schema.Status.Health         |str        |Resource health state  
|12 |time                         |str        |Date and time of information acquisition (UTC, ISO 8601 format)

## Table 5-5. Mapping from Spec Information to REST API Item Names

The correspondence between the specification information stored in the return value of `get_spec_info`
and the item name of the REST API of the HW control function is shown below.

- In the item name of the spec information, the key of the nested dictionary is represented by dot separation.
  For example, if the item name is `a.b.c`, the dictionary value is `dictionary ["a"]["b"]["c"]`.
- Similarly, the item names in the REST API are dotted with the property names of nested objects.

### Spec Information(Mapping): Processor

|No.|Spec information                                 |REST API
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

### Spec Information(Mapping): Memory

|No.|Spec information                           |REST API
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

### Spec Information(Mapping): Storage

|No.|Spec information                                 |REST API
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

### Spec Information(Mapping): Network Interface

|No.|Spec information                                                             |REST API
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

### Spec Information(Mapping): Graphics Controller

|No.|Spec information             |REST API
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

## Table 5-6. Return Value of `get_metric_info`

The return value of `get_metric_info` is a dictionary with the items in the table below.

|No.|Key         |Type       |Value
|:-:|------------|-----------|--------------------------------------------------
| 1 |devices     |list[dict] |A list of dictionaries containing device metric information

Each element of the list corresponds to each element of the parameter [`key_values`](#table-5-3-parameter-key_values)
and is a dictionary with a different entry for each [Device Type](#table-5-1-device-type).  
The following are dictionary entries for each device type.

- Dotted keys in nested dictionaries. For example, if the key is `a.b.c`, the dictionary value is `dictionary["a"]["b"]["c"]`.
- `deviceID`, `type`, and `time` are required. The other items are set if the information can be retrieved from the device.

### Metric Information: Processor

|No.|Key                                              |Type       |Value
|:-:|-------------------------------------------------|-----------|-----------------------------------------------------
| 1 |deviceID                                         |str        |OOB device ID
| 2 |type                                             |str        |Device type
| 3 |schema                                           |dict       |Processor information
| 4 |schema.Status                                    |dict       |Processor status information
| 5 |schema.Status.State                              |str        |Resource state
| 6 |schema.Status.Health                             |str        |Resource health state
| 7 |schema.PowerState                                |str        |The current power state of the processor
| 8 |schema.PowerCapability                           |bool       |Whether the power control function is enabled
| 9 |metric                                           |dict       |Metric information
|10 |metric.BandwidthPercent                          |float      |Processor bandwidth utilization (%)
|11 |metric.OperatingSpeedMHz                         |int        |Processor speed (MHz)
|12 |metric.LocalMemoryBandwidthBytes                 |int        |Local memory bandwidth usage (in bytes)
|13 |metric.RemoteMemoryBandwidthBytes                |int        |Remote memory bandwidth usage (in bytes)
|14 |metric.Cache                                     |list[dict] |Processor cache measurements
|15 |metric.Cache.CacheMiss                           |float      |Number of cash line misses in millions
|16 |metric.Cache.CacheMissesPerInstruction           |float      |Number of cache misses per instruction
|17 |metric.Cache.HitRatio                            |float      |Cash line hit ratio
|18 |metric.Cache.OccupancyBytes                      |int        |Total cache level footprint (in bytes)
|19 |metric.Cache.OccupancyPercent                    |float      |Total cache occupancy
|20 |metric.CoreMetrics                               |list[dict] |Processor core measurements
|21 |metric.CoreMetrics.CoreId                        |str        |Processor core identifier
|22 |metric.CoreMetrics.InstructionsPerCycle          |float      |Instructions per clock cycle for this core
|23 |metric.CoreMetrics.CoreCache                     |list[dict] |Cache measurements of cores in the processor
|24 |metric.CoreMetrics.CoreCache.OccupancyBytes      |int        |Total cache level footprint (in bytes)
|25 |metric.CoreMetrics.CoreCache.OccupancyPercent    |float      |Total cache occupancy
|26 |environment                                      |dict       |Energy consumption (J)
|27 |environment.Sensor                               |dict       |Sensor Information
|28 |environment.Sensor.SensorResetTime               |str        |Date and time when the time property was last reset (UTC, ISO 8601 format)
|29 |environment.Sensor.SensingInterval               |int        |Time interval between sensor readings (seconds)
|30 |environment.Sensor.ReadingTime                   |str        |Date and time when the measurement was taken from the sensor (UTC, ISO 8601 format)
|31 |environment.EnergyJoules                         |dict       |Energy consumption
|32 |environment.EnergyJoules.Reading                 |float      |Measured energy consumption (J)
|33 |time                                             |str        |Date and time of information acquisition (UTC, ISO 8601 format)

### Metric Information: Memory

|No.|Key                                              |Type       |Value
|:-:|-------------------------------------------------|-----------|-----------------------------------------------------
| 1 |deviceID                                         |str        |OOB device ID
| 2 |type                                             |str        |Device type
| 3 |schema                                           |dict       |Memory information
| 4 |schema.Enabled                                   |bool       |Whether memory is enabled
| 5 |schema.Status                                    |dict       |Memory status information
| 6 |schema.Status.State                              |str        |Resource state
| 7 |schema.Status.Health                             |str        |Resource health state
| 8 |schema.PowerState                                |str        |The current power state of the memory
| 9 |schema.PowerCapability                           |bool       |Whether the power control function is enabled
|10 |metric                                           |dict       |Metric information
|11 |metric.BandwidthPercent                          |float      |Memory Bandwidth Utilization (%)
|12 |metric.BlockSizeBytes                            |int        |Block size in bytes
|13 |metric.OperatingSpeedMHz                         |int        |Memory operating speed in MHz or MT/s, depending on need
|14 |metric.HealthData                                |dict       |Memory health information
|15 |metric.HealthData.DataLossDetected               |bool       |Whether data loss has been detected
|16 |metric.HealthData.LastShutdownSuccess            |bool       |Whether the last shutdown was successful
|17 |metric.HealthData.PerformanceDegraded            |bool       |Whether the performance was degraded?
|18 |metric.HealthData.PredictedMediaLifeLeftPercent  |float      |Percentage of media that is expected to be available for read/write Energy consumption (J)
|19 |environment                                      |dict       |Energy consumption (J)
|20 |environment.Sensor                               |dict       |Sensor information
|21 |environment.Sensor.SensorResetTime               |str        |Date and time when the time property was last reset (UTC, ISO 8601 format)
|22 |environment.Sensor.SensingInterval               |int        |Time interval between sensor readings (seconds)
|23 |environment.Sensor.ReadingTime                   |str        |Date and time when the measurement was taken from the sensor (UTC, ISO 8601 format)
|24 |environment.EnergyJoules                         |dict       |Energy consumption
|25 |environment.EnergyJoules.Reading                 |float      |Measured energy consumption (J)
|26 |time                                             |str        |Date and time of information acquisition (UTC, ISO 8601 format)

### Metric Information: Storage

|No.|Key                                              |Type       |Value
|:-:|-------------------------------------------------|-----------|-----------------------------------------------------
| 1 |deviceID                                         |str        |OOB device ID
| 2 |type                                             |str        |Device type
| 3 |schema                                           |dict       |Storage information
| 4 |schema.Volume                                    |dict       |Volume information
| 5 |schema.Volume.Capacity                           |dict       |Capacity information for this volume
| 6 |schema.Volume.Capacity.Data                      |dict       |Capacity information related to user data
| 7 |schema.Volume.Capacity.Data.AllocatedBytes       |int        |The number of bytes currently allocated by the storage
| 8 |schema.Volume.Capacity.Data.ConsumedBytes        |int        |Number of bytes consumed
| 9 |schema.Volume.Capacity.Data.GuaranteedBytes      |int        |Number of bytes guaranteed for storage
|10 |schema.Volume.Capacity.Data.ProvisionedBytes     |int        |Maximum number of bytes that can be allocated
|11 |schema.Volume.Capacity.Metadata                  |dict       |Capacity information related to metadata
|12 |schema.Volume.Capacity.Metadata.AllocatedBytes   |int        |The number of bytes currently allocated by the storage
|13 |schema.Volume.Capacity.Metadata.ConsumedBytes    |int        |Number of bytes consumed
|14 |schema.Volume.Capacity.Metadata.GuaranteedBytes  |int        |Number of bytes guaranteed for storage
|15 |schema.Volume.Capacity.Metadata.ProvisionedBytes |int        |Maximum number of bytes that can be allocated
|16 |schema.Volume.Capacity.Snapshot                  |dict       |Capacity information related to snapshot or backup data
|17 |schema.Volume.Capacity.Snapshot.AllocatedBytes   |int        |The number of bytes currently allocated by the storage
|18 |schema.Volume.Capacity.Snapshot.ConsumedBytes    |int        |Number of bytes consumed
|19 |schema.Volume.Capacity.Snapshot.GuaranteedBytes  |int        |Number of bytes guaranteed for storage
|20 |schema.Volume.Capacity.Snapshot.ProvisionedBytes |int        |Maximum number of bytes that can be allocated
|21 |schema.Volume.RemainingCapacityPercent           |int        |Percentage of capacity remaining on this volume
|22 |schema.Drive                                     |dict       |Drive information
|23 |schema.Drive.NegotiatedSpeedGbs                  |float      |The speed at which this drive currently communicates with storage
|24 |schema.Drive.Status                              |dict       |Storage status information
|25 |schema.Drive.Status.State                        |str        |Resource State
|26 |schema.Drive.Status.Health                       |str        |Resource health state
|27 |schema.Drive.PowerState                          |str        |The current power state of the drive
|28 |schema.Drive.PowerCapability                     |bool       |Whether the power control function is enabled
|29 |environment                                      |dict       |Energy consumption (J)
|30 |environment.Sensor                               |dict       |Sensor information
|31 |environment.Sensor.SensorResetTime               |str        |Date and time when the time property was last reset (UTC, ISO 8601 format)
|32 |environment.Sensor.SensingInterval               |int        |Time interval between sensor readings (seconds)
|33 |environment.Sensor.ReadingTime                   |str        |Date and time when the measurement was taken from the sensor (UTC, ISO 8601 format)
|34 |environment.EnergyJoules                         |dict       |Energy consumption
|35 |environment.EnergyJoules.Reading                 |float      |Measured energy consumption (J)
|36 |time                                             |str        |Date and time of information acquisition (UTC, ISO 8601 format)

### Metric Information: Network Interface

|No.|Kye                                                  |Type       |Value
|:-:|-----------------------------------------------------|-----------|-------------------------------------------------
| 1 |deviceID                                             |str        |OOB device ID
| 2 |type                                                 |str        |Device type
| 3 |schema                                               |dict       |Network interface information
| 4 |schema.NetworkDeviceFunctions                        |dict       |Network Device Capabilities
| 5 |schema.NetworkDeviceFunctions.DeviceEnabled          |bool       |Whether this network device feature is enabled
| 6 |schema.Network.Status                                |dict       |Network status information
| 7 |schema.Network.Status.State                          |str        |Resource State
| 8 |schema.Network.Status.Health                         |str        |Resource health state
| 9 |schema.Network.PowerState                            |str        |The current power state of the network function
|10 |schema.Network.PowerCapability                       |bool       |Whether the power control function is enabled
|11 |metric                                               |dict       |Metric information
|12 |metric.Network                                       |dict       |Network
|13 |metric.Network.CPUCorePercent                        |float      |Device CPU core utilization (%)
|14 |metric.Network.HostBusRXPercent                      |float      |Host bus such as PCIe, RX utilization rate (%)
|15 |metric.Network.HostBusTXPercent                      |float      |Host bus such as PCIe, TX utilization (%)
|16 |metric.NetworkDeviceFunctions                        |dict       |Network Device Capabilities
|17 |metric.NetworkDeviceFunctions.RXAvgQueueDepthPercent |float      |RX Average Queue Depth
|18 |metric.NetworkDeviceFunctions.TXAvgQueueDepthPercent |float      |TX Average Queue Depth
|19 |metric.NetworkDeviceFunctions.RXBytes                |int        |Total number of bytes received by the network function
|20 |metric.NetworkDeviceFunctions.RXFrames               |int        |Total number of frames received by the network function
|21 |metric.NetworkDeviceFunctions.TXBytes                |int        |Total number of bytes sent by the network function
|22 |metric.NetworkDeviceFunctions.TXFrames               |int        |Total number of frames transmitted by the network function
|23 |environment                                          |dict       |Energy consumption (J)
|24 |environment.Sensor                                   |dict       |Sensor Information
|25 |environment.Sensor.SensorResetTime                   |str        |Date and time when the time property was last reset (UTC, ISO 8601 format)
|26 |environment.Sensor.SensingInterval                   |int        |Time interval between sensor readings (seconds)
|27 |environment.Sensor.ReadingTime                       |str        |Date and time when the measurement was taken from the sensor (UTC, ISO 8601 format)
|28 |environment.EnergyJoules                             |dict       |Energy consumption
|29 |environment.EnergyJoules.Reading                     |float      |Measured energy consumption (J)
|30 |time                                                 |str        |Date and time of information acquisition (UTC, ISO 8601 format)

## Table 5-7. Mapping from Metric Information to REST API Item Names

### Metric Information(Mapping): Processor

|No.|Metric information                               |REST API
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

### Metric Information(Mapping): Memory

|No.|Metric information                               |REST API
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

### Metric Information(Mapping): Storage

|No.|Metric information                               |REST API
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

### Metric Information(Mapping): Network Interface

|No.|Metric information                                   |REST API
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

## Table 5-8. Return Value of `get_power_state`

The return value of `get_power_state` is a dictionary with the items in the table below.

|No.|Key         |Type       |Value
|:-:|------------|-----------|--------------------------------------------------
| 1 |devices     |list[dict] |A list of dictionaries containing the power states of the device

Each element of the list corresponds to each element of the parameter [`key_values`](#table-5-3-parameter-key_values).  
Here are the dictionary entries:

- `deviceID`, `type`, and `time` are required. Set the `powerState` if it can be obtained from the device.

|No.|Key                    |Type |Value
|:-:|-----------------------|-----|-------------------------------------------------------------------------------------
| 1 |deviceID               |str  |OOB device ID
| 2 |type                   |str  |Device type
| 3 |powerState             |str  |Power state (one of `On`, `Off`, `Paused`, `PoweringOff`, `PoweringOn` or `Unknown`)
| 4 |time                   |str  |Date and time of information acquisition (UTC, ISO 8601 format)

## Table 5-9. Return Value of Update Methods

The return value of the update method is a list of dictionaries with the items in the table below.

|No.|Key       |Type |Value
|:-:|----------|-----|----------------------------------------------------------
| 1 |deviceID  |str  |OOB device ID
| 2 |type      |str  |Device type
| 3 |status    |int  |HTTP response status codes for REST APIs
| 4 |time      |str  |Date and time of operation (UTC, ISO 8601 format)
