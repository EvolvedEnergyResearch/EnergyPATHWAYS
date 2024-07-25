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
First download the EnergyPATHWAYS code from the `EnergyPATHWAYS GitHub repository <https://github.com/EvolvedEnergyResearch/EnergyPATHWAYS>`_ either by downloading the zip file or by cloning the repository using git::

    $ git clone https://github.com/EvolvedEnergyResearch/EnergyPATHWAYS

.. Note::
    If you are using a Windows machine and do not have git installed, you can download the repository as a zip file and proceed with the installation. If you would like install git on your machine, you can download it from `here <https://git-scm.com/download/win>`_.

Once you have downloaded the code, EnergyPATHWAYS can be installed using the ``environment.yml`` file provided in the repository. This file contains all the necessary packages to run EnergyPATHWAYS. To install the environment, navigate to the directory containing the ``environment.yml`` file and run the following commands::

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

Once the installation is complete, before running EnergyPATHWAYS, you will need to set up the EP interface and the data files. The following sections describe how to perform these steps.

1. EP Interface setup
---------------------

EnergyPATHWAYS comes with a user interface that allows users to create, load and run scenarios. It contains two main files:

- `scenario_builder.xlsm`: An Excel file with the commands to run the model.
- `scenario_builder.py`: A python script with main functions to interact with the model.

See the :ref:`User Interface` section for more information. 

To set up the EP interface, follow these steps:

1. Copy the `EP interface` folder outside of EnergyPathways main folder to the working directory. 
2. Open the `scenario_builder.xlsm` file and enable macros.
3. Setup the `xlwings.conf` sheet in the `scenario_builder.xlsm` file to point to the conda environment you created in the previous step. This step is different for Windows and MacOS users:

    **For Windows users**

    Enter the "Interpreter_Win", "Conda path" and "Conda env" values on the "xlwings.conf" sheet of your scenario_builder.xlsm file. Find the path to your Conda "base environment" ::

        (ep) $ conda info

    The Conda path should be something like ``C:\Users\Username\Anaconda3``. Copy this path to the "Conda path" field on your xlwings.conf sheet. Assuming you have followed installation instructions up to this point, use ``ep`` as the "Conda env" and ``python`` as the "Interpreter_Win" values.

    .. note:: 
        The "Conda path" and "Conda env" variables will be used to activate your conda environment before running energyPATHWAYS. The "Start Runs" button in your scenario_builder.xlsm file will likely not work if you do not provide these values.

    The xlwings.conf sheet should be similar to this (replace "Username" with your actual username):

        +-----------------+--------------------------------+
        | Interpreter_Win | python                         |
        +-----------------+--------------------------------+
        | Conda Path      | C:\\Users\\Username\\Anaconda3 |
        +-----------------+--------------------------------+
        | Conda Env       | ep                             |
        +-----------------+--------------------------------+

    **For MacOS users**

    Enter the "Interpreter_Mac" value on the "xlwings.conf" sheet of your scenario_builder.xlsm file. Find the path to your Python interpreter by running the following command in the terminal::

        (ep) $ which python

    The Interpreter_Mac path should be something like ``/Users/Username/miniconda3/envs/ep/bin/python``. Copy this path to the "Interpreter_Mac" field on your xlwings.conf sheet.

    The xlwings.conf sheet should be similar to this (replace "Username" with your actual username):

        +-----------------+------------------------------------------------+
        | Interpreter_Mac |  /Users/Username/miniconda3/envs/ep/bin/python |
        +-----------------+------------------------------------------------+

    With the EP conda environment activated in the terminal, run the following command to finalize the installation of the xlwings package::

        (ep) $ xlwings runpython install

2. Data Setup
-------------

In addition to installation of the EnergyPATHWAYS package described above, a model cannot be run until input data are provided. The input data consist of three components:

1. A database describing your energy system
2. A configuration file (e.g. ``config.INI``)
3. A runs_key.csv file that describes the variations of your energy system that you would like to model.

To import scenario data into the model, make sure to edit the ``database_path`` variable in the ``config.INI`` file to point to the directory where the database has been placed.

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

    (ep) $ energyPATHWAYS [options]

To get help on the various command line options, use::

    (ep) $ energyPATHWAYS --help

In most cases, the Excel user interface, described in :doc:`Interface Section <interface>`, is the best way to interact with the model.

Uninstall EnergyPATHWAYS
========================


To uninstall EnergyPATHWAYS, deactivate the environment and remove it::

    (ep) $ conda deactivate
    (base) $ conda remove -n ep --all

Delete the EnergyPATHWAYS repository from your local computer and the EP interface folder.