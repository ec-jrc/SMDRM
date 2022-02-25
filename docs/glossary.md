# Glossary

Let us establish a concise glossary of terms that will be the jargon used throughout the documentation.

## Annotate

The action of assigning a probability score to the `text` field of a datapoint.
This is a float number between 0 and 1 representing the likelihood that the textual
information in the `text` field refers to a specific [disaster](#disaster) type.

## Datapoint

It is a JSON dictionary made of a specific set of [fields](architecture.md#fields).

## Directed Acyclic Graph

Within the Airflow ecosystem, a Directed Acyclic Graph (DAG) is a workflow of coded instructions
to execute a sequence of _tasks_ that make a pipeline. Each task must be atomic,
which means it produces the same result every time it is executed on a defined dataset.
A DAG specifies the dependencies between tasks, and the order in which to execute them, and run retries.

## Disaster

Within the context of SMDRM, a (environmental) disaster can be of the following types:
* Floods

## Task

A task is the smallest component of a pipeline. It executes a specific logic,
be it fetching data, running analysis, triggering other systems, or more.

## Workflow

A workflow consists of an orchestrated and repeatable pattern of activity,
enabled by the systematic organization of resources into processes that
transform materials, provide services, or process information.

Source [Wikipedia](https://en.wikipedia.org/wiki/Workflow)

