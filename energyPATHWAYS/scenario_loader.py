

import json
import os
import logging
import itertools
from collections import defaultdict
import pdb
import pandas as pd
import six
from energyPATHWAYS.util import csv_read_table
from csvdb.data_object import get_database
from csvdb.error import ScenarioFileError
from csvdb.scenario import AbstractScenario, CsvdbFilter

SCENARIO_FILE = 'runs_key.csv'
INDEX_DIVIDER = '--'

class Scenario(AbstractScenario):
    MEASURE_CATEGORIES = {"DemandEnergyEfficiencyMeasures",
                          "DemandFuelSwitchingMeasures",
                          "DemandServiceDemandMeasures",
                          "DemandSalesShareMeasures",
                          "DemandStockMeasures",}

    def __init__(self, scenario_name, dirpath=None):
        dirpath = dirpath or os.getcwd()

        self._id = scenario_name
        self._bucket_lookup = self._load_bucket_lookup()

        self._measures = {category: defaultdict(list) for category in self.MEASURE_CATEGORIES}
        self._sensitivities = defaultdict(dict)

        # N.B. self.pathname is set in super's __init__()
        super(Scenario, self).__init__(scenario_name, dirpath, 'csv', filename=SCENARIO_FILE)

    # Required subclass method, called by AbstractScenario
    def load(self):
        df = pd.read_csv(self.pathname, index_col=0)
        df.fillna('', inplace=True)
        db = get_database()

        # TODO: (RJP) discuss with Ryan. Not sure this is still relevant.
        # Special case where there are no sensitivity columns. We assume the user just
        # wants a sensitivity with all the reference selections.
        if df.shape == 1:
            df['reference'] = ''

        try:
            scenario_data = df[self.name]

        except KeyError:
            raise ScenarioFileError(self.pathname, "Scenario '{}' not found.".format(self.name))

        for key, sens_name in scenario_data.items():
            # TODO (RJP): skip measures with no value in the current sensitivity column?
            if sens_name == '':
                continue

            parts = key.split(INDEX_DIVIDER)
            tbl_name = parts[0]

            if tbl_name in self.MEASURE_CATEGORIES:
                if len(parts) != 3:
                    raise ValueError("Expected measure to have 3 parts delimited by '--', got {}".format(parts))

                idx_value = parts[1]
                tbl_key   = parts[2]
                self._add_measure(tbl_name, tbl_key, idx_value)

            else: # sensitivity scenario
                tbl_key = parts[1] if db.table_metadata(tbl_name).has_key_col else None
                constraints = dict([tuple(c.split(':')) for c in parts[2:]])
                sorted_constraints = list((key, constraints[key]) for key in sorted(constraints.keys()))
                self._add_sensitivity(tbl_name, tbl_key, sens_name, sorted_constraints)

    def _add_sensitivity(self, tbl_name, tbl_key, sens_name, constraints):
        obj = CsvdbFilter(tbl_name, tbl_key, sens_name, constraints)
        self.add_filter(obj)

    def _add_measure(self, tbl_name, measure, idx_value):
        try:
            bucket_id = self._bucket_lookup[tbl_name][measure]
        except KeyError:
            raise ValueError(
                "{} scenario wants to use {} {} but no such measure was found in the database.".format(self._id,
                                                                                                       tbl_name,
                                                                                                       measure))
        if measure in self._measures[tbl_name][bucket_id]:
            raise ValueError("Scenario uses {} {} more than once.".format(tbl_name, measure))

        self._measures[tbl_name][bucket_id].append(measure)

    def _load_sensitivity(self, filter):
        db = get_database()

        table       = filter.table_name
        name        = filter.key_value
        sensitivity = filter.sens_value

        if name in self._sensitivities[table]:
            raise ValueError("Scenario specifies sensitivity for {} {} more than once".format(table, name))

        # Check that the sensitivity actually exists in the database before using it
        md = db.table_metadata(table)

        # TODO: (RJP) Why aren't explicit constraints applied here?
        filters = {'sensitivity' : sensitivity, md.key_col : name}
        data = csv_read_table(table, **filters)

        if data is None or len(data) == 0:
            raise ValueError("Could not find sensitivity '{}' for {} {}.".format(sensitivity, table, name))

        self._sensitivities[table][name] = sensitivity

    @staticmethod
    def _index_col(measure_table):
        """Returns the name of the column that should be used to index the given type of measure"""
        if measure_table.startswith('Demand'):
            return 'subsector'
        elif measure_table == "BlendNodeBlendMeasures":
            return 'blend_node'
        else:
            return 'supply_node'

    @staticmethod
    def _subindex_col(measure_table):
        """Returns the name of the column that subindexes the given type of measure, i.e. the technology id column"""
        if measure_table in ("DemandSalesShareMeasures", "DemandStockMeasures"):
            return 'demand_technology'
        elif measure_table in ("SupplySalesMeasures", "SupplySalesShareMeasures", "SupplyStockMeasures"):
            return 'supply_technology'
        else:
            return None

    def _load_bucket_lookup(self):
        """
        Returns a dictionary matching each measure_id to the combination of subsector and technology
        that it applies to. If the measure does not apply to a technology, the second member of tuple is None.
        """
        from energyPATHWAYS.util import table_data

        lookup = defaultdict(dict)

        for table in self.MEASURE_CATEGORIES:
            index_col = self._index_col(table)
            subindex_col = self._subindex_col(table)
            col_names = ['name', index_col] + ([subindex_col] if subindex_col else [])
            num_cols = len(col_names)

            tbl_dict = lookup[table]
            tup_iter = table_data(table, column_names=col_names, as_tup_iter=True)

            for row in tup_iter:
                tbl_dict[row[0]] = (row[1], row[2] if num_cols == 3 else None)

        return lookup

    def get_measures(self, category, subsector_or_node_id, tech_id=None):
        """
        This method is pretty self-explanatory, but note the implicit validation: If the user requests an unknown
        category, a KeyError will be raised because the top level of this stricture is a regular dict. If they
        request a combination of subsector and technology that happens to have no measures for that
        category, an empty list will be returned because the second layer is a defaultdict.

        Note also that if tech_id is None, the only measure_ids returned will be those that pertain to the
        subsector as a whole, and not to any individual technology.
        """
        measure_ids = self._measures[category][(subsector_or_node_id, tech_id)]

        # Log when measure_ids are found
        if measure_ids:
            log_msg = "{} {} loaded for {} {}".format(
                category, measure_ids, self._index_col(category), subsector_or_node_id
            )
            if tech_id:
                log_msg += " and {} {}".format(self._subindex_col(category), tech_id)
            logging.debug(log_msg)

        return measure_ids

    def all_measure_ids_by_category(self):
        # This list(itertools...) nonsense is just to flatten to a single list from a list-of-lists
        return {category: list(itertools.chain.from_iterable(contents.values()))
                for category, contents in self._measures.items()}
