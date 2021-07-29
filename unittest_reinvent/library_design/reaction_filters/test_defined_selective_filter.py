import unittest

from rdkit import Chem

from reinvent_chemistry.library_design import BondMaker, AttachmentPoints
from reinvent_chemistry.library_design.reaction_filters import ReactionFiltersEnum
from reinvent_chemistry.library_design.reaction_filters.reaction_filter import ReactionFilter
from reinvent_chemistry.library_design.reaction_filters.reaction_filter_configruation import ReactionFilterConfiguration
from unittest_reinvent.fixtures.paths import REACTION_DEFINITIONS_PATH
from unittest_reinvent.fixtures.test_data import DECORATION_SUZUKI, \
    SCAFFOLD_SUZUKI, SCAFFOLD_NO_SUZUKI, DECORATION_NO_SUZUKI, SCAFFOLD_TO_DECORATE, TWO_DECORATIONS_SUZUKI, \
    TWO_DECORATIONS_ONE_SUZUKI, REACTION_SUZUKI_NAME


class TestDefinedSelectiveFilterSingleReaction(unittest.TestCase):
    def setUp(self):
        self._bond_maker = BondMaker()
        self._attachment_points = AttachmentPoints()
        self._enum = ReactionFiltersEnum()
        reactions = {"0": [REACTION_SUZUKI_NAME]}
        configuration = ReactionFilterConfiguration(type=self._enum.DEFINED_SELECTIVE,
                                                    reactions=reactions,
                                                    reaction_definition_file=REACTION_DEFINITIONS_PATH)
        self.reaction_filter = ReactionFilter(configuration)

    def test_with_suzuki_reagents(self):
        scaffold = SCAFFOLD_SUZUKI
        decoration = DECORATION_SUZUKI
        scaffold = self._attachment_points.add_attachment_point_numbers(scaffold, canonicalize=False)
        molecule: Chem.Mol = self._bond_maker.join_scaffolds_and_decorations(scaffold, decoration)
        score = self.reaction_filter.evaluate(molecule)
        self.assertEqual(1.0, score)

    def test_with_non_suzuki_reagents(self):
        scaffold = SCAFFOLD_NO_SUZUKI
        decoration = DECORATION_NO_SUZUKI
        scaffold = self._attachment_points.add_attachment_point_numbers(scaffold, canonicalize=False)
        molecule: Chem.Mol = self._bond_maker.join_scaffolds_and_decorations(scaffold, decoration)
        score = self.reaction_filter.evaluate(molecule)
        self.assertEqual(0.5, score)


class TestDefinedSelectiveFilter(unittest.TestCase):
    def setUp(self):
        self._bond_maker = BondMaker()
        self._attachment_points = AttachmentPoints()
        self._enum = ReactionFiltersEnum()
        reactions = {"0": [REACTION_SUZUKI_NAME], "1": [REACTION_SUZUKI_NAME]}
        configuration = ReactionFilterConfiguration(type=self._enum.DEFINED_SELECTIVE, reactions=reactions,
                                                    reaction_definition_file=REACTION_DEFINITIONS_PATH)
        self.reaction_filter = ReactionFilter(configuration)

    def test_two_attachment_points_with_suzuki_reagents(self):
        scaffold = SCAFFOLD_TO_DECORATE
        decoration = TWO_DECORATIONS_SUZUKI
        scaffold = self._attachment_points.add_attachment_point_numbers(scaffold, canonicalize=False)
        molecule: Chem.Mol = self._bond_maker.join_scaffolds_and_decorations(scaffold, decoration)
        score = self.reaction_filter.evaluate(molecule)
        self.assertEqual(1.0, score)

    def test_two_attachment_points_one_with_suzuki_reagents(self):
        scaffold = SCAFFOLD_TO_DECORATE
        decoration = TWO_DECORATIONS_ONE_SUZUKI
        scaffold = self._attachment_points.add_attachment_point_numbers(scaffold, canonicalize=False)
        molecule: Chem.Mol = self._bond_maker.join_scaffolds_and_decorations(scaffold, decoration)
        score = self.reaction_filter.evaluate(molecule)
        self.assertEqual(0.75, score)
