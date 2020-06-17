"""This file implements several sampling methods"""

import logging

from scisample.samples import Samples

LOGGER = logging.getLogger(__name__)


def get_custom_generator(env, **kwargs):
    """
    Create a custom populated ParameterGenerator.

    This function supports several sampling methods.

    :params kwargs: A dictionary of keyword arguments this function uses.
    :returns: A ParameterGenerator populated with parameters.
    """

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

    return Samples(SAMPLE_DICTIONARY).maestro_pgen()
