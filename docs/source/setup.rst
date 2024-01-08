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

EnergyPATHWAYS has been tested with **Python 3.10**. We recommend downloading a specific Anaconda Distribution of python, which can be found here: `<https://repo.anaconda.com/archive/Anaconda3-2023.03-1-Windows-x86_64.exe>`_

.. Note::
   EnergyPATHWAYS has been developed and tested on Microsoft Windows and the interface requires Microsoft Excel for the interface.

Model outputs consist of large csv files that have been designed to work well with `Tableau <https://www.tableau.com/>`_.


Installation
============

.. Note::
   EnergyPATHWAYS requires the csvdb library, which is not currently on PyPI and therefore won't be installed when running the setup script. It can be downloaded here: `<https://github.com/EvolvedEnergyResearch/csvdb>`_

EnergyPATHWAYS can be installed using Python's setuptools.

After cloning the EnergyPATHWAYS repository::

    > python setup.py develop

After running the setup script, the excel interface will be able to call the EnergyPATHWAYS model.

.. topic:: Troubleshooting

    Running setup.py develop will often give permissions errors. To address this, it is recommended that you right click on the command prompt and select the option *Run as administrator*.

    If you encounter an error saying *python: can't open file 'setup.py': [Errno 2] No such file or directory,* check to make sure you are in the correct directory.

Folder Organization
===================
You can place EnergyPATHWAYS anywhere you want on your computer. However, we would recommend the following organization:

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
