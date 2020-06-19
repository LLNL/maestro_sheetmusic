import logging
import random

from contextlib import suppress

from scisample.utils import (
    _log_assert, _validate_constants_parameters, _validate_parameters_dict)

PANDAS_PLUS = False
with suppress(ModuleNotFoundError):
    import pandas as pd
    import numpy as np
    import scipy.spatial as spatial
    PANDAS_PLUS = True

LOGGER = logging.getLogger(__name__)


def _validate_best_candidate_dictionary(sampling_dict):
    _validate_constants_parameters(sampling_dict)
    _validate_parameters_dict(sampling_dict)
    _log_assert(
        type(sampling_dict["num_samples"]) == int,
        "'num_samples' must exist and be an integer")
    _log_assert(
        isinstance(sampling_dict["parameters"], dict),
        "'parameters' must exist and be a dictionary")
    if 'previous_samples' in sampling_dict.keys():
        pass
        # TTD: validate that file exists and that it
        # contains same parameters as `parameters`
    for key, value in sampling_dict["parameters"].items():
        _log_assert(type(key) == str, "parameter labels must be strings")
        _log_assert(
            str(value["min"]).isnumeric(),
            "parameter must have a numeric minimum")
        _log_assert(
            str(value["max"]).isnumeric(),
            "parameter must have a numeric maximum")


def downselect(samples, sampling_dict):
    """
    Downselect samples based on specification in sampling_dict.

    Prototype dictionary::

       num_samples: 30
       previous_samples: samples.csv # optional
       parameters:
           X1:
               min: 10
               max: 50
           X2:
               min: 10
               max: 50
    """
    _log_assert(
        PANDAS_PLUS,
        "This function requires pandas, numpy, scipy & sklearn packages")
    _validate_best_candidate_dictionary(sampling_dict)

    df = pd.DataFrame.from_dict(samples)
    columns = sampling_dict["parameters"].keys()
    ndims = len(columns)
    candidates = df[columns].values.tolist()
    num_points = sampling_dict["num_samples"]

    if not('previous_samples' in sampling_dict.keys()):
        sample_points = []
        sample_points.append(candidates[0])
        new_sample_points = []
        new_sample_points.append(candidates[0])
        new_sample_ids = []
        new_sample_ids.append(0)
        n0 = 1
    else:
        try:
            previous_samples = pd.read_csv(sampling_dict["previous_samples"])
        except ValueError:
            raise Exception("Error opening previous_samples datafile:" +
                            sampling_dict["previous_samples"])
        sample_points = previous_samples[columns].values.tolist()
        new_sample_points = []
        new_sample_ids = []
        n0 = 0

    mins = np.zeros(ndims)
    maxs = np.zeros(ndims)

    first = True
    for i in range(len(candidates)):
        ppi = candidates[i]
        for j in range(ndims):
            if first:
                mins[j] = ppi[j]
                maxs[j] = ppi[j]
                first = False
            else:
                mins[j] = min(ppi[j], mins[j])
                maxs[j] = max(ppi[j], maxs[j])
    print("extrema for new input_labels: ", mins, maxs)
    print("down sampling to %d best candidates from %d total points." % (
        num_points, len(candidates)))
    bign = len(candidates)

    for n in range(n0, num_points):
        px = np.asarray(sample_points)
        tree = spatial.KDTree(px)
        j = bign
        d = 0.0
        for i in range(1, bign):
            pos = candidates[i]
            dist = tree.query(pos)[0]
            if dist > d:
                j = i
                d = dist
        if j == bign:
            raise Exception("Something went wrong!")
        else:
            new_sample_points.append(candidates[j])
            sample_points.append(candidates[j])
            new_sample_ids.append(j)

    new_samples_df = pd.DataFrame(columns=df.keys().tolist())
    for n in range(len(new_sample_ids)):
        new_samples_df = new_samples_df.append(df.iloc[new_sample_ids[n]])

    return new_samples_df.to_dict(orient='records')


def random_sample(sampling_dict):
    """
    Return set of random samples based on specification in sampling_dict.

    Prototype dictionary:

    num_samples: 30
    previous_samples: samples.csv # optional
    parameters:
        X1:
            min: 10
            max: 50
        X2:
            min: 10
            max: 50
    """
    _validate_best_candidate_dictionary(sampling_dict)
    # create initial input data
    random_list = []
    min_dict = {}
    range_dict = {}
    for key, value in sampling_dict["parameters"].items():
        min_dict[key] = value["min"]
        range_dict[key] = value["max"] - value["min"]
    for i in range(sampling_dict["num_samples"]):
        random_dictionary = {}
        for key, value in sampling_dict["parameters"].items():
            random_dictionary[key] = (
                min_dict[key] + random.random() * range_dict[key])
        random_list.append(random_dictionary)
    return(random_list)


def best_candidate_sample(sampling_dict, over_sample_rate=10):
    """
    Return set of best candidate samples based on specification in sampling_dict.

    Prototype dictionary:

    sample_type: best_candidate
    num_samples: 30
    # previous_samples: samples.csv
    constants:
        X3: 20
    parameters:
        X1:
            min: 10
            max: 50
        X2:
            min: 10
            max: 50
    """
    _log_assert(
        PANDAS_PLUS,
        "This function requires pandas, numpy, scipy & sklearn packages")
    _validate_best_candidate_dictionary(sampling_dict)
    new_sampling_dict = sampling_dict.copy()
    new_sampling_dict["num_samples"] *= over_sample_rate
    new_random_sample = random_sample(new_sampling_dict)

    samples = downselect(new_random_sample, sampling_dict)
    if "constants" in sampling_dict.keys():
        for sample in samples:
            for key, value in sampling_dict["constants"].items():
                sample[key] = value

    return samples
