"""This file implements several sampling methods"""

import logging

from maestrowf.datastructures.core import ParameterGenerator

# can importing the sample functions be made more compact?
from scisample.list import list_sample
from scisample.cross_product import cross_product_sample
from scisample.column_list import column_list_sample
from scisample.utils import _convert_dict_to_maestro_params

LOGGER = logging.getLogger(__name__)


def get_custom_generator(env, **kwargs):
    """
    Create a custom populated ParameterGenerator.

    This function supports several sampling methods.

    :params kwargs: A dictionary of keyword arguments this function uses.
    :returns: A ParameterGenerator populated with parameters.
    """
    p_gen = ParameterGenerator()

    LOGGER.info("pgen env:\n%s", str(env))
    LOGGER.info("pgen type(env):\n%s", str(type(env)))
    LOGGER.info("pgen kwargs:\n%s", str(kwargs))
    LOGGER.info("pgen type(kwargs):\n%s", str(type(kwargs)))

    try:
        SAMPLE_DICTIONARY = kwargs.get(
            "sample_dictionary",
            env.find("SAMPLE_DICTIONARY").value)
    except ValueError:
        raise ValueError("this pgen code requires SAMPLE_DICTIONARY " +
                         "to be defined in the yaml specification")
    try:
        sample_type = SAMPLE_DICTIONARY["sample_type"]
    except ValueError:
        raise ValueError("this pgen code requires SAMPLE_DICTIONARY" +
                         "['sample_type'] to be defined in the yaml " +
                         "specification")
    if sample_type == "list":
        samples = list_sample(SAMPLE_DICTIONARY)
    elif sample_type == "cross_product":
        samples = cross_product_sample(SAMPLE_DICTIONARY)
    elif sample_type == "column_list":
        samples = column_list_sample(SAMPLE_DICTIONARY)
    # elif sample_type == "best_candidate":
    #     samples = best_candidate_sample(SAMPLE_DICTIONARY)
    else:
        raise ValueError("The 'sample_type' of " + sample_type +
                         " is not supported.")

    params = _convert_dict_to_maestro_params(samples)
    LOGGER.info("params:\n%s", str(params))

    for key, value in params.items():
        p_gen.add_parameter(key, value["values"], value["label"])

    return p_gen
