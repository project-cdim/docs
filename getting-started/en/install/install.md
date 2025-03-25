# Install CDIM

## 1. Prerequisites

- Docker
- Git

## 2. Retrieve the Installer

Retrieve the installer:

```sh
git clone https://github.com/project-cdim/installer.git
```

Execute the `pre_install` script to obtain the necessary components.

```sh
cd installer
./pre_install
```

Verify that the repositories for each component have been cloned.

## 3. Modify the Configuration Files

### 3.1. Frontend

#### 3.1.1. Create Configuration File

Navigate to the mf-core component.

```sh
cd mf-core
```

Create a configuration file `.env` based on the sample file `.env.sample`.

```sh
cp .env.sample .env
```

#### 3.1.2. Modify Configuration File

Modify the `.env` file according to your environment. Typically, change `cdim-server` to the hostname or IP address of the server where Docker is installed.

Below is an excerpt of the sections to modify.

```sh: .env
# Micro frontend URL settings
NEXT_PUBLIC_URL_CORE      = 'http://cdim-server:3000'
NEXT_PUBLIC_URL_RESOURCE  = 'http://cdim-server:3003'
NEXT_PUBLIC_URL_LAYOUT    = 'http://cdim-server:3004'
NEXT_PUBLIC_URL_USER      = 'http://cdim-server:3005'

# URL of the authentication server
NEXT_PUBLIC_URL_IDP        = 'http://cdim-server:8287'

# API endpoint for configuration design backend
NEXT_PUBLIC_URL_BE_LAYOUT_DESIGN = 'http://cdim-server:8014/cdim/api/v1/layout-design'
# API endpoint for configuration apply backend
NEXT_PUBLIC_URL_BE_LAYOUT_APPLY = 'http://cdim-server:8014/cdim/api/v1/layout-apply'
# API endpoint for constraint management backend
NEXT_PUBLIC_URL_BE_POLICY_MANAGER = 'http://cdim-server:8014/cdim/api/v1/policy-manager'
# API endpoint for configuration information management backend
NEXT_PUBLIC_URL_BE_CONFIGURATION_MANAGER = 'http://cdim-server:8014/cdim/api/v1/configuration-manager'
# API endpoint for performance information management backend (VictoriaMetrics)
NEXT_PUBLIC_URL_BE_PERFORMANCE_MANAGER = 'http://cdim-server:8014/cdim/api/v1/performance-manager'
```

### 3.2. Configuration Information

The following modifications are unnecessary if no changes are required.

By modifying the following file, you can adjust the HW information retrieval interval to suit your environment.

```sh
configuration-collector-compose/configuration-collector/configuration-collector/config/collect.yaml
```

Modify the "interval" and "timeout" values under hw_collect_configs. Below is an example modified to 120 seconds.

```sh
global:
  max_jobs: 200
  job_interval: 600
  job_timeout: 600
hw_collect_configs:
  - job_name: 'Hardware-Sync'
    interval: 120
    timeout: 120
    collect:
      url: 'http://configuration-exporter:8080/cdim/api/v1/devices'
    forwarding:
      url: 'http://configuration-manager:8080/cdim/api/v1/devices'
```

## 4. Start the Containers

Execute the `install` script to build and start the containers.

```sh
./install --up
```

[Next step: Perform Initial Setup of CDIM](../setup/setup.md)
