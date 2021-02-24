"""This file implements several sampling methods

The most current version is kept at:
https://github.com/LLNL/scisample/blob/master/bin/pgen_scisample.py
"""

import logging

from scisample.samplers import new_sampler

LOG = logging.getLogger(__name__)


def get_custom_generator(env, **kwargs):
    """
    Create a custom populated ParameterGenerator.
    This function supports several sampling methods.
    :params kwargs: A dictionary of keyword arguments this function uses.
    :returns: A ParameterGenerator populated with parameters.
    """

    try:
        SAMPLE_DICTIONARY = kwargs.get(
            "sample_dictionary",
            env.find("SAMPLE_DICTIONARY").value)
    except ValueError:
        raise Exception("this pgen code requires SAMPLE_DICTIONARY " +
                        "to be defined in the yaml specification")

    return new_sampler(SAMPLE_DICTIONARY).maestro_pgen

def main():
    print("This script needs to be used by maestrowf.")
    print("Please visit https://github.com/LLNL/maestrowf for more information.")

if __name__ == "__main__":
    # execute only if run as a script
    main()
