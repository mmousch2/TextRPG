import sys
import unittest
from io import StringIO

import gameSetup
from characters import npc as n
from objects import room as r


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

    def room_test(self):
        self.room.set_name("my room")
        assert(self.room.name == "my room")

        self.room.set_description("a beautiful room")
        assert(self.room.description == "a beautiful room")

        self.room.add_direction("west", 42)
        assert("west" in self.room.directions)
        assert(self.room.directions["west"] == 42)

        self.room.add_item("shiny object")
        assert("shiny object" in self.room.items)

        self.room.add_character("steve")
        assert("steve" in self.room.characters)