# Multidimensional sampling using scisample

This repo contains several yaml specifications that implement
multidimensional sampling methods from the `scisample` package.
The sampling parameters are defined in the env/variables section 
of a given maestro specification. This yaml specification is a nested 
list named `SAMPLE_DICTIONARY`.

It requires the [`scisample` package](https://github.com/LLNL/scisample) 
to be installed. The `scisample` provides a `pgen_scisample.py` script 
that can be easily used with maestro with "--pgen \`which pgen_scisample.py\`". 
Some sampling methods require additional packages to
be installed. The `best_candidate` method requires `pandas`, `numpy`, and
`scipy`. 

`scisample` can be installed with `pip install scisample`.

`maestro` using `scisample` is executed as follows:
 
```
maestro run [-y] --pgen ./pgen_scisample.py {sample_list.yaml},
```

If scisample is installed with `pip`, `pgen_scisample.py` is also added to
your path, so that the following will work as well: 

```
maestro run [-y] --pgen `which pgen_sample.py` {sample_list.yaml},
```

where `[-y]` is an optional `auto-run` option, and `sample_list.yaml` is a maestro specification containing a `SAMPLE_DICTIONARY`.  

`pgen_sample.py` currently supports four sampling modes:

1. `list`: see `sample_list.yaml`
1. `column_list`: see `sample_column_list.yaml`
1. `cross_product`: see `sample_cross_product.yaml`
1. `best_candidate`: see `sample_best_candidate.yaml`
1. `random`: see `sample_random.yaml`

## The List Mode

The `list` mode requires two items to be defined
in `SAMPLE_DICTIONARY`:

1. `type` must equal `list`
2. `constants` or `parameters` must contain at least one variable
and one value.

The following sample dictionary

```yaml
SAMPLE_DICTIONARY:
    type: list
    constants:
        X3: 20
    parameters:
        X1: [ 5, 10 ]
        X2: [ 5, 10 ]
```
is equivalent to the following Maestro `global.parameter` block:

```yaml
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

1. `type` must equal `column_list`
2. `constants` or `parameters` must contain at least one variable
and one value.

The following sample dictionary

```
SAMPLE_DICTIONARY:
    type: column_list
    constants:
        X3: 20
    parameters: |
        X1  X2
        5   5
        10  10
```
is also equivalent to the following Maestro `global.parameter` block:

```yaml
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

1. `type` must equal `cross_product`
2. `constants` or `parameters` must contain at least one variable
and one value.

The following sample dictionary

```yaml
SAMPLE_DICTIONARY:
    type: cross_product
    constants:
        X4: 20
    parameters:
        X1: [ 5, 10 ]
        X2: [ 5, 10 ]
        X3: [ 5, 10 ]
```
is also equivalent to the following Maestro `global.parameter` block:

```yaml
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

The `best_candidate` mode requires three items to be defined
in`SAMPLE_DICTIONARY`:

1. `type` must equal `best_candidate`
1. `num_samples` must contain an integer
2. `parameters` must contain at least one variable
and one range.

The following sample dictionary

```yaml
SAMPLE_DICTIONARY:
    type: best_candidate
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
will produce different results each time it is run. Below is an example of an 
equivalent Maestro `global.parameter` block:

```yaml
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

## The Random Mode

The `random` mode requires three items to be defined
in`SAMPLE_DICTIONARY`:

1. `type` must equal `random`
1. `num_samples` must contain an integer
2. `parameters` must contain at least one variable
and one range.

The following sample dictionary

```yaml
SAMPLE_DICTIONARY:
    type: random
    num_samples: 4
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

```yaml
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

# Testing

The integration of `scisample` with `maestrowf` can be tested as follows:

```
# cd into `multidimensional_sampling` directory
cd maestro_sheetmusic/multidimensional_sampling

# deactivate any existing python virtual environments
deactivate

# delete the `venv` virtual environment
/bin/rm -rf venv

# create a new `venv` virtual environment
python3 -m venv venv

# activate virtual environment
source venv/bin/activate

# install `maestro`, `scisample`, and dependencies
pip install -r requirements

# install local version of pytest
pip install pytest

# run local version of pytest (tests take ~30 seconds to run)
~/venv/bin/pytest
```
