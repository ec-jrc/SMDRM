# Tools

This directory should be mounted into a Docker container to enable development functionalities at runtime.

## Jupyter Dev Env

A Jupyter Notebook based development framework

```shell
docker-compose run --rm -v $(pwd):/opt/smdrm/ws -w /opt/smdrm/ws libdrm bash tools/dev.sh
```

