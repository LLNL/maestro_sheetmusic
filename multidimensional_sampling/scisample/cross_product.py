"""This file implements several sampling methods"""

import logging

from .utils import (
    _log_assert, _validate_constants_parameters)

LOGGER = logging.getLogger(__name__)

def _validate_cross_product_dictionary(sampling_dict):
    _validate_constants_parameters(sampling_dict)
    if "parameters" in sampling_dict.keys():
        for key, value in sampling_dict["parameters"].items():
            _log_assert(type(key) == str, "parameter labels must be strings")
            _log_assert(type(value) == list, "parameter values must be a list")


def _recursive_cross_product_sample(params, samples=[{}]):
    if params == {}:
        return samples
    key = next(iter(params))
    new_list = []
    for sample in samples:
        for item in params[key]:
            new_sample = sample.copy()
            new_sample[key] = item
            new_list.append(new_sample)
    new_params = params.copy()
    new_params.pop(key)
    return _recursive_cross_product_sample(new_params, samples=new_list)


def cross_product_sample(sampling_dict):
    """
    Return set of samples based on specification in sampling_dict.

    Prototype dictionary:

    sample_type: cross_product
    parameters:
        X1: [ 10, 20 ]
        X2: [ 10, 20 ]
    constants:
        X3: 20
    """
    _validate_cross_product_dictionary(sampling_dict)
    samples = []
    if "constants" in sampling_dict.keys():
        constants = {}
        for key, value in sampling_dict["constants"].items():
            constants[key] = value
    else:
        constants = {}
    if "parameters" in sampling_dict.keys():
        parameters = sampling_dict["parameters"].copy()
        samples = _recursive_cross_product_sample(
                                            parameters,
                                            samples=[constants])
    else:
        samples = [constants]
    LOGGER.info("samples:\n%s", str(samples))
    return samples
