# TwinPy

[![CodeFactor](https://www.codefactor.io/repository/bitbucket/ctw-bw/twinpy/badge?s=a7ae9b43e3ce8764663908b3985134f45c98052a)](https://www.codefactor.io/repository/bitbucket/ctw-bw/twinpy)
[![Documentation Status](https://readthedocs.org/projects/twinpy/badge/?version=latest)](https://twinpy.readthedocs.io/en/latest/?badge=latest)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![codecov](https://codecov.io/bb/ctw-bw/twinpy/branch/master/graph/badge.svg?token=DEHFOCVJY9)](https://codecov.io/bb/ctw-bw/twinpy)

This repository contains a GUI made in Python to interface with Simulink models in TwinCAT.

It has two main functions: maps to Simulink models can be created, and linked to TwinCAT, and GUI widgets that read and write from those.

Interfacing with TwinCAT is done through ADS, the variable sharing service.

API documentation can be found here: https://twinpy.readthedocs.io/en/latest/

A complete example of a TwinPy GUI can be found here: https://bitbucket.org/ctw-bw/twinpy-gui-demo. This example does not use Simulink, and instead uses a very simple PLC script, which variables end up in the ADS pool. 

## Your own custom GUI

TwinPy is designed as a library. So your own application should incorporate it instead of modifying it.

To customize a GUI for your application, you can extend the `BaseGUI` or `TcMainWindow` class with your own. To maintain clean version control, create your own repository and load this base repo as a git submodule.

### Starting your own GUI

A repository has been cloned or initialized.

 1. Add TwinPy as a submodule by running:
       * `git submodule add https://bitbucket.org/ctw-bw/twinpy.git`
 2. Create and activate a virtual environment if none exists yet:
       * `python -m venv venv`
       * `venv\Scripts\activate`
 3. Now install the TwinPy submodule in the virtual environment:
       * `pip install -e twinpy`
            * This will create a link from the TwinPy source, so it is available everywhere (inside that venv)
 4. To install other dependencies, copy `./twinpy/requirements.txt` to `./requirements.txt` and run
       * `pip install -r requirements.txt`
 5. Now create your own application, extending `twinpy.ui.BaseGUI` or `twinpy.ui.TcMainWindow`
     * You can also copy the source of `BaseGUI` and `__main__.py` to your own application to get you started.

## Install package

Install TwinPy via pip:

```pip install twinpy```

### From source

After cloning this repository (stand-alone or as a submodule), run the following in a command window (from the virtual environment):

```
pip install -e ./twinpy
```

This will install the package from local source. The `-e` flag keeps the original source editable, which is convenient during development.

It is recommended to install a local package like twinpy only in a virtual environment. 

## Getting started

This explains how to run the given TwinPy example with the WE2 Simulink models. This is not applicable to a custom GUI or custom models. Use this getting-started as a check to see if your system is ready.

 1. To run from a virtual environment (recommended), open a terminal in this directory and run: `python -m venv venv` (use a full path to select a different Python version). A virtual environment is now created.
 2. Run `venv/Scripts/Activate.ps1` for PowerShell or `venv/Scripts/activate.bat` for CMD. Your terminal should now show a '(venv)' prefix, the environment has been activated.
 4. Install the regular packages with `python -m pip install -r requirements.txt`
 5. You can now run `python -m twinpy`

In case you do not want to use a virtual environment, just skip steps 1 and 2.

## Run with active terminal

By default `app.exec()` is a hanging command that fires up the main event loop of the GUI. It will prevent the script from exiting when the application is still open. When running the GUI from a terminal, you cannot interact with the active objects untill the GUI was closed.

Pyzo has a way around this. If you run the script from a shell with 'gui' set to "PyQt5" you can disable the `app.exec()` line. The interpreter will handle the QT event loop elsewhere, freeing up the Python console for you to use.

## TwinCAT Interface

Interfacing with TwinCAT starts with the SimulinkModel object. It points to a Simulink object running in TwinCAT. You can address parts of the model in a hierarchical way, based on the hierarchy in the original Simulink model:

```
model = SimulinkModel(...)
const_block = model.MySubSystem.OtherSubSystem.MyConstBlock
```

Parameters are listed as properties of blocks. Use `get()` and `set()` to read and write those parameters:

```
val = model.MySubSystem.OtherSubSystem.MyConstBlock.Value.get()
# A Constant block only has one parameter, named `Value`
```

If a block only has a single parameter or signal, you can also use `get()` and `set()` directly on the block:

```
val = model.MySubSystem.OtherSubSystem.MyConstBlock.get()  # Same result as above
```

Signals are named `si{n}` and `so{n}` for input and output signals, numbered in the order determined by Simulink. Parameters are named after their Simulink name.

## Docs ##

Documentation from the source can be compiled using sphinx:

```
cd docs
make html
```

Note: if you get an error about e.g. missing the pyads package because you use a virtual environment, install sphinx inside the virtual environment too. 

Documentation is automatically built and hosted on readthedocs.io: 

## Tests ##

See the `tests/` directory for unit tests and some run scripts. The tests are made with the `unittest` framework. Run all tests with:

```shell
python -m unittest
```

Some tests rely on the pyads test server. This test server unfortunately does not work with Windows. When on a Windows system, use Linux subsystem for Windows, a virtual machine or Docker. Look for the pyads documentation or the pyads [Contributing.md](https://github.com/stlehmann/pyads/blob/master/CONTRIBUTING.md#testing) for more info.

### PyQt ###

When running the tests without an actual screen (like SSH terminal or in a pipeline) PyQt will throw a fatal error. The widgets cannot be created without a screen. There a couple of workarounds for this:

 * Include the Qt option `-platform minimal` option: run `python -m unittest -platform minimal`
 * Set a debug environment variable: `export QT_QPA_PLATFORM=offscreen`
 * Use a virtual X server: `xvfb-run python -m unittest`
