### Troubleshooting <!-- omit in toc -->
This section explains troubleshooting for the Composable Disaggregated Infrastructure Manager (CDIM).
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
Please refer to the [Getting started](../../../../getting-started/en/setup/setup.md#2-frontend) procedure.  
You can check and change CDIM authentication information by logging in from the Keycloak management URL.  
The default login information is as follows:
```
URL: http://<ip-address>:8287
User: admin
Password: admin
```

#### 2. Network Error Displayed on Dashboard Screen

##### If 401 Error is Displayed
There may be an issue with the authentication settings. The client name needs to be consistent across the following three:
- Keycloak client
- mf-core .env NEXT_PUBLIC_AUTH_CLIENT_ID
- Kong settings 
Regarding Kong settings, ensure that the format of the public_key in the set-up-tools directory is correct and that the key content matches the public key of CDIM.  
If there are any errors, correct them and then perform [Initialize Kong Settings](#initialize-kong-settings) followed by [set-up-tools configuration](../../../../getting-started/en/setup/setup.md#12-initial-setup-for-gateway).

##### If Network Error is Displayed
It is possible that Kong cannot be connected and a 404 error is displayed.  
Check if there are any proxy settings or routing settings in the network of the created Docker container.  
If there are proxy settings within the container, it may not function properly.

##### If 500 Error is Displayed  
It is possible that Kong cannot connect with other components.  
Check if there are any proxy settings or routing settings in the created Docker container.  
If there are proxy settings within the container, it may not function properly.

##### If 502 Error is Displayed
Please restart Kong using the following command:
```sh
$ cd ~/cdim/base-compose
$ docker-compose down
$ docker-compose up -d --build
```

##### Initialize Kong Settings
Delete and recreate the volume containing Kong settings using the following command:

```sh
$ cd ~/cdim/base-compose
$ docker-compose down
$ docker volume ls
$ docker volume rm base_gateway-db
$ docker-compose up -d --build
```

#### 3. Cannot Connect to CDIM Dashboard/Dashboard Screen is Blank
Please check the mf-core/.env file.  
Ensure that the IP address and port number match the container information.  
```sh
How to check container information
$ docker ps
How to check IP address
$ ip address [| grep ens]
```

#### 4. Restart a Specific Component
This section shows how to restart individual components.  
If you need to restart all components, refer to [Initialize CDIM](#5-initialize-cdim).  
```sh
Move to the directory of the component you want to restart and stop the container
$ cd ~/cdim/base-compose
$ docker compose down
Once the container stop is confirmed, restart the container
$ docker compose up -d --build
```

#### 5. Initialize CDIM
This section explains how to initialize CDIM.  
Please be careful when executing the following commands as they will stop and delete all Docker containers.  
```sh
Stop and delete all containers
$ docker down $( docker ps -q )
$ docker rm $( docker ps -aq )
Delete all container images and volumes
$ docker image rm $( docker image ls -q )
$ docker volume rm $( docker volume ls -q )
Start containers
$ cd ~/cdim
$ ./install --up
```
