# TODO: Add file comment
import unittest
import nba_bot

class TestCalc(unittest.TestCase):

    # TODO: Add more tests
    def test_return_stats(self):
        result = nba_bot.return_stats('@sportstatsgenie NBA Zach LaVine 2020-21 PTS')
        self.assertEqual(result, 'Zach LaVine averaged 27.4 PTS in the 2020-21 season')

        result2 = nba_bot.return_stats('@sportstatsgenie NBA Michael Jordan 1997-98 PTS')
        self.assertEqual(result2, 'Michael Jordan averaged 28.7 PTS in the 1997-98 season')


if __name__ == '__main__':
    unittest.main()