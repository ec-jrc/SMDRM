# Floods

This is our `floods_model` Docker image.

It uses Machine Learning models trained on text related to flood disasters to annotate new incoming texts.

## Instructions

For more details, check the [Makefile](Makefile).

### Build

```shell
make image
```

### Create Docker Volume

```shell
make volume
```

Actions:
* Create Docker Volume
* Populate Volume
