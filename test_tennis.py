import unittest

from tennis import Tennis


class TestTennis(unittest.TestCase):
    def test_fifteen_love(self):
        tennis = Tennis()
        tennis.first_player_score()
        self.assertEqual(tennis.score(), 'fifteen love')


