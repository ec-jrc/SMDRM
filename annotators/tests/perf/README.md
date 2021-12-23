# Performance Tests

> :bangbang: execute all bash commands from project root directory

## Build

```shell
docker build -t e1/annotators_perftest:1.0 $(pwd)/annotators/tests/perf/
```

## Run

```shell
docker run --rm --network <annotator-network-name> e1/annotators_perftest:1.0
```
