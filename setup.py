from setuptools import find_packages, setup

setup(name='energyPATHWAYS',
      version='2021.4.1',
      description='Software package for long-term energy system modeling',
      url='https://github.com/energyPATHWAYS/energyPATHWAYS',
      author='Ben Haley, Ryan Jones, Michael Cohen, Gabe Kwok, Ana Mileva',
      packages=find_packages(),
      install_requires=['pandas',
                        'numpy',
                        'scipy',
                        'pint',
                        'pyomo',
                        'datetime',
                        'pytz',
                        'matplotlib', # util.py
                        'click',
                        'numpy_financial'
                        ],
      extras_require={'documentation': ["Sphinx"],
                      },
      include_package_data=True,
      entry_points={'console_scripts': ['energyPATHWAYS=energyPATHWAYS.run:click_run',
                                        'EP2RIO=energyPATHWAYS.export_to_rio:click_run']},
)
