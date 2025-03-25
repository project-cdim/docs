# Concepts

## Our goal

In recent years, hardware known as Composable Disaggregated Infrastructure (hereinafter referred to as CDI) is being released by various hardware vendors. This hardware allows for the dynamic reconfiguration of connections between servers (CPU nodes) and devices such as Memory (CXL Memory), GPUs, FPGAs, and NVMe SSDs through PCI Express/CXL switches. By using CDI to appropriately configure, reconfigure, and dismantle nodes according to workload conditions, it is expected that hardware can be utilized efficiently.

However, in large-scale environments where CDI configuration resources (such as CPU, Memory, GPU, FPGA, NVMe SSD, etc.) reach hundreds or thousands, instant configuration control of these complex computing resources and their automated management becomes a challenge.

To address this challenge, the ultimate goal is to provide a common platform through a Composable Disaggregated Infrastructure Manager (hereinafter referred to as CDIM). This platform would enable the automatic design and reconfiguration of an optimal system structure for workloads, independent of the implementation of clients in the upper layer and hardware or fabric in the lower layer.

![OverviewOurGoal][]

## Our scope

To achieve the ultimate goal of the CDIM, we anticipate the need for the following major functionalities. These functionalities will be implemented in this project to achieve our final objectives:

1. An interface capable of integrative/common management of heterogeneous hardware.
2. A framework for the automatic design and implementation of node configurations optimized for workloads.
3. Integrated system control that includes existing software such as OpenStack and Kubernetes.

As of now, the range of what is being offered extends only to the functionality for "an interface capable of integrative/common management of heterogeneous hardware." For more information on the roadmap for other functionalities, please refer to the [Roadmap][].

## Architecture

The current architecture is as shown in the diagram below.
Based on this architecture, we will add components and interface specifications to implement the unimplemented functionalities described in [Our scope][].

![ModuleDiagram][]

The functionalities described in blue are provided by CDIM, and those in orange use other OSS. Additionally, although not represented in the diagram, Dapr is used for integration between services.

The descriptions for each functionality are as follows:

> [!NOTE] The individual devices that constitute the CDI are referred to as "resource," and the computational execution platform created by combining these resources is referred to as a "compute node".

### Base services

| Function name | Repository | Description |
|--|--|--|
| Gateway(Kong) | [base-compose][] | API gateway for the APIs provided by the backend service. Kong is used for the implementation. |
| IAM(Keycloak) | [base-compose][] | Authentication and authorization features. Keycroak is used for the implementation. |

### Frontend services

| Function name | Repository | Description |
|--|--|--|
| Main UI | [mf-core][] | Main Web UI screen | 
| Resource management UI | [mf-resource][] | Web UI screen for checking the list and detailed information of resources |
| Lauout management UI | [mf-layout][] | Web UI screen for checking and modifying the layout of compute nodes |
| User management UI | [mf-user][] | Web UI Screen for managing users (such as adding or deleting users) |
| UI shared modules | [mf-shared-modules][] | Common modules for the Web UI |

### Backend services

#### Configuration management services

| Function name | Repository | Description |
|--|--|--|
| Configuration manager | [configuration-manager][] | Manages configuration information and status of resources and compute nodes in a database |
| Configuration collector | [configuration-collector][] | Collects configuration information and status of resources and compute nodes |
| Configuration exporter | [configuration-exporter][] | Exporter for resource and compute node configuration information and status |

#### Layout apply services

| Function name | Repository | Description |
|--|--|--|
| Layout apply | [layout-apply][] | Receives requests to apply new compute node layout and controls resources through hw-control |
| Migration procedure generator | [migration-procedure-generator][] | Generates resource control procedures for migrating from the current compute node layout to a new one |

#### Performance management services

| Function name | Repository | Description |
|--|--|--|
| Performance manager(VictriaMetrics) | [performance-manager-compose][] | Manages performance information of resources and compute nodes using VictoriaMetrics |
| Performance collector | [performance-collector][] | Collects performance information of resources and compute nodes and works in conjunction with Configuration manager. Prometheus is used for the implementation. |
| Performance exporter| [performance-exporter][] | Prometheus exporter for the performance information of resources and compute nodes |

#### Hardware control services

| Function name | Repository | Description |
|--|--|--|
| Hardware control | [hw-control][] | Controls operations such as retrieving resource information, powering resources on/off, and connecting/disconnecting resources |

##### Reference hardware plugins

| Function name | Repository | Description |
|--|--|--|
| Reference Fabric Manager Plugin | [fm-plugin-reference][] | Reference implementation plugin for Fabric Manager |
| Reference Out-of-Band Plugin | [oob-plugin-reference][] | Reference implementation plugin for Out-of-Band management |

### Refernce hardware emulator

| Function name | Repository | Description |
|--|--|--|
| Reference hadrware emulator | [hw-emulator-reference][] | Hardware emulator that emulates the Redfish interface |

<!-- Link informations  -->

[OverviewOurGoal]: imgs/overview_our_goal.png
[Roadmap]: ../../roadmap/en/README.md
[Our scope]: #our-scope
[ModuleDiagram]: imgs/architecture.png

[base-compose]: https://github.com/project-cdim/base-compose

[mf-core]: https://github.com/project-cdim/mf-core
[mf-resource]: https://github.com/project-cdim/mf-resource
[mf-layout]: https://github.com/project-cdim/mf-layout
[mf-user]: https://github.com/project-cdim/mf-user
[mf-shared-modules]: https://github.com/project-cdim/mf-shared-modules

[configuration-manager]: https://github.com/project-cdim/configuration-manager
[configuration-collector]: https://github.com/project-cdim/configuration-collector
[configuration-exporter]: https://github.com/project-cdim/configuration-exporter

[layout-apply]: https://github.com/project-cdim/layout-apply
[migration-procedure-generator]: https://github.com/project-cdim/migration-procedure-generator

[performance-manager-compose]: https://github.com/project-cdim/performance-manager-compose
[performance-collector]: https://github.com/project-cdim/performance-collector
[performance-exporter]: https://github.com/project-cdim/performance-exporter

[hw-control]: https://github.com/project-cdim/hw-control
[fm-plugin-reference]: https://github.com/project-cdim/fm-plugin-reference
[oob-plugin-reference]: https://github.com/project-cdim/oob-plugin-reference

[hw-emulator-reference]: https://github.com/project-cdim/hw-emulator-reference
