===============
Getting Started
===============

Overview
========

A working EnergyPATHWAYS installation consists of four main parts:

1. EnergyPATHWAYS code
2. csvd python package
3. Excel interface
4. CSV file database

Dependencies
============

EnergyPATHWAYS has been tested with **Python 3.10**. If you use Windows and do not already have a conda/Andacond installation, we recommend downloading a specific Anaconda Distribution of python, which can be found here: `<https://repo.anaconda.com/archive/Anaconda3-2023.03-1-Windows-x86_64.exe>`_

If you want a smaller conda installation or are not on windows, feel free to download and install the `most recent version of Miniconda <https://docs.anaconda.com/free/miniconda/>`_ for your operating system. 

.. Note::
   EnergyPATHWAYS has been developed and tested primarily on Microsoft Windows and the interface requires Microsoft Excel. Some of the Excel interface features can be used on a Mac, and a shell script is now available to run cases on Mac or Linux.

Model outputs consist of large csv files that have been designed to work well with `Tableau <https://www.tableau.com/>`_.


Installation
============
EnergyPATHWAYS can be installed using the ``environment.yml`` file provided in the repository. This file contains all the necessary packages to run EnergyPATHWAYS. To install the environment, navigate to the directory containing the ``environment.yml`` file and run the following commands::

    $ cd EnergyPATHWAYS
    $ conda env create -f environment.yml -n ep

This will create a new environment called ``ep``. Then, activate the environment and install EnergyPATHWAYS::

    $ conda activate ep
    $ pip install -e .

Alternatively, EnergyPATHWAYS can be installed using Python's setuptools.

After cloning the EnergyPATHWAYS repository::

    > python setup.py develop

After running the setup script, the excel interface will be able to call the EnergyPATHWAYS model.

.. topic:: Troubleshooting

    Running setup.py develop will often give permissions errors. To address this, it is recommended that you right click on the command prompt and select the option *Run as administrator*.

    If you encounter an error saying *ERROR: <folder name> does not appear to be a Python project: neither 'setup.py' nor 'pyproject.toml' found,* check to make sure you are in the correct directory.

Data Setup
==========

In addition to installation of the EnergyPATHWAYS package described above, a model cannot be run until input data are provided. The input data consist of three components:

1. A database describing your energy system
2. A configuration file (e.g. ``config.INI``)
3. A runs_key.csv file that describes the variations of your energy system that you would like to model.

The first two of these are described below, and the third is covered in detail unde

Workspace Organization
======================
You can place EnergyPATHWAYS anywhere you want on your computer. We find that a folder structure similar to what is below makes for a clean workspace for EnergyPATHWAYS.

::

    Some-Date-EP_model
    ├── EnergyPATHWAYS
    │   ├── EnergyPATHWAYS
    │   └── setup.py
    ├── csvdb
    │   ├── numerous folders
    │   └── setup.py
    ├── EP_interface
    │   ├── scenario_builder.py
    │   └── scenario_builder.xlsm
    ├── ep_db
    │   ├── ShapeData
    │   └── numerous csv files
    ├── ep_runs
    │   ├── my_scenario
    │   │   └── config.INI
    │   │   └── runs_key.csv

Running the Model
===================

After installing EnergyPATHWAYS and setting up the necessary input data the model can be run from the command line::

    $ energyPATHWAYS [options]

To get help on the various command line options, use::

    $ energyPATHWAYS --help

In most cases, the user interface, described in :doc:`Interface Section <interface>`, is the best way to interact with the model.