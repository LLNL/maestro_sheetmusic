
# Maestro Sheetmusic
[![Issues](https://img.shields.io/github/issues/LLNL/maestro_sheetmusic)](https://github.com/LLNL/maestro_sheetmusic/issues)
[![Forks](https://img.shields.io/github/forks/LLNL/maestro_sheetmusic)](https://github.com/LLNL/maestro_sheetmusic/network)
[![Stars](https://img.shields.io/github/stars/LLNL/maestro_sheetmusic)](https://github.com/LLNL/maestrowf/stargazers)
[![License](https://img.shields.io/badge/license-MIT-blue)](https://raw.githubusercontent.com/LLNL/maestro_sheetmusic/master/LICENSE)

This repository is a collection of example Maestro studies and code that can be used within workflows. The goal of these examples is to serve as a starting point for starting new Maestro examples and to illustrate some of the cases where Maestro can be used.

Some of the items in this repository:
- Sample specifications of complete multistep workflows
- Parameter generator (pgen) examples for executing various sampling techniques
- Both local and remote examples for running on super computers

## Maestro Workflow Conductor ([maestrowf](https://pypi.org/project/maestrowf/))

<img src="https://github.com/LLNL/maestrowf/raw/develop/assets/logo.png?raw=true" alt="Maestro Workflow Conductor: Orchestrate your workflows with ease!" title="Orchestrate your workflows with ease!" width="60%">

### Maestro Status
[![Build Status](https://travis-ci.org/LLNL/maestrowf.svg?branch=develop)](https://travis-ci.org/LLNL/maestrowf)
[![PyPI](https://img.shields.io/pypi/v/maestrowf.svg)](https://pypi.python.org/pypi?name=maestrowf&version=1.0.0&:action=display)
![Spack](https://img.shields.io/spack/v/py-maestrowf)

Maestro is a general purpose software tool that defines a YAML-based study specification for defining multistep workflows and automates execution of software flows on HPC resources. For more information, see the Maestro Workflow Conductor [repository](https://github.com/LLNL/maestrowf).

### Setting up your Python Environment and Installation

To get started, we recommend using virtual environments. If you do not have the
Python `virtualenv` package installed, take a look at their official [documentation](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/) to get started.

To create a new virtual environment:

    python -m virtualenv maestro_venv
    source maestro_venv/bin/activate

Once set up, test the environment. The paths should point to a virtual environment folder.

    which python
    which pip

Now, within your new environment, install the latest version of Maestro run

    pip install maestrowf

## Contributing Examples

If you'd like to contribute to these examples, please feel free to post a pull request. In order to contribute an example, please provide the following in a new directory for your example:
- a README that describes your example and provides installation instructions
- any standalone code needed to run your example
- whenever possible, a Maestro specification to run your example
- if your example provides code for pgen, specification generating, etc. please describe the process and what the code does and how it's used.

## Bugs, Questions, or Requests?

If you have any questions about Maestro itself or want to submit a feature request please [open a ticket](https://github.com/llnl/maestrowf/issues) on the Maestro Workflow Conductor [repository](https://github.com/llnl/maestrowf).

If you find that an example in this repository does not work or has a bug, please file an issue [here](https://github.com/llnl/maestro_sheetmusic/issues).

----------------
## Release
MaestroWF is released under an MIT license.  For more details see the
NOTICE and LICENSE files.

``LLNL-CODE-734340``