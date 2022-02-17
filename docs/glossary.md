# Glossary

Let us establish a concise glossary of terms that will be the jargon used throughout the documentation.

## Annotate

The action of assigning a probability score to the `text` field of a datapoint
i.e., a float number between 0 and 1 representing the likelihood that the textual
information in the `text` field refers to a specific disaster type.

## DAG

Add

### Datapoints

The smallest data unit. It is a JSON formatted dictionary made of a number of required fields.
For more info, see the [Input Data Model](../README.md#input-data-model) section.

## Disaster

Within the context of SMDRM, a (environmental) disaster can be of the following types:
* Floods

## Uploads

The compressed input data that users intend to enrich.
Each upload has the following requirements:
* at least 1 zip file
* at least 1 JSON file in the zip file
* only 1 JSON formatted datapoint for each line in the JSON file

You can verify the required datapoint structure in the [Input Data Model](../README.md#input-data-model) section.

## Workflow

add

