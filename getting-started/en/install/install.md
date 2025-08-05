# Install CDIM

## 1. Prerequisites

Ensure you have the following installed:

- Docker
- Git

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

## 3. Modify the Configuration Files

Adjust configuration files to suit your installation environment.

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

Open the `.env` file and update it according to your specific environment settings. Adjust the `cdim-server` address to point to your Docker server's hostname or IP address.

Here’s an example of what might be modified:

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

Return to the repository root directory.

```sh
cd ..
```

### 3.2. Backend Configuration

Adjust backend settings if necessary. You may need to modify hardware information retrieval intervals to match your operational environment.

Navigate to the following configuration and make the desired changes:

```sh
configuration-collector-compose/configuration-collector/configuration-collector/config/collect.yaml
```

Modify the "interval" and "timeout" values under `hw_collect_configs`. Here is an example modification setting the interval to 120 seconds:

```yaml
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

After configurations are set, use the `install` script to build and initialize the containers:

```sh
./install --up
```

This will start the CDIM environment. Verify that all services are running correctly before proceeding.

[Next step: Perform Initial Setup of CDIM](../setup/setup.md)
