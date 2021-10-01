# -*- coding: utf-8 -*-

"""
The Pipes and Filters architectural pattern provides a structure for systems that process a stream of data.
Each processing step is encapsulated in a filter component. Data is passed through pipes between adjacent filters.
Recombining filters allow you to build families of related systems.
"""

import typing


def file_processing_pipeline(start_generator: typing.Iterable, filters: typing.Iterable) -> typing.Iterable:
    generator = start_generator
    for _filter in filters:
        generator = _filter(generator)
    return generator
