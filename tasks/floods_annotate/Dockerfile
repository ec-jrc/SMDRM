# syntax=docker/dockerfile:1
FROM libdrm

# set working directory
WORKDIR /home/smdrm/floods_annotate

# copy source code
COPY VERSION.txt .
COPY floods_annotate.py .
COPY tests tests

# runtime execution
CMD python floods_annotate.py --help

