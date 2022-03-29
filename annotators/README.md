# Annotators

The Named Entity Recognition (NER) Machine Learning models to annotate the
textual information in the disaster related data points.
Each model is available by means of HTTP API call to a dedicated endpoint.

At the moment, the following annotators are shown in table 1.

|Name|Description|Licence|Notes|
|----|-----------|-------|-----|
|[DeepPavlov](deeppavlov/README.md)|Multilingual Geo Political Entities (GPE), Locations (LOC), and Facilities (FAC) NER tagging|[Apache Licence](https://github.com/deepmipt/DeepPavlov/blob/master/LICENSE)|External|
|[Floods](floods/README.md)|Multilingual floods disaster related probability annotation.|[European Union Public Licence V1.2](https://joinup.ec.europa.eu/collection/eupl/eupl-text-eupl-12)|Internal|

_Table 1. Available Machine Learning Annotators._

## Performance Tests

Performance tests validate an annotator's performance.
They are run against a multilingual (4) test [dataset](tests/perf/data/).

> :bangbang: Execute the following command from the project root directory

Say, you want to test the Floods annotator.
Build the annotator, and the performance test Docker images.

```shell
docker-compose build annotators-perftests annotators-floods
```

Start the Floods annotator

```shell
docker-compose up annotators-floods
```

When the annotator is healthy, you can trigger the performance tests

```shell
docker-compose run --rm annotators-perftests --annotator floods
```

## Troubleshooting

> :warning: Given the size of some Machine Learning packages,
> you might incur in the Out Of Memory (OOM) error on Mac, and Windows OS.
>
> To avoid that, make sure you allocate at least 4 GB of memory to Docker containers.
> For more info, check the Resource management pages for your OS:
> * [Mac](https://docs.docker.com/desktop/mac/#resources)
> * [Windows](https://docs.docker.com/desktop/windows/#resources)

