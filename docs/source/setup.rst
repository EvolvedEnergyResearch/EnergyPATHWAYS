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

   **All prompt commands on Windows should be run in the Anaconda Prompt.**

Model outputs consist of large csv files that have been designed to work well with `Tableau <https://www.tableau.com/>`_.


Installation
============
EnergyPATHWAYS can be installed using the ``environment.yml`` file provided in the repository. This file contains all the necessary packages to run EnergyPATHWAYS. To install the environment, navigate to the directory containing the ``environment.yml`` file and run the following commands::

    $ cd EnergyPATHWAYS
    $ conda env create -f environment.yml

This will create a new environment called ``ep``. Then, activate the environment and install EnergyPATHWAYS::

    $ conda activate ep
    $ pip install -e .

Using the ``-e`` flag will install EnergyPATHWAYS inside your new ``ep`` conda environment in editable mode so that any changes to the code are reflected when running EnergyPATHWAYS without having to reinstall.

After running the setup script, the excel interface will be able to call the EnergyPATHWAYS model. It will also make the command line function ``energyPATHWAYS`` available.

.. tip::

    If you get permissions errors on a Windows machine during the installation process, right click on the Anaconda Prompt and select the option *Run as administrator*.

    If you encounter an error saying *ERROR: <folder name> does not appear to be a Python project: neither 'setup.py' nor 'pyproject.toml' found,* check to make sure you are in the correct directory. If you run ``ls`` (or ``dir`` on Windows) at the command prompt you should see the ``environment.yml`` and ``pyproj.toml`` files.

Additional Excel configuration
------------------------------

For Windows users
^^^^^^^^^^^^^^^

1. (Optional, **depreciated**) Install the ``xlwings`` Excel Add-in by running the following command in the terminal::
    
    (ep) $ xlwings addin install

Installing the xlwings addin will add a new ribbon tab to your Excel files. We have started using an "xlwings.conf" sheet in the scenario_builder.xlsm file instead of the ribbon tab.

2. Enter the "Conda path" and "Conda env" values on the "xlwings.conf" sheet of your scenario_builder.xlsm file. Find the path to your Conda "base environment" ::
   
   (ep) $ conda info

The Conda path should be something like ``C:\Users\Username\Anaconda3``. Copy this path to the "Conda path" field on your xlwings.conf sheet. Assuming you have followed installation instructions up to this point, use ``ep`` as the "Conda env".

.. note:: 
    The "Conda path" and "Conda env" variables will be used to activate your conda environment before running energyPATHWAYS. The "Start Runs" button in your scenario_builder.xlsm file will likely not work if you do not provide these values.
   
    For more information on using the Xlwings ribbon and "xlwings.conf" sheet, see the `xlwings addin documentation <https://docs.xlwings.org/en/latest/addin.html>`_.

3. Check that the "Interpreter_Win" value on the "xlwings.conf" sheet of your scenario_builder.xlsm file is either set to "python" or contains the path to your Python interpreter. Find the path to your Python interpreter by running the following command in the command prompt::

   (ep) $ where python

The Interpreter_Win path should be either ``python`` or something like ``C:\Users\Username\Anaconda3\envs\ep\python.exe``, where ``ep`` is the name of your conda environment. Copy this path to the "Interpreter_Win" field on your xlwings.conf sheet.

For MacOS users
^^^^^^^^^^^^^^^

1. Enter the "Interpreter_Mac" value on the "xlwings.conf" sheet of your scenario_builder.xlsm file. Find the path to your Python interpreter by running the following command in the terminal::

    (ep) $ which python

The Interpreter_Mac path should be something like ``/Users/Username/miniconda3/envs/ep/bin/python``. Copy this path to the "Interpreter_Mac" field on your xlwings.conf sheet.

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
    │   └── pyproj.toml
    ├── EP_interface
    │   ├── scenario_builder.py
    │   ├── scenario_builder.xlsm
    │   └── start_runs.sh
    ├── ep_db
    │   ├── ShapeData
    │   └── numerous csv files
    ├── ep_runs
    │   ├── my_scenario
    │   │   ├── config.INI
    │   │   └── runs_key.csv

Running the Model
===================

After installing EnergyPATHWAYS and setting up the necessary input data the model can be run from the command line::

    $ energyPATHWAYS [options]

To get help on the various command line options, use::

    $ energyPATHWAYS --help

In most cases, the Excel user interface, described in :doc:`Interface Section <interface>`, is the best way to interact with the model.