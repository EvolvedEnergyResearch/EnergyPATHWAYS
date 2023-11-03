# -*- coding: utf-8 -*-
__author__ = 'Michael'

import unittest
import mock
import energyPATHWAYS
from energyPATHWAYS.util import *


def read_table(table_name, column_names='*', return_unique=False, return_iterable=False, **filters):
    if table_name == 'IDMap' and column_names == 'identifier_id, ref_table':
        return [(u'supply_type_id', u'SupplyTypes'), (u'ghg_id', u'GreenhouseGases')]
    elif table_name == 'SupplyTypes' and column_names == 'id, name':
        return [(1, u'Blend'), (2, u'Conversion'), (3, u'Delivery'), (4, u'Import'), (5, u'Primary'), (6, u'Storage')]
    elif table_name == 'GreenhouseGases' and column_names == 'id, name':
        return [(1, u'CO2'), (2, u'CH4'), (3, u'N2O')]

    # if we've gotten this far without returning, something is amiss
    raise ValueError("Mock doesn't know how to provide this table read: " +
                     str(table_name) + ", " + str(column_names) + ", " + str(filters))

mock_sql_read_table = mock.create_autospec(csv_read_table, side_effect=read_table)

