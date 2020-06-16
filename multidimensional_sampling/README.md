# Work in progress:

1. setting up a full package
1. moving sample scripts to subdirectory
1. support pgen and non-pgen sampling
1. rename pgen_sample scisample

# object thoughts:

1. object: sample(dict)
1. object.samples
1. make extensible
1. add doc strings
1. add optional maestro behavior
1. add csv output

# Multidimensional Sampling

This repo contains a pgen script for maestro that implements several
multidimensional sampling methods which are driven by a simple yaml
specification included in the env/variables section of any maestro
specification. This yaml specification is a nested list named
`SAMPLE_DICTIONARY`, and this repo contains several examples. 

The pgen script is executed as follows
 
```
maestro run [-y] --pgen ./pgen_sample.py {sample_list.yaml},
```

where `[-y]` is an optional `auto-run` option, and `sample_list.yaml` is a maestro specification containing a `SAMPLE_DICTIONARY`.  

`pgen_sample.py` currently supports four sampling modes:

1. `list`: see `sample_list.yaml`
1. `column_list`: see `sample_column_list.yaml`
1. `cross_product`: see `sample_cross_product.yaml`
1. `best_candidate`: see `sample_best_candidate.yaml`

Note: the `best_candidate` sampling mode currently requires that maestro is installed from scratch in a virtual environment (see Maestro [install documentation](https://github.com/LLNL/maestrowf#setting-up-your-python-environment)) and that the `pandas`, `scipy`, and `sklearn` packages be installed in that environment as well. Please see the [installing the necessary python packages](#installing-the-necessary-python-packages) section below. 

## The List Mode

The `list` mode requires two items to be defined
in `SAMPLE_DICTIONARY`:

1. `sample_type` must equal `list`
2. `constants` or `parameters` must contain at least one variable
and one value.

The following sample dictionary

```
SAMPLE_DICTIONARY:
    sample_type: list
    constants:
        X3: 20
    parameters:
        X1: [ 5, 10 ]
        X2: [ 5, 10 ]
```
is equivalent to the following Maestro global.parameter block:

```
global.parameters:
    X1:
        values: [5, 10]
        label: X1.%%
    X2:
        values: [5, 10]
        label: X2.%%
    X3:
        values: [20, 20]
        label: X3.%%

```

## The Column List Mode

The `column_list` mode requires two items to be defined
in`SAMPLE_DICTIONARY`:

1. `sample_type` must equal `column_list`
2. `constants` or `parameters` must contain at least one variable
and one value.

The following sample dictionary

```
SAMPLE_DICTIONARY:
    sample_type: column_list
    constants:
        X3: 20
    parameters: |
        X1  X2
        5   5
        10  10
```
is also equivalent to the following Maestro global.parameter block:

```
global.parameters:
    X1:
        values: [5, 10]
        label: X1.%%
    X2:
        values: [5, 10]
        label: X2.%%
    X3:
        values: [20, 20]
        label: X3.%%

```

## The Cross Product Mode

The `cross_product` mode requires two items to be defined
in`SAMPLE_DICTIONARY`:

1. `sample_type` must equal `cross_product`
2. `constants` or `parameters` must contain at least one variable
and one value.

The following sample dictionary

```
SAMPLE_DICTIONARY:
    sample_type: cross_product
    constants:
        X4: 20
    parameters:
        X1: [ 5, 10 ]
        X2: [ 5, 10 ]
        X3: [ 5, 10 ]
```
is also equivalent to the following Maestro global.parameter block:

```
global.parameters:
    X1:
        values: [5, 5, 5, 5, 10, 10, 10, 10]
        label: X1.%%
    X2:
        values: [5, 5, 10, 10, 5, 5, 10, 10]
        label: X2.%%
    X3:
        values: [5, 10, 5, 10, 5, 10, 5, 10]
        label: X3.%%
    X4:
        values: [20, 20, 20, 20, 20, 20, 20, 20]
        label: X4.%%

```


## The Best Candidate Mode

The `cross_product` mode requires three items to be defined
in`SAMPLE_DICTIONARY`:

1. `sample_type` must equal `best_candidate`
1. `num_samples` must contain an integer
2. `parameters` must contain at least one variable
and one range.

The following sample dictionary

```
        SAMPLE_DICTIONARY:
            sample_type: best_candidate
            num_samples: 4
            # previous_samples: samples.csv # optional
            constants:
                X3: 20
            parameters:
                X1:
                   min: 10
                   max: 50
                X2:
                   min: 10
                   max: 50
```
will produce different results each time it is run. Below is an example of an equivalent Maestro global.parameter block:

```
global.parameters:
    X1:
        values: [48.70164719044195, 10.286343604507039, 22.19704244879045, 28.491627750335073]
        label: X1.%%
    X2:
        values: [29.705997207402138, 36.7811077888954, 11.310907646035941, 48.554124837450594]
        label: X2.%%
    X3:
        values: [20, 20, 20, 20]
        label: X3.%%

```

## Installing the necessary python packages

The `best_candidate` sampling mode currently requires that maestro is installed from scratch in a virtual environment (see Maestro [install documentation](https://github.com/LLNL/maestrowf#setting-up-your-python-environment)) and that the `pandas`, `scipy`, and `sklearn` packages be installed in that environment as well. Below are the steps to take: 

```
# set install locations:
MAESTRO_INSTALL_DIRECTORY=${HOME}/maestro_install
MAESTRO_SHEETMUSIC_DIRECTORY=${HOME}/maestro_sheetmusic_install

# Deactivate any current virtual environments.
deactivate 

# Clone a fresh copy of the maestro source.
# Note: this can not be in the maestro_sheetmusic directory.
mkdir ${MAESTRO_INSTALL_DIRECTORY}
cd ${MAESTRO_INSTALL_DIRECTORY}
date > maestro_install_start.txt
git clone https://github.com/LLNL/maestrowf.git 

# Set up and activate a new virtual environment.
cd maestrowf
python3 -m venv venv
source venv/bin/activate

# Install maestro.
pip install -r requirements.txt
pip install -e .

# Install pandas, scipy, and sklearn
pip install pandas
pip install scipy
pip install sklearn

# Timestamp #2
cd ${MAESTRO_INSTALL_DIRECTORY}
date > maestro_install_end.txt

# Clone maestro sheetmusic
mkdir ${MAESTRO_SHEETMUSIC_DIRECTORY}
cd ${MAESTRO_SHEETMUSIC_DIRECTORY}
git clone https://github.com/LLNL/maestro_sheetmusic.git 

# Run smart_sampler_demo
cd ${MAESTRO_SHEETMUSIC_DIRECTORY}/maestro_sheetmusic/multidimensional_sampling
maestro run -y --pgen ./pgen_sample.py sample_best_candidate.yaml

# Timestamp #3
cd ${MAESTRO_INSTALL_DIRECTORY}
date > maestro_sheetmusic_run_end.txt
echo done
```

