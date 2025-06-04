### Troubleshooting <!-- omit in toc -->
This section provides troubleshooting guidance for Composable Disaggregated Infrastructure Manager (CDIM).
- [1. Forgot CDIM Password/Cannot Access CDIM](#1-forgot-cdim-passwordcannot-access-cdim)
- [2. Network Error Displayed on Dashboard Screen](#2-network-error-displayed-on-dashboard-screen)
  - [If 401 Error is Displayed](#if-401-error-is-displayed)
  - [If Network Error is Displayed](#if-network-error-is-displayed)
  - [If 500 Error is Displayed](#if-500-error-is-displayed)
  - [If 502 Error is Displayed](#if-502-error-is-displayed)
  - [Initialize Kong Settings](#initialize-kong-settings)
- [3. Cannot Connect to CDIM Dashboard/Dashboard Screen is Blank](#3-cannot-connect-to-cdim-dashboarddashboard-screen-is-blank)
- [4. Restart a Specific Component](#4-restart-a-specific-component)
- [5. Initialize CDIM](#5-initialize-cdim)

#### 1. Forgot CDIM Password/Cannot Access CDIM
Refer to the [Getting started](../../../../getting-started/en/setup/setup.md#2-frontend) procedure for recovering or resetting CDIM authentication details.  
Default login credentials are:
```
URL: http://<ip-address>:8287
User: admin
Password: admin
```

#### 2. Network Error Displayed on Dashboard Screen

##### If 401 Error is Displayed
This error might be due to inconsistencies in authentication settings. Ensure uniformity in client names across:
- Keycloak client
- mf-core `.env` value `NEXT_PUBLIC_AUTH_CLIENT_ID`
- Kong configuration

Check the `public_key` format in the set-up-tools directory, ensuring it matches the public key for CDIM. Rectify any discrepancies, then perform [Initialize Kong Settings](#initialize-kong-settings) followed by [set-up-tools configuration](../../../../getting-started/en/setup/setup.md#12-initial-setup-for-gateway).

##### If Network Error is Displayed
Kong might be unreachable, indicated by a 404 error. Verify any proxy or routing settings of the Docker container's network. Inappropriate proxy settings could impair functionality.

##### If 500 Error is Displayed
Kong might be unable to connect with other components. Again, check for improper proxy or routing settings in the network configuration of the Docker container.

##### If 502 Error is Displayed
Restart Kong with the following commands:
```sh
$ cd ~/cdim/base-compose
$ docker-compose down
$ docker-compose up -d --build
```

##### Initialize Kong Settings
Reset Kong configuration by deleting and recreating the related volume:
```sh
$ cd ~/cdim/base-compose
$ docker-compose down
$ docker volume ls
$ docker volume rm base-compose_gateway-db
$ docker-compose up -d --build
```

#### 3. Cannot Connect to CDIM Dashboard/Dashboard Screen is Blank
Verify the `mf-core/.env` file for correct IP address and port number corresponding to the container details:
```sh
# Checking container information
$ docker ps
# Checking IP address
$ ip address [| grep ens]
```

#### 4. Restart a Specific Component
To restart individual components:
```sh
# Move to the component directory and stop the container
$ cd ~/cdim/base-compose
$ docker compose down
# Restart the container once it stops
$ docker compose up -d --build
```
For a full restart, refer to [Initialize CDIM](#5-initialize-cdim).

#### 5. Initialize CDIM
Resetting CDIM involves stopping and deleting all Docker containers, images, and volumes. Execute the following with caution:
```sh
# Stop and delete all containers
$ docker stop $(docker ps -q)
$ docker rm $(docker ps -aq)
# Delete all images and volumes
$ docker image rm $(docker image ls -q)
$ docker volume rm $(docker volume ls -q)
# Start containers
$ cd ~/cdim
$ ./install --up
```
