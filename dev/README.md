# Development Environment

The Development Environment (DE) is based on the `python:3.8-slim-bullseye` Docker image,
that is the same image used to build the Engine and Upload APIs.

The purpose of the DE is to set a common working environment for all users to be able to
create and test new features in a repeatable and standard manner.

> :information_source: The Image is based on Debian, so you can install additional OS libraries using the `apt`
> package manager. Run `apt update` to enable its functionality.

## Build
```shell
bash dev/build.sh
```

## Run
```shell
bash dev/run.sh
```

## Usage

The DE uses the Docker Bind Mount functionality to reference the project directory (and its content) in the container
at runtime, in the `workspace` directory.

> :warning: Be aware that any change in the filesystem of the DE will be reflected in the referenced filesystem.

The DE comes with pre-installed dependencies that do NOT include those required by the SMDRM microservices.
This is intended to reduce build time. For more info, see [requirements.txt](requirements.txt).
You can manually install the dependencies of a service using the requirements.txt file in its directory.
