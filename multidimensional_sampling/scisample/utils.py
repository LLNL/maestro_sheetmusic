"""This file implements several sampling methods"""

import yaml
import random
import glob
import time
from math import *

import logging
from maestrowf.datastructures.core import ParameterGenerator

LOGGER = logging.getLogger(__name__)

def _log_assert(test, msg):
    if not(test):
        LOGGER.error(msg)
        raise ValueError(msg)


def _validate_constants_parameters(sampling_dict):
    _log_assert(
        ("parameters" in sampling_dict.keys() or
         "constants" in sampling_dict.keys()),
        "'parameters' or 'constants' must exist")
    if "constants" in sampling_dict.keys():
        _log_assert(
            isinstance(sampling_dict["constants"], dict),
            "'constants' must be a dictionary")


def _validate_parameters_dict(sampling_dict):
    if "parameters" in sampling_dict.keys():
        _log_assert(
            isinstance(sampling_dict["parameters"], dict),
            "'parameters' must be a dictionary for this sampling type")


def _validate_parameters_string(sampling_dict):
    if "parameters" in sampling_dict.keys():
        _log_assert(
            isinstance(sampling_dict["parameters"], str),
            "'parameters' must be a string for this sampling type")


def _validate_sample_dict(samples):
    keys = list(samples[0].keys())
    for row in samples:
        for key in keys:
            _log_assert(
                key in list(row.keys()),
                ("data point " +
                 str(row) + " does not have a value for " +
                 str(key)))


def _convert_dict_to_maestro_params(samples):
    _validate_sample_dict(samples)
    keys = list(samples[0].keys())
    parameters = {}
    for key in keys:
        parameters[key] = {}
        parameters[key]["label"] = str(key) + ".%%"
        values = [sample[key] for sample in samples]
        parameters[key]["values"] = values
    return parameters



