# Install CDIM

## 1. Prerequisites

### 1.1. About Docker proxy settings

> [!WARNING]  
> Do not use the method of creating or editing the `~/.docker/config.json` file as introduced in the official Docker documentation.  
> https://docs.docker.com/engine/cli/proxy/#configure-the-docker-client  
> The proxy settings from the above method will apply during builds and to all running containers, causing communication issues with the Dapr sidecar.

#### 1.1.1. Proxy settings for docker image pull  

Recommend using the method described in the official Docker documentation to set up under ``~/.config/systemd/user/docker.service.d/``.
https://docs.docker.com/engine/daemon/proxy/#environment-variables

#### 1.1.2. Proxy settings docker image build

Configuration using compose.override.yml is recommended.  
The targets are as follows.

| compose recipes                       | docker services               |
| ------------------------------------- | ----------------------------- |
| base-compose                          | message-broker-setting        |
| configuration-exporter-compose        | configuration-exporter        |
| configuration-manager-compose         | configuration-manager         |
| hw-control-compose                    | hw-control                    |
| job-manager-compose                   | job-manager-setup             |
| layout-apply-compose                  | layout-apply                  |
| migration-procedure-generator-compose | migration-procedure-generator |
| performance-collector-compose         | performance-collector         |
| performance-exporter-compose          | performance-exporter          |
| set-up-tools                          | gateway-set-up-tools          |

## 2. Retrieve the Installer

First, retrieve the CDIM installer from the repository:

```sh
git clone https://github.com/project-cdim/installer.git
```

Navigate to the installer directory and run the `pre_install` script to download the necessary components:

```sh
cd installer
./pre_install
```

Check to ensure that the repositories for each component are correctly cloned.
Each cloned directories (such as base-compose) must be retained in the environment and not deleted.

```text
installer
 ├ alert-manager-compose
 ├ base-compose
 ├ configuration-exporter-compose
 ├ configuration-manager-compose
 ├ hw-control-compose
 ├ job-manager-compose
 ├ layout-apply-compose
 ├ mf-core
 ├ mf-layout
 ├ mf-resource
 ├ mf-user
 ├ migration-procedure-generator-compose
 ├ performance-collector-compose
 ├ performance-exporter-compose
 ├ performance-manager-compose
 └ set-up-tools
```

## 3. Modify the Configuration Files

> [!NOTE]
> In the procedures of this chapter, the current directory will be the `installer` of the installer that was cloned in the previous steps.

### 3.1. Frontend Configuration

#### 3.1.1. Create Configuration File

Navigate to the `mf-core` directory:

```sh
cd mf-core
```

Create a new `.env` configuration file by copying the sample provided:

```sh
cp .env.example .env
```

#### 3.1.2. Edit Configuration File

Open the `.env` file and update it according to your specific environment settings.

Here’s an example of what might be modified:
Adjust the `cdim-server` address to point to your Docker server's hostname or IP address.
It also needs to be a hostname or IP address that can be accessed externally,
as it will be the connection destination for the browser.

```ini: .env
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
NEXT_PUBLIC_URL_BE_LAYOUT_APPLY  = 'http://cdim-server:8014/cdim/api/v1/layout-apply'
# API endpoint for constraint management backend
NEXT_PUBLIC_URL_BE_POLICY_MANAGER = 'http://cdim-server:8014/cdim/api/v1/policy-manager'
# API endpoint for configuration information management backend
NEXT_PUBLIC_URL_BE_CONFIGURATION_MANAGER = 'http://cdim-server:8014/cdim/api/v1/configuration-manager'
# API endpoint for performance information management backend (VictoriaMetrics)
NEXT_PUBLIC_URL_BE_PERFORMANCE_MANAGER = 'http://cdim-server:8014/cdim/api/v1/performance-manager'
```

If you want to replace it with the FQDN of the server where Docker is installed, you can change it with the following command.

```sh
sed -e "/^NEXT_PUBLIC/s/localhost/$(hostname -f)/g" .env.example > .env
```

### 3.2. Job Management Configuration

Adjust backend settings if necessary. You may need to modify hardware information retrieval intervals to match your operational environment.

Navigate to the following configuration and make the desired changes:

```sh
job-manager-compose/job-manager-setup/HW_configuration_information_data_linkage_job.yaml
```

Modify the "time" in schedule.
Here is an example of adjusting it to 5 minutes.

```yaml
- defaultTab: nodes
  description: ''
  executionEnabled: true
  id: 9d6fd442-71e3-412d-be58-17487269787a
  loglevel: INFO
  name: HW configuration information data linkage job
  nodeFilterEditable: false
  plugins:
    ExecutionLifecycle: null
  schedule:
    dayofmonth:
      day: '*'
    month: '*'
    time:
      hour: '*'
      minute: '0/5'
      seconds: '0'
    year: '*'
```

## 4. Start the Containers

After configurations are set, use the `install` script to build and initialize the containers:

```sh
./install --up
```

This will start the CDIM environment. Verify that all services are running correctly before proceeding.

[Next step: Perform Initial Setup of CDIM](../setup/setup.md)
