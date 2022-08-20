# TODO: Add file comment
import unittest
import warnings
import nba_bot

class TestCalc(unittest.TestCase):

    def setUp(self):
        # Supress some annoying ResourceWarnings that I don't care about
        warnings.filterwarnings(action="ignore", message="unclosed", category=ResourceWarning)
        nba_bot.setup()

    # TODO: Add more tests
    def test_return_stats(self):
        result1 = nba_bot.process_request('@sportstatsgenie NBA Zach LaVine 2020-21 PTS')
        result2 = nba_bot.process_request('@sportstatsgenie NBA Michael Jordan 1997-98 PTS')
        
        self.assertEqual(result1, 'Zach LaVine averaged 27.4 PTS in the 2020-21 season')
        self.assertEqual(result2, 'Michael Jordan averaged 28.7 PTS in the 1997-98 season')

    def test_errors(self):
        result1 = nba_bot.process_request('@randomat NBA Zach LaVine 2020-21 PTS')
        result2 = nba_bot.process_request('@sportstatsgenie NFL Zach LaVine 2020-21 PTS')

        self.assertEqual(result1, 'ERROR - Unfortunately I could not process your request. Your tweet must begin with @sportstatsgenie')
        self.assertEqual(result2, 'ERROR - I could not process your request. Please request a valid sport. Currently supported sport: NBA')

    def test_invalid_query(self):
        result1 = nba_bot.process_request('')


if __name__ == '__main__':
    unittest.main()