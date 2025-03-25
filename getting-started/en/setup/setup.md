# Initial Setup for CDIM

> [!NOTE]
> Use the same value for `cdim-server` as used in the configuration file for [Installing CDIM](../install/install.md).

## 1. Gateway (Kong)

### 1.1. Confirm Public Key

Log in to Keycloak.

```sh
http://cdim-server:8287/
admin/admin
```

Switch the realm to "CDIM".

Click "Realm settings" and then click the "Keys" tab. Check and copy the "Public key" for "RS256".
![fig 1-1 realm settings keys](img/key.png)

### 1.2. Initial Setup for Gateway

Using the Public key confirmed and copied in "1.1.", create a `public_key.pem` file under the `set-up-tools/gateway/tools/` directory. The format is as follows:

```txt:public_key.pem
-----BEGIN PUBLIC KEY-----
(Paste the copied Public key here)
-----END PUBLIC KEY-----
```

Execute the `setup` script to perform the initial setup.

```sh
./setup
```

Restart the base containers.

```sh
cd base-compose
docker compose down
docker compose up -d --build
```

## 2. Frontend

### 2.1. Create Client

Log in to Keycloak.

```sh
http://cdim-server:8287/
admin/admin
```

Switch the realm to "CDIM".

Click "Clients" and then click "Create client".
![fig 2-1 Clients Create client](img/add_client1.png)

In "General settings", configure as follows and click "Next".

| Item | Value |
|---|---|
| Client type | OpenID Connect |
| Client ID | cdim-client |
| Name | (leave blank) |
| Description | (leave blank) |
| Always display in UI | Off |

![fig 2-2 Clients Create client](img/add_client2.png)

In "Capability config", select only "Standard flow" under "Authentication flow" and click "Next".

![fig 2-3 Clients Create client](img/add_client3.png)

Specify the following in "Login settings".

| Item | Value |
|------|------|
|Root URL| <http://cdim-server:3000/>  |
|Home URL| <http://cdim-server:3000/>  |
|Valid redirect URIs| <http://cdim-server:3000/*> |
|Valid post logout redirect URIs| <http://cdim-server:3000/*> |
|Web origins| * |

![fig 2-4 Clients Create client](img/add_client4.png)

Click "Save" to save the settings.

### 2.2. Create User

Create a user for CDIM. Here, we will explain how to create an administrator user.

#### 2.2.1. Add User

Click "Users" and then click "Add User".
![fig 2-1 Users Add user](img/add_user1.png)

Enter the "Username" and click the "Create" button.
![fig 2-2 Users Add user](img/add_user2.png)

#### 2.2.2. Set Password for User

Click the "Credentials" tab, and in the displayed screen, click the "Set password" button.
![fig 2-3 Users Add user](img/add_user3.png)

Enter the password. Set "Temporary" to "Off". Click the "Save" button.
![fig 2-4 Users Add user](img/add_user4.png)

Click the "Save password" button.
![fig 2-5 Users Add user](img/add_user5.png)

#### 2.2.3. Assign Role to User

Click the "Role mapping" tab and then click the "Assign role" button.
![fig 2-6 Users Add user](img/add_user6.png)

Switch the filter condition to "Filter by realm roles".
![fig 2-7 Users Add user](img/add_user7.png)

Check the role to be assigned in the list. Here, check "cdim-administrator", which represents administrator privileges. Click the "Assign" button.
![fig 2-8 Users Add user](img/add_user8.png)

## 3. Verification

Log in to CDIM using the created user.

```sh
http://cdim-server:3000/
```

If the dashboard screen displays resource information retrieved from the emulator as shown below, it is functioning properly.

![fig 3-1 CDIM Dashboard](img/cdim_dashboard.png)

[Next step: Using CDIM](../use/use.md)
