"""This file implements several sampling methods"""

import logging

from contextlib import suppress

from scisample.list import list_sample
from scisample.cross_product import cross_product_sample
from scisample.column_list import column_list_sample
from scisample.best_candidate import best_candidate_sample
from scisample.utils import _convert_dict_to_maestro_params

SAMPLE_FUNCTIONS_DICT = {
    "list": list_sample,
    "cross_product": cross_product_sample,
    "column_list": column_list_sample,
    "best_candidate": best_candidate_sample
}

MAESTROWF = False
with suppress(ModuleNotFoundError):
    from maestrowf.datastructures.core import ParameterGenerator
    MAESTROWF = True

LOGGER = logging.getLogger(__name__)


class Samples:
    """
    Provides access to several different sampling methods
    """

    def __init__(self, samples_specification):
        LOGGER.info("new Samples object")
        self.dictionary = samples_specification
        self._samples = None
        self._pgen = None

        try:
            sample_type = self.dictionary["sample_type"]
            self.sample_type = sample_type
        except ValueError:
            raise Exception("this pgen code requires SAMPLE_DICTIONARY" +
                            "['sample_type'] to be defined in the yaml " +
                            "specification")

    def samples(self):
        """
        Returns a dictionary of samples
        """
        if self._samples is not None:
            return self._samples

        sample_type = self.sample_type
        try:
            sample_function = SAMPLE_FUNCTIONS_DICT[sample_type]
        except KeyError as e:
            raise KeyError("The 'sample_type' of " + sample_type +
                           " is not supported.")
        LOGGER.info("generating samples of type '" +
                    sample_type + "'")
        samples = sample_function(self.dictionary)
        LOGGER.info("generated samples:\n" + str(samples))
        self._samples = samples
        return samples

    def maestro_pgen(self):
        """
        Returns a maestrowf Parameter Generator object containing samples
        """
        if not MAESTROWF:
            raise Exception("maestrowf is not installed\n" +
                            "the maestro_pgen is not supported")
        if self._pgen is not None:
            return self._pgen

        LOGGER.info("generating ParameterGenerator object")

        pgen = ParameterGenerator()
        params = _convert_dict_to_maestro_params(self.samples())

        for key, value in params.items():
            pgen.add_parameter(key, value["values"], value["label"])

        self._pgen = pgen
        return pgen
