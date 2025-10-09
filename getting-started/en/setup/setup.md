# Initial Setup for CDIM

> [!NOTE]
> Use the same value for `cdim-server` as used in the configuration file for [Installing CDIM](../install/install.md).

## 1. Gateway (Kong) Setup

### 1.1. Confirm Public Key

Log in to Keycloak.

```sh
http://cdim-server:8287/
Username: admin
Password: admin
```

Switch to the "CDIM" realm.

Click "Realm settings" and then click the "Keys" tab. Check and copy the "Public key" for "RS256".  
![fig 1-1 Realm Settings Keys](img/key.png)

### 1.2. Setup Gateway with Public Key

Using the copied Public Key from "1.1", create a `public_key.pem` file in the `set-up-tools/gateway/tools/` directory using the format shown below:

```txt:public_key.pem
-----BEGIN PUBLIC KEY-----
(Paste the copied Public key here)
-----END PUBLIC KEY-----
```

Run the `post_install` script to initialize the gateway.

```sh
./post_install
```

Afterward, reset the gateway containers.

```sh
cd base-compose
docker compose down gateway-dapr
docker compose down gateway
docker compose up -d --build
```

## 2. Frontend Configuration

### 2.1. Create Client in Keycloak

Log in to Keycloak.

```sh
http://cdim-server:8287/
Username: admin
Password: admin
```

Click "Clients" and then click "Create client", then click on "Create client".  
![fig 2-1 Clients Create Client](img/add_client1.png)

In "General settings", configure as follows and click "Next".

| Item | Value |
|---|---|
| Client type | OpenID Connect |
| Client ID | cdim-client |
| Name | (leave blank) |
| Description | (leave blank) |
| Always display in UI | Off |

![fig 2-2 Clients Create Client](img/add_client2.png)

In "Capability config", only enable "Standard flow" under "Authentication flow" and click "Next".

![fig 2-3 Clients Create Client](img/add_client3.png)

Specify the following in "Login settings":

| Item | Value |
|------|------|
| Root URL | <http://cdim-server:3000/> |
| Home URL | <http://cdim-server:3000/> |
| Valid redirect URIs | <http://cdim-server:3000/*> |
| Valid post logout redirect URIs | <http://cdim-server:3000/*> |
| Web origins | * |

![fig 2-4 Clients Create Client](img/add_client4.png)

Click "Save" to finalize the settings.

### 2.2. User Setup

Create a user account for CDIM, ideally with administrative privileges.

#### 2.2.1. Add User

Click "Users" and then click "Add User".
![fig 2-1 Users Add User](img/add_user1.png)

Enter the "Username" and click "Create".
![fig 2-2 Users Add User](img/add_user2.png)

#### 2.2.2. Set User Password

Click the "Credentials" tab, and in the displayed screen, click the "Set password".
![fig 2-3 Users Add User](img/add_user3.png)

Enter the password. Set "Temporary" to "Off". Click the "Save".  
![fig 2-4 Users Add User](img/add_user4.png)

Click the "Save password".  
![fig 2-5 Users Add User](img/add_user5.png)

#### 2.2.3. Assign Roles

Click the "Role mapping" tab and then click the "Assign role".
![fig 2-6 Users Add User](img/add_user6.png)

Switch the filter condition to "Filter by realm roles".
![fig 2-7 Users Add User](img/add_user7.png)

Check the role to be assigned in the list. Here, check "cdim-administrator", which represents administrator privileges. Click the "Assign".  
![fig 2-8 Users Add user](img/add_user8.png)

## 3. Verification

Log in to CDIM using the credentials of the user you just created.

```sh
http://cdim-server:3000/
```

If the dashboard correctly displays information like resource data retrieved from the emulator, then the setup is successful.  
![fig 3-1 CDIM Dashboard](img/cdim_dashboard.png)

[Next step: Using CDIM](../use/use.md)
