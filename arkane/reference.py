#!/usr/bin/env python
# -*- coding: utf-8 -*-

###############################################################################
#                                                                             #
# RMG - Reaction Mechanism Generator                                          #
#                                                                             #
# Copyright (c) 2002-2019 Prof. William H. Green (whgreen@mit.edu),           #
# Prof. Richard H. West (r.west@neu.edu) and the RMG Team (rmg_dev@mit.edu)   #
#                                                                             #
# Permission is hereby granted, free of charge, to any person obtaining a     #
# copy of this software and associated documentation files (the 'Software'),  #
# to deal in the Software without restriction, including without limitation   #
# the rights to use, copy, modify, merge, publish, distribute, sublicense,    #
# and/or sell copies of the Software, and to permit persons to whom the       #
# Software is furnished to do so, subject to the following conditions:        #
#                                                                             #
# The above copyright notice and this permission notice shall be included in  #
# all copies or substantial portions of the Software.                         #
#                                                                             #
# THE SOFTWARE IS PROVIDED 'AS IS', WITHOUT WARRANTY OF ANY KIND, EXPRESS OR  #
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,    #
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE #
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER      #
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING     #
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER         #
# DEALINGS IN THE SOFTWARE.                                                   #
#                                                                             #
###############################################################################

"""
This module defines the ReferenceSpecies class, which are used in isodesmic reaction calculations

"""

from __future__ import print_function, division

import logging
import os
from collections import namedtuple

import yaml

from arkane.common import ArkaneSpecies, ARKANE_CLASS_DICT
from arkane.isodesmic import ErrorCancelingSpecies
from rmgpy import settings
from rmgpy.molecule import Molecule
from rmgpy.rmgobject import RMGObject
from rmgpy.species import Species
from rmgpy.statmech import Conformer
from rmgpy.thermo import ThermoData


