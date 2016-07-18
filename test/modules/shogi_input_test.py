
import unittest
from app.modules.shogi_input import ShogiInput
class ShogiTest(unittest.TestCase):
    def setUp(self):
        pass

    def test_shogi_input_is_initable(self):
        shogi = ShogiInput.init("channel_id", ["user1", "user2"])
        self.assertEqual(shogi.channel_id, "channel_id")

        shogi = ShogiInput.init("channel_id", ["user1", "user2"])
        self.assertIsNone(shogi)

        ShogiInput.clear("channel_id")
        shogi = ShogiInput.init("channel_id", ["user1", "user2"])
        self.assertEqual(shogi.channel_id, "channel_id")


    def test_clear_for_non_exists_channnel(self):
        self.assertIsNone(ShogiInput.clear("channel_id_non_exists"))
