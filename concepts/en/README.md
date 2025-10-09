# Concepts

## Our Goal

In recent years, a variety of hardware vendors have introduced Composable Disaggregated Infrastructure (CDI). This technology enables dynamic reconfiguration of connections between servers (CPU nodes) and various devices like Memory (CXL Memory), GPUs, FPGAs, and NVMe SSDs via PCI Express/CXL switches. Leveraging CDI, it is possible to efficiently configure, reconfigure, and dismantle nodes based on workload demands, thus optimizing hardware utilization.

However, managing hundreds or thousands of CDI configuration resources (such as CPUs, Memory, GPUs, FPGAs, NVMe SSDs) in large-scale environments poses significant challenges for instant configuration control and automation.

To overcome these challenges, our ultimate goal is to deliver a unified platform through Composable Disaggregated Infrastructure Manager (CDIM). This platform aims to automatically design and reconfigure an optimal system architecture for various workloads, operating independently of the client implementations at the upper layer and the hardware or fabric at the lower layer.

![OverviewOurGoal][]

## Our Scope

To realize CDIM's ultimate goal, we envision necessary functionalities. These functionalities, which we aim to implement in this project to fulfill our objectives, are:

1. An interface for integrated/common management of heterogeneous hardware.
2. A framework for the automatic design and implementation of node configurations optimized for workloads.
3. Integrated system control that includes existing software such as OpenStack and Kubernetes.

Currently, we only provide the functionality for "an interface for integrated/common management of heterogeneous hardware." For more details on the roadmap for additional functionalities, please refer to our [Roadmap][].

## Architecture

The diagram below represents the current architecture.
Based on this, we will further develop components and interface specifications to incorporate the as-yet unimplemented functionalities outlined in [Our Scope][].

![ModuleDiagram][]

Features implemented by CDIM are colored blue, and those relying on other OSS are marked in orange. Additionally, while not shown in the diagram, Dapr is utilized for service integration.

Function descriptions are as follows:

> [!NOTE]
> In CDI terminology, individual devices are called "resources," and the computational execution platform formed by combining these resources is called a "compute node."

### Base Services

| Function Name     | Repository        | Description                                  |
|--|--|--|
| Gateway (Kong)    | [base-compose][]  | API gateway for backend services using Kong. |
| IAM (Keycloak)    | [base-compose][]  | Provides authentication and authorization features, implemented using Keycloak. |

### Frontend Services

| Function Name         | Repository        | Description                              |
|--|--|--|
| Main UI               | [mf-core][]       | Main web user interface.                 |
| Resource Management UI| [mf-resource][]   | Web interface for resource details and listings. |
| Layout Management UI  | [mf-layout][]     | Web interface for modifying and viewing compute node layouts. |
| User Management UI    | [mf-user][]       | Web interface for user management (e.g., adding or removing users). |
| UI Shared Modules     | [mf-shared-modules][] | Common modules for web interfaces.     |

### Backend Services

#### Configuration Management Services

| Function Name            | Repository                     | Description                                              |
|--|--|--|
| Configuration Manager    | [configuration-manager][]      | Manages configuration data and status for resources and compute nodes in a database. |
| Configuration Exporter  | [configuration-exporter][]     | Exports configuration data and status for resources and compute nodes. |

#### Alert Management Services

| Function Name | Repository | Description |
|--|--|--|
| Alert Manager | [alert-manager-compose][] | Manage alert information such as hardware errors. |

#### Job Management Services

| Function Name | Repository | Description |
|--|--|--|
| Job Manager | [job-manager-compose][] | Automatically executes pre-registered jobs according to the set schedule. By default, it runs two jobs: an information collection job from the Configuration Exporter and a housekeeping job for the Alert Manager. |

#### Layout Apply Services

| Function Name                | Repository                  | Description                                                  |
|--|--|--|
| Layout Apply                 | [layout-apply][]            | Processes requests to apply new compute node layouts and controls resources via hw-control. |
| Migration Procedure Generator| [migration-procedure-generator][] | Creates resource control procedures for transitioning to new compute node layouts. |

#### Performance Management Services

| Function Name                 | Repository                        | Description                                              |
|--|--|--|
| Performance Manager (VictoriaMetrics) | [performance-manager-compose][] | Manages performance data for resources and compute nodes using VictoriaMetrics. |
| Performance Collector         | [performance-collector][]         | Collects performance data in conjunction with Configuration Manager. Prometheus is used for implementation. |
| Performance Exporter          | [performance-exporter][]          | Exports performance data for resources and compute nodes. |

#### Hardware Control Services

| Function Name         | Repository        | Description                                   |
|--|--|--|
| Hardware Control      | [hw-control][]    | Manages operations such as retrieving resource information, powering on/off resources, and connecting/disconnecting resources. |

##### Reference Hardware Plugins

| Function Name                  | Repository              | Description                                                    |
|--|--|--|
| Reference Fabric Manager Plugin| [fm-plugin-reference][] | Reference implementation for a Fabric Manager plugin.           |
| Reference Out-of-Band Plugin   | [oob-plugin-reference][]| Reference implementation for an Out-of-Band management plugin. |

### Reference Hardware Emulator

| Function Name                 | Repository                  | Description                                         |
|--|--|--|
| Reference Hardware Emulator  | [hw-emulator-reference][]   | Emulates the Redfish interface for hardware.        |

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
[configuration-exporter]: https://github.com/project-cdim/configuration-exporter

[alert-manager-compose]: https://github.com/project-cdim/alert-manager-compose
[job-manager-compose]: https://github.com/project-cdim/job-manager-compose

[layout-apply]: https://github.com/project-cdim/layout-apply
[migration-procedure-generator]: https://github.com/project-cdim/migration-procedure-generator

[performance-manager-compose]: https://github.com/project-cdim/performance-manager-compose
[performance-collector]: https://github.com/project-cdim/performance-collector
[performance-exporter]: https://github.com/project-cdim/performance-exporter

[hw-control]: https://github.com/project-cdim/hw-control
[fm-plugin-reference]: https://github.com/project-cdim/fm-plugin-reference
[oob-plugin-reference]: https://github.com/project-cdim/oob-plugin-reference

[hw-emulator-reference]: https://github.com/project-cdim/hw-emulator-reference