class ReferenceSpecies(ArkaneSpecies):
    """
    A class for storing high level reference data and quantum chemistry calculations for a variety of model chemistry
    selections for use in isodesmic reaction calculations
    """

    def __init__(self, species=None, smiles=None, adjacency_list=None, inchi=None, reference_data=None,
                 calculated_data=None, preferred_reference=None, index=None, label=None, cas_number=None,
                 symmetry_number=None, default_xyz_chemistry=None, **kwargs):
        """
        One of the following must be provided: species, smiles, adjacency_list, inchi.

        Args:
            species (rmgpy.molecule.Species): Molecule object representing the reference species
            smiles (str): SMILES string representing the reference species
            adjacency_list (str): An RMG adjacency list representation of the reference species
            inchi (str): InChI string representing the reference species
            reference_data (dict): Formatted as {'source_string': ReferenceDataEntry, ...}
            calculated_data (dict): Formatted as {'model_chemistry': CalculatedDataEntry, ...}
            preferred_reference (str): The source string key for the reference data to use for isodesmic reactions
            index (int): Index of this species in the database of reference species located at
                `RMG-database/input/reference_sets/`
            label (str): A user defined label for easily identifying the species
            cas_number (str): CAS number associated with the reference species
            symmetry_number (int): The true symmetry number of the species (if not provided will default to the number
                calculated by RMG)
            default_xyz_chemistry (str): The model chemistry that should be used to get the default XYZ coordinates for
                this species.
            **kwargs: Arguments passed to the parent ArkaneSpecies class when loading from a YAML file. Not intended for
                user input
        """

        if species is None:
            if smiles:
                species = Species(SMILES=smiles)
            elif inchi:
                species = Species(InChI=inchi)
            elif adjacency_list:
                species = Species().fromAdjacencyList(adjacency_list)
            else:
                raise ValueError('Either an rmgpy species object, smiles string, InChI string, or an adjacency list '
                                 'must be given to create a ReferenceSpecies object')

        super(ReferenceSpecies, self).__init__(species=species, label=label, **kwargs)

        self.reference_data = reference_data
        self.calculated_data = calculated_data
        self.index = index
        self.cas_number = cas_number
        self.preferred_reference = preferred_reference
        self.default_xyz_chemistry = default_xyz_chemistry

        # Alter the symmetry number calculated by RMG to the one provided by the user
        if symmetry_number:
            self.symmetry_number = symmetry_number

    def __repr__(self):
        if self.index:
            label = '{0}({1})'.format(self.smiles, self.index)
        else:
            label = '{0}'.format(self.smiles)

        return '<ReferenceSpecies {0}>'.format(label)

    @property
    def reference_data(self):
        return self._reference_data

    @reference_data.setter
    def reference_data(self, value):
        if not value:
            self._reference_data = {}
        elif isinstance(value, dict):
            if all(isinstance(source, str) for source in value.keys()):
                if all(isinstance(data_entry, ReferenceDataEntry) for data_entry in value.values()):
                    self._reference_data = value
        else:
            raise ValueError('Reference data must be given as a dictionary of the data source (string) and associated '
                             'ReferenceDataEntry object')

    @property
    def calculated_data(self):
        return self._calculated_data

    @calculated_data.setter
    def calculated_data(self, value):
        if not value:
            self._calculated_data = {}
        elif isinstance(value, dict):
            if all(isinstance(source, str) for source in value.keys()):
                if all(isinstance(data_entry, CalculatedDataEntry) for data_entry in value.values()):
                    self._calculated_data = value
        else:
            raise ValueError('Calculated data must be given as a dictionary of the model chemistry (string) and '
                             'associated CalculatedDataEntry object')

    def load_yaml(self, path, label=None, pdep=False):
        """
        Load a ReferenceSpecies object from a YAML file.

        Args:
            path (str): Location on disk of the YAML file
            label: Unused argument from parent class ArkaneSpecies
            pdep: Unused argument from parent class ArkaneSpecies
        """
        with open(path, 'r') as f:
            data = yaml.safe_load(stream=f)

        if data['class'] != 'ReferenceSpecies':
            raise ValueError('Cannot create ReferenceSpecies object from yaml file {0}: object defined by this file is'
                             'not a ReferenceSpecies object'.format(path))

        data = {key: data[key] for key in data.keys() if key != 'class'}
        class_dict = ARKANE_CLASS_DICT
        class_dict['ReferenceDataEntry'] = ReferenceDataEntry
        class_dict['CalculatedDataEntry'] = CalculatedDataEntry

        self.make_object(data, class_dict)

    def update_from_arkane_spcs(self, arkane_species):
        """
        Add in calculated data from an existing ArkaneSpecies object.

        Notes:
            If the model chemistry already exists then this calculated data will be overwritten by the data contained
            in arkane_species

        Args:
            arkane_species (ArkaneSpecies):  Matching Arkane species that was run at the desired model chemistry
        """
        conformer = arkane_species.conformer
        thermo_data = arkane_species.thermo_data
        calc_data = CalculatedDataEntry(conformer, thermo_data,)
        self.calculated_data[arkane_species.level_of_theory] = calc_data

    def to_error_canceling_spcs(self, model_chemistry, source=None):
        """
        Extract calculated and reference data from a specified model chemistry and source and return as a new
        ErrorCancelingSpecies object

        Args:
            model_chemistry (str): Model chemistry (level of theory) to use as the low level data
            source (str): Reference data source to take the high level data from

        Raises:
            KeyError: If `model_chemistry` is not available for this reference species

        Returns:
            ErrorCancelingSpecies
        """
        if model_chemistry not in self.calculated_data:
            raise KeyError('Model chemistry `{0}` not available for species {1}'.format(model_chemistry, self))

        molecule = Molecule(SMILES=self.smiles)

        reference_enthalpy = self.get_reference_enthalpy(source=source)
        low_level_h298 = self.calculated_data[model_chemistry].thermo_data.H298.__reduce__()[1]

        return ErrorCancelingSpecies(
            molecule, low_level_h298, model_chemistry,
            high_level_hf298=reference_enthalpy.h298,
            source=reference_enthalpy.source
        )

    def get_reference_enthalpy(self, source=None):
        """
        Extract reference data from a specified source

        Notes:
            If no source is given, the preferred source for this species. If the `preferred_source` attribute is not set
            then the preferred source is taken as the source with the lowest non-zero uncertainty

        Args:
            source (str): Reference data source to take the high level data from

        Raises:
            ValueError: If there is no reference data for this reference species

        Returns:
            ScalarQuantity
        """
        if not self.reference_data:
            raise ValueError('No reference data is included for species {0}'.format(self))

        ReferenceEnthalpy = namedtuple('ReferenceEnthalpy', ['h298', 'source'])
        preferred_source = source

        if preferred_source is None:
            # Find the preferred source
            if self.preferred_reference is not None:
                preferred_source = self.preferred_reference
            else:  # Choose the source that has the smallest uncertainty
                sources = self.reference_data.keys()
                data = self.reference_data.values()
                preferred_source = sources[0]  # If all else fails, use the first source as the preferred one
                uncertainty = data[0].thermo_data.H298.uncertainty_si
                for i, entry in enumerate(data):
                    if (entry.thermo_data.H298.uncertainty_si > 0) and \
                            (entry.thermo_data.H298.uncertainty_si < uncertainty):
                        uncertainty = entry.thermo_data.H298.uncertainty_si
                        preferred_source = sources[i]

        return ReferenceEnthalpy(
            self.reference_data[preferred_source].thermo_data.H298.__reduce__()[1],
            preferred_source
        )

    def get_default_xyz(self):
        """
        Return the XYZ coordinates of the default geometry for this species for use as a starting point for other
        quantum chemistry calculations

        Notes:
            The attribute `default_xyz_chemistry` must be set for this reference species, preferable to a model
            chemistry with a highly accurate equilibrium geometry

        Returns:
            dict: {'numbers': np.ndarray, 'coords': np.ndarray} Coordinates are returned in angstroms
        """
        if self.default_xyz_chemistry:
            conformer = self.calculated_data[self.default_xyz_chemistry].conformer
            xyz_data = {'numbers': conformer.number.value_si, 'coords': conformer.coordinates.value_si * (10.0 ** 10.0)}
            return xyz_data

        else:
            raise ValueError('The default model chemistry to use for XYZ coordinates has not been set '
                             'for {0}'.format(self))


