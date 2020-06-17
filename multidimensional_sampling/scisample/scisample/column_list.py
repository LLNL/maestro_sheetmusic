"""This file implements several sampling methods"""
import logging

from scisample.utils import (
    _log_assert, _validate_constants_parameters, _validate_parameters_string)

LOGGER = logging.getLogger(__name__)


def _validate_column_list_dictionary(sampling_dict):
    _validate_constants_parameters(sampling_dict)
    _validate_parameters_string(sampling_dict)


def column_list_sample(sampling_dict):
    """
    Return set of samples based on specification in sampling_dict.

    Prototype dictionary:

    sample_type: column_list
    constants:
        X3: 20
    parameters: |
        X1       X2
        5        10
        3        7
        12       16
    """
    _validate_column_list_dictionary(sampling_dict)
    samples = []
    if "constants" in sampling_dict.keys():
        constants = {}
        for key, value in sampling_dict["constants"].items():
            constants[key] = value
    else:
        constants = {}
    if "parameters" in sampling_dict.keys():
        rows = sampling_dict["parameters"].split('\n')
        headers = rows.pop(0).split()
        for row in rows:
            data = row.split()
            if len(data) > 0:
                _log_assert(
                    len(data) == len(headers),
                    "Data >>" + str(data) + "<< does not match\n" +
                    "headers >>" + str(headers) + "<<.")
                sample = constants.copy()
                for header, datum in zip(headers, data):
                    sample[header] = datum
                samples.append(sample)
    else:
        samples.append(constants)
    return samples

