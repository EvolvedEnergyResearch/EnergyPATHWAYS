from energyPATHWAYS import config
from energyPATHWAYS import shapes2
from energyPATHWAYS import util
from energyPATHWAYS import pathways_model

from .generated.ep_db_loader import _Metadata, EnergyPathwaysDatabase

#
# These methods form the API between a subclass of CsvDatabase and the validation subsystem.
#
def get_metadata():
    return _Metadata

def database_class():
    return EnergyPathwaysDatabase