class ReferenceDataEntry(RMGObject):
    """
    A class for storing reference data for a specific species from a single source
    """
    def __init__(self, thermo_data, atct_id=None):
        """

        Args:
            thermo_data (rmgpy.thermo.ThermoData): Thermochemistry (Hf298, Cp, ...) from the reference for a species
            atct_id (str): ID number in the Active Thermochemical Tables if the source is ATcT
        """
        super(ReferenceDataEntry, self).__init__()
        self.thermo_data = thermo_data
        self.atct_id = atct_id

    def __repr__(self):
        return str(self.as_dict())

    @property
    def thermo_data(self):
        return self._thermo_data

    @thermo_data.setter
    def thermo_data(self, value):
        if value:
            if isinstance(value, ThermoData):
                self._thermo_data = value
            else:
                raise ValueError('thermo_data for a ReferenceDataEntry object must be an rmgpy ThermoData instance')
        else:
            self._thermo_data = None


class CalculatedDataEntry(RMGObject):
    """
    A class for storing a single entry of statistical mechanical and thermochemistry information calculated at a single
    model chemistry or level of theory
    """
    def __init__(self, conformer, thermo_data, t1_diagnostic=None, fod=None):
        """

        Args:
            conformer (rmgpy.statmech.Conformer): Conformer object generated from an Arkane job. Stores many peices of
                information gained from quantum chemistry calculations, including coordinates, frequencies etc.
            thermo_data (rmgpy.thermo.ThermoData): Actual thermochemistry values calculated using statistical mechanics
                at select points. Arkane fits a heat capacity model to this data
            t1_diagnostic (float): T1 diagnostic for coupled cluster calculations to check if single reference methods
                are suitable
            fod (float): Fractional Occupation number weighted electron Density
        """
        super(CalculatedDataEntry, self).__init__()
        self.conformer = conformer
        self.thermo_data = thermo_data
        self.t1_diagnostic = t1_diagnostic
        self.fod = fod

    def __repr__(self):
        return str(self.as_dict())

    @property
    def conformer(self):
        return self._conformer

    @conformer.setter
    def conformer(self, value):
        if value:
            if isinstance(value, Conformer):
                self._conformer = value
            else:
                raise ValueError('conformer for a CalculatedDataEntry object must be an rmgpy Conformer instance')
        else:
            self._conformer = None

    @property
    def thermo_data(self):
        return self._thermo_data

    @thermo_data.setter
    def thermo_data(self, value):
        if value:
            if isinstance(value, ThermoData):
                self._thermo_data = value
            else:
                raise ValueError('thermo_data for a CalculatedDataEntry object must be an rmgpy ThermoData object')


