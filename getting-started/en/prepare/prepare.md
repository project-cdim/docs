# Set Up Environment

## 1. Prerequisites

List of prerequisites:

- The Operating System is installed.

## 2. Install Git

Install Git.

```sh
sudo dnf install git
```

Ensure the `git` command can be executed.
Check that the Git version is displayed with the following command:

```sh
git version
```

## 3. Install Docker

Refer to the Docker documentation to install Docker Engine.

- https://docs.docker.com/engine/install/

To grant the user executing the CDIM installation process the permission to run the `docker` command,
add the user to the docker group.

If the current user is the one being used for the CDIM installation process,
execute the following command:

```sh
sudo gpasswd -a $USER docker
```

Verify that the specified user has been added to the docker group.
Ensure the specified username is displayed with the command below:

```sh
getent group docker
```

## 4. Create Docker Network

Create a Docker network for CDIM and the emulator.

```sh
docker network create cdim-net
```

Verify that the Docker network is created.
Ensure cdim-net is displayed with the command below:

```sh
docker network ls
```