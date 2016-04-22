import os
import unittest
from io import StringIO
import sys

from objects import room as r
from characters import character as c, npc as n, player as p
import gameSetup


class TestControllerCommands(unittest.TestCase):

    def setUp(self):
        self.room = r.Room()
        self.convotree = gameSetup.make_conv_trees()
        self.npc = n.NPC("Vivi", self.convotree)
        self.stdout = sys.stdout
        sys.stdout = self.output = StringIO()

    def tearDown(self):
        self.room = None
        self.npc = None
        self.output.close()
        sys.stdout = self.stdout

    def test_npc_setup(self):
        self.assertTrue("Vivi" in self.convotree, "Vivi is not in convotree")
        self.assertTrue(self.npc.name == "Vivi")