class ReferenceDatabase(object):
    """
    A class for loading and working with database of reference species, located at RMG-database/input/reference_sets/
    """
    def __init__(self):
        """
        Attributes:
            self.reference_sets (Dict[str, ReferenceSpecies]): {'set name': [ReferenceSpecies, ...], ...}
        """
        self.reference_sets = {}

    def load(self, paths=''):
        """
        Load one or more set of reference species and append it on to the database

        Args:
            paths (Union[list, str]): A single path string, or a list of path strings pointing to a set of reference
                species to be loaded into the database. The string should point to the folder that has the name of the
                reference set. The name of sub-folders in a reference set directory should be indices starting from 0
                and should contain a YAML file that defines the ReferenceSpecies object of that index, named {index}.yml
        """
        if not paths:  # Default to the main reference set in RMG-database
            paths = [os.path.join(settings['database.directory'], 'reference_sets/main')]

        if isinstance(paths, str):  # Convert to a list with one element
            paths = [paths]

        molecule_list = []
        for path in paths:
            set_name = os.path.basename(path)
            logging.info('Loading in reference set `{0}` from {1} ...'.format(set_name, path))
            spcs_files = os.listdir(path)
            reference_set = []
            for spcs in spcs_files:
                ref_spcs = ReferenceSpecies.__new__(ReferenceSpecies)
                ref_spcs.load_yaml(os.path.join(path, spcs))
                molecule = Molecule().fromAdjacencyList(ref_spcs.adjacency_list)
                if (len(ref_spcs.calculated_data) == 0) or (len(ref_spcs.reference_data) == 0):
                    logging.warning('Molecule {0} from reference set `{1}` does not have any reference data and/or '
                                    'calculated data. This entry will not be added'.format(ref_spcs.smiles, set_name))
                    continue
                # perform isomorphism checks to prevent duplicate species
                for mol in molecule_list:
                    if molecule.isIsomorphic(mol):
                        logging.warning('Molecule {0} from reference set `{1}` already exists in the reference '
                                        'database. The entry from this reference set will not be added. The path for '
                                        'this species is {2}'.format(ref_spcs.smiles, set_name, spcs))
                        break
                else:
                    molecule_list.append(molecule)
                    reference_set.append(ref_spcs)

            self.reference_sets[set_name] = reference_set

    def extract_model_chemistry(self, model_chemistry, sets=None, as_error_canceling_species=True):
        """
        Return a list of ErrorCancelingSpecies or ReferenceSpecies objects from the reference species in the database
        that have entries for the requested model chemistry

        Args:
            model_chemistry (str): String that describes the level of chemistry used to calculate the low level data
            sets (list): A list of the names of the reference sets to include (all sets in the database will be used if
                not specified or `None`)
            as_error_canceling_species (bool): Return ErrorCancelingSpecies objects if True

        Returns:
            List[ErrorCancelingSpecies]
        """
        reference_list = []

        if sets is None:  # Load in all of the sets
            sets = self.reference_sets.keys()

        for set_name in sets:
            current_set = self.reference_sets[set_name]
            for ref_spcs in current_set:
                if model_chemistry not in ref_spcs.calculated_data:  # Move on to the next reference species
                    continue
                if not ref_spcs.reference_data:  # This reference species does not have any sources, continue on
                    continue
                reference_list.append(ref_spcs)

        if as_error_canceling_species:
            reference_list = [s.to_error_canceling_spcs(model_chemistry) for s in reference_list]

        return reference_list

    def list_available_chemistry(self, sets=None):
        """
        List the set of available model chemistries present in at least one reference species in the database

        Args:
            sets (list): A list of the names of the reference sets to include (all sets in the database will be used if
                not specified or `None`)

        Returns:
            List[str]
        """
        model_chemistry_set = set()
        if sets is None:  # Load in all of the sets
            sets = self.reference_sets.keys()

        for set_name in sets:
            current_set = self.reference_sets[set_name]
            for ref_spcs in current_set:
                model_chemistry_set.update(ref_spcs.calculated_data.keys())

        return list(model_chemistry_set)

    def get_species_from_index(self, indices, set_name='main'):
        """
        Returns a list of reference species from the requested reference set that matches the indices in order

        Args:
            indices (List(int)): A list of reference species indices to return (in order)
            set_name (str): The name of the reference set to search in (only one set)

        Returns:
            List
        """
        if not isinstance(indices, list):
            indices = [indices]

        reference_species_list = []
        search_set = self.reference_sets[set_name]
        for index in indices:
            if not isinstance(index, int):
                index = int(index)
            for ref_spcs in search_set:
                if ref_spcs.index == index:
                    reference_species_list.append(ref_spcs)
                    break
            else:
                raise ValueError('No reference species with index {0} was found in reference set {1}'.format(index,
                                                                                                             set_name))

        return reference_species_list

    def get_species_from_label(self, labels, set_name='main'):
        """
        Returns a list of reference species from the requested reference set that matches the labels in order

        Args:
            labels (List(str)): A list of labels that match the returned reference species (in order)
            set_name (str): The name of the reference set to search in (only one set)

        Returns:
            List
        """
        if not isinstance(labels, list):
            labels = [labels]

        reference_species_list = []
        search_set = self.reference_sets[set_name]
        for label in labels:
            if not isinstance(label, str):
                label = str(label)
            for ref_spcs in search_set:
                if ref_spcs.label == label:
                    reference_species_list.append(ref_spcs)
                    break
            else:
                raise ValueError('No reference species with label "{0}" was found in reference set '
                                 '{1}'.format(label, set_name))

        return reference_species_list


if __name__ == '__main__':
    pass