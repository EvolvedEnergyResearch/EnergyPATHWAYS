===============
Getting Started
===============

Overview
========

A working EnergyPATHWAYS installation consists of three main parts:

1. Python code or executable files
2. Excel interface
3. CSV file database

Dependencies
============

Before completing the installation we need to install Python. EnergyPATHWAYS requires **Python 3.8**. We recommend downloading the Anaconda Distribution of python, which can be found here: `<https://www.anaconda.com/products/individual>`_

.. Note::
   EnergyPATHWAYS has been developed and tested on Microsoft Windows and the interface requires Microsoft Excel for the interface.

Model outputs consist of large csv files that have been designed to work well with `Tableau <https://www.tableau.com/>`_. We recommend purchasing a license for use in conjunction with EnergyPATHWAYS.

Third Party Libraries
---------------------
The EnergyPATHWAYS code requires numerous third party libraries. These do not need to be manually installed by the user and either come build into the Anaconda Python distribution, or will be installed when the setup scripts are called (see `Installation`_), or come pre-packaged in executable files. A list of the third party libraries used in EnergyPATHWAYS is provided below:

* pandas
* numpy
* scipy
* pint
* datetime
* pytz
* matplotlib
* click

Installation
============

.. Note::
   The instructions below are only required if you do not have packaged executable files. If you have packaged executables, you can skip these steps and move to the next section.

Once the dependencies are installed, EnergyPATHWAYS can be installed using Python's setuptools.

The first step is to install a library called csvdb that is distributed alongside EnergyPATHWAYS. Open a windows command prompt from the csvdb directory and run the following command::

    > python setup.py develop

Once finished, navigate to the EnergyPATHWAYS directory and run the same command.

.. Note::
   Setuptools will attempt to install any required packages that are not in your environment when you run ``setup.py``. However, we have found that this method does not reliably install all dependencies on all platforms. This is why we recommend using Anaconda to set up the environment before installing EnergyPATHWAYS, as described under `Dependencies`_, above.

.. topic:: Troubleshooting

    Running setup.py develop will often give permissions errors. To address this, it is recommended that you right click on the command prompt and select the option *Run as administrator*.

    If you encounter an error saying *python: can't open file 'setup.py': [Errno 2] No such file or directory,* check to make sure you are in the correct directory.

Folder Organization
===================
You can place EnergyPATHWAYS anywhere you want on your computer. However, we recommend not changing or moving files within the folder structures. We would recommend the following organization:

::

    Some-Date-EP_model
    ├── EP
    │   ├── EnergyPATHWAYS
    │   └── setup.py
    ├── csvdb
    │   ├── numerous folders
    │   └── setup.py
    ├── EP_interface
    │   ├── scenario_builder.py
    │   └── scenario_builder.xlsm
    ├── ep_db_us_2021
    │   ├── ShapeData
    │   └── numerous csv files
    ├── EP_runs
    │   ├── 2021EER
    │   │   └── config.INI
    │   │   └── runs_key.csv
    │   ├── your_custom_scenario
    │   │   └── config.INI
    │   │   └── runs_key.csv