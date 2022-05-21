import unittest

from tennis import Tennis


class TestTennis(unittest.TestCase):
    def setUp(self):
        self.tennis = Tennis()

    def test_fifteen_love(self):
        self.given_first_player_score(1)
        self.score_should_be('fifteen love')

    def test_thirty_love(self):
        self.given_first_player_score(2)
        self.score_should_be('thirty love')

    def given_first_player_score(self, times):
        for _ in range(times):
            self.tennis.first_player_score()

    def score_should_be(self, expected):
        self.assertEqual(self.tennis.score(), expected)
