"""This file implements several sampling methods"""

import logging

from scisample.utils import (
    _log_assert, _validate_constants_parameters, _validate_parameters_dict)

LOGGER = logging.getLogger(__name__)


def _validate_list_dictionary(sampling_dict):
    _validate_constants_parameters(sampling_dict)
    _validate_parameters_dict(sampling_dict)
    if "parameters" in sampling_dict.keys():
        first = True
        for key, value in sampling_dict["parameters"].items():
            _log_assert(type(key) == str, "parameter labels must be strings")
            _log_assert(type(value) == list, "parameter values must be a list")
            if first:
                sample_length = len(value)
            _log_assert(
                len(value) == sample_length,
                "all sample lists must be the same length")


def list_sample(sampling_dict):
    """
    Return set of samples based on specification in sampling_dict.

    Prototype dictionary:

    sample_type: list
    parameters:
        X1: [ 10, 20, 30 ]
        X2: [ 10, 20, 30 ]
    constants:
        X3: 20
    """
    _validate_list_dictionary(sampling_dict)
    samples = []
    if "constants" in sampling_dict.keys():
        constants = {}
        for key, value in sampling_dict["constants"].items():
            constants[key] = value
    else:
        constants = {}
    if "parameters" in sampling_dict.keys():
        parameters = sampling_dict["parameters"]
        sample_length = len(parameters[next(iter(parameters))])
        for i in range(sample_length):
            sample = constants.copy()
            for key, items in sampling_dict["parameters"].items():
                sample[key] = items[i]
            samples.append(sample)
    else:
        samples.append(constants)
    return samples
