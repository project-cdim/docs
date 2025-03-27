### 3. Various Configuration Methods <!-- omit in toc -->
This section explains various configuration methods for the Composable Disaggregated Infrastructure Manager (CDIM).

- [3.1. Check and Change Log Output Methods](#31-check-and-change-log-output-methods)
  - [3.1.1. Check Logs](#311-check-logs)
  - [3.1.2. Change Log Output Methods](#312-change-log-output-methods)
- [3.2. Change Information Collection Settings](#32-change-information-collection-settings)
- [3.3. Change User Authentication Methods and Permissions](#33-change-user-authentication-methods-and-permissions)
  - [3.3.1. Add Users](#331-add-users)
  - [3.3.2. Change User Permissions in CDIM](#332-change-user-permissions-in-cdim)
  - [3.3.3. Register and Change User Authentication Methods](#333-register-and-change-user-authentication-methods)
    - [3.3.3.1. Password Authentication Settings](#3331-password-authentication-settings)

#### 3.1. Check and Change Log Output Methods 
##### 3.1.1. Check Logs
By default, logs are output to the following location. They are output within the container, so be careful with saving them.
```sh
$ docker exec -it <container-name> /bin/sh
$ ls /var/log/cdim
```
Logs are separated by component into the following files:

| Log Type | Log File Name |
|:--|:--|
| Audit Log | trail.log |
| Application Log (Hardware Control) | app_hw_control.log |
| Application Log (Layout Application) | app_layout_apply.log |
| Application Log (Migration Procedure Generation) | app_migration_procedures.log |
| Application Log (Configuration Information Management) | app_config_info.log |

##### 3.1.2. Change Log Output Methods
Change the settings file for each component to modify the log output method. The settings files are as follows:

| Component Name | Settings File Name | File Path |
|:--|:--|:--|
| Audit Log (Performance Information Collection) | main.go | performance-collector-compose/performance-collector/performance-collector |
| Audit Log (Performance Information Exporter) | main.go | performance-exporter-compose/performance-exporter/performance-exporter |
| Audit Log (Configuration Information Collection) | run_collect.go | configuration-collector-compose/configuration-collector/configuration-collector/cmd |
| Audit Log (Configuration Information Exporter) | main.go | configuration-exporter-compose/configuration-exporter/configuration-exporter |
| Audit Log (Configuration Information Management) | main.go | configuration-manager-compose/configuration-manager/configuration-manager |
| Hardware Control | setting.py | hw-control-compose/hw-control/src/app/common |
| Layout Application | layoutapply_config.yaml | layout-apply-compose/layout-apply/src/layoutapply/config |
| Migration Procedure Generation | migrationprocedures_config.yaml | migration-procedure-generator-compose/migration-procedure-generator/src/migrationproceduregenerator/config |
| Performance Information Collection | logger.go | performance-collector-compose/performance-collector/performance-collector/internal/service |
| Performance Information Exporter | logger.go | performance-exporter-compose/performance-exporter/performance-exporter/internal/service |
| Configuration Information Collection | collect_logger.go | configuration-collector-compose/configuration-collector/configuration-collector/service |
| Configuration Information Exporter | controller_common.go | configuration-exporter-compose/configuration-exporter/configuration-exporter/controller |
| Configuration Information Management | gi_cm_applog.go | configuration-manager-compose/configuration-manager/configuration-manager/common |

The settings for log output files are as follows. For settings files in Go format, write the following items in the code.
| Setting Item | Description |
|:--|:--|
| tag | Tag representing the component |
| log_dir | Log output directory |
| log_file | Log file name |
| logging_level | Logging level. Logs above the set level are output |
| rotation_size | File size (bytes) for log rotation |
| backup_files | Number of backup files to retain through rotation |
| stdout | If true, logs are also output to standard output |

After changing the output method, you need to restart the component. Please follow [this procedure](../appendix/troubleshooting/README.md#4-restart-a-specific-component) to restart.

> [!NOTE]
> If the component does not run after changing the log output directory, you may need to create the directory. In that case, modify the Dockerfile to create the log output directory as well.

#### 3.2. Change Information Collection Settings 
You can change the collection interval and other settings by modifying the settings file for each collection component.

Configuration Information Collection: configuration-collector-compose/configuration-collector/configuration-collector/config/collect.yaml

```yaml
hw_collect_configs:
  - job_name: 'Hardware-Sync'
    interval: 90   # Configuration information retrieval interval (s)
    timeout: 90    # Configuration information timeout value (s)
```
After changing the collection method, you need to restart the component.  
Please follow [this procedure](../appendix/troubleshooting/README.md#4-restart-a-specific-component) to restart.

Performance Information Collection: performance-collector-compose/share/prometheus.yml

```yaml
global:
    evaluation_interval: 60s  # Performance information retrieval interval (s)
    scrape_interval: 60s      # Performance information timeout value (s)
```

For performance information collection, you need to re-execute the information collection.
```sh
$ docker exec -it performance-collector /bin/sh
$ curl -i -s -X PUT http://localhost:8080/cdim/api/v1/configs
```

#### 3.3. Change User Authentication Methods and Permissions
> [!NOTE]
> Keycloak is used for authentication.  
> For details, refer to the [official documentation (English version)](https://www.keycloak.org/documentation).

##### 3.3.1. Add Users

1. Access the Keycloak master URL for CDIM user management and log in
   - When operating from the user management screen  
  
    Log in with an account that has cdim-manage-user permissions (such as Administrator) and press User Management/User List.

    Press "Admin Console" in the upper right and log in.
    ![](imgs/user-dashboard.png)

   - When operating from the Keycloak management URL  
  
    Follow the instructions in [getting started](../../../getting-started/en/setup/setup.md#2-frontend) to log in directly to the Keycloak management screen.  
    After logging in, change the dropdown list in the upper left from Keycloak to CDIM to switch to the CDIM management screen.

> [!NOTE]
> If you log in from the user management screen, you may see a "We are sorry" screen, but this is not a problem.  
> Press "Back to Application" to connect to the CDIM management URL.

> [!NOTE] 
> Also, users without the cdim-administrator role can transition to the user management screen, but cannot make changes such as adding users.  
<r>

1. Add users from Users  
    Press Users in the menu on the left side of the screen and press the "Add User" button.
    ![](imgs/user-console-keycloak.png)
    Select "English/Japanese" for locale and enter the user name.
    ![](imgs/add-user-keycloak.png)
    After entering other necessary items, press the "Create" button to create the user.
    <br>

2. Delete a user  
   Select the user you want to delete and press "Delete User".
   ![](imgs/delete-user.png)
   ![](imgs/delete-user2.png)

##### 3.3.2. Change User Permissions in CDIM
- Add permissions to a user
  1. Open the details screen of the created user  
     Access the URL for user management and switch to the CDIM management screen.  
     Press Users on the left side of the screen and open the details screen of the user whose permissions you want to change.  
     ![](imgs/user-details-keycloak.png)
     <br>
  2. Change permissions from "Role mapping"  
     * To add permissions  
     Select "Role mapping" from the tabs at the top of the screen and press the "Assign role" button.
     ![](imgs/user-rolemapping-keycloak.png)  
     Change the filter in the upper left to "Filter by realm roles".
     ![](imgs/change-filter-keycloak.png)  
     Check the permissions you want to add and press Assign.
     ![](imgs/add-roles-keycloak.png)
     After adding the role, log in again to apply the settings.

   <details>
   <summary> Details of CDIM Permissions </summary>
   Can be selected when the filter in the upper left is "filter by realm roles".

   - User Roles
  
   | Role | Name | Description |
   |:--|:--|:--|
   | Guest | cdim-viewer | Can view all menus in CDIM. A composite role that includes cdim-view-layout, cdim-view-resource, and cdim-view-user |
   | DC Operator | cdim-operator | Can operate all menus in CDIM. A composite role that includes cdim-viewer permissions as well as cdim-manage-layout and cdim-manage-resource |
   | DC Administrator | cdim-administrator | Can operate all permissions in CDIM. A composite role that includes cdim-operator permissions as well as cdim-manage-user permissions |
   
   </details>

- Remove permissions  
   In the "Role mapping" screen, check the permissions you want to remove and press the Unassign button.
   ![](imgs/unassign-roles-keycloak.png)

##### 3.3.3. Register and Change User Authentication Methods
###### 3.3.3.1. Password Authentication Settings

1. Assign a password to the user  
   Log in with an account that has cdim-administrator permissions, press User Management/User List, and press "Admin Console" in the upper right.  
   From Users in the left menu of the screen, open the details screen of the user you want to register for password authentication.  
   Select the "Credentials" tab and press "Set Password". After entering the password, press the "Save" button.
   ![](imgs/check-credential-keycloak.png)
   ![](imgs/enter-password-keycloak.png)  

   > [!TIP]
   > If you are issuing an account to a user, turn "Temporary" ON.  
   > In this case, the user will be prompted to set a new password upon first login.

   Access the CDIM URL and log in with password authentication.

2. Password Policy Settings  
   Log in to the user management URL with a REALM management account.
   Press "Authentication" and select the "Policy" tab.
   ![](imgs/dashboard_authentication.png)
   ![](imgs/dashboard_password_policy.png)
   Select "Add policy" in the password policy section and choose the password policy you want to add.
   ![](imgs/add_password_policy.png)

<!--
###### 3.3.3.2. OTP (One Time Password) Authentication Method

Log in to the Keycloak master URL and change the dropdown list in the upper left from Keycloak to CDIM.
Select the "Authentication" menu and choose the Flow you want to change the authentication method for.
Select "Add step" and choose "OTP Form" for the OTP authentication Flow, and insert it at your preferred timing in the Flow.
After deciding the Flow, return to the "Authentication" menu, select Policies/OTP Policy from the tabs above.
After setting the details of the OTP authentication, press "Save" to complete the settings.

Access CDIM and log in with OTP authentication.

###### 3.3.3.3. Single Sign-On Authentication Method
-->

[Next 4. Appendix](../appendix/README.md)

