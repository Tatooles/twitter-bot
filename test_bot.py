'''
Test suite for the NBA Twitter bot.
Tests a couple example Tweets to make sure the bot will respond properly
'''
import unittest
import warnings
import nba_bot

class TestCalc(unittest.TestCase):

    def setUp(self):
        # Supress some annoying ResourceWarnings that I don't care about
        warnings.filterwarnings(action="ignore", message="unclosed", category=ResourceWarning)
        nba_bot.setup()

    def test_return_stats(self):
        result1 = nba_bot.process_request('@sportstatsgenie NBA Zach LaVine 2020-21 PTS')
        result2 = nba_bot.process_request('@sportstatsgenie NBA Michael Jordan 1997-98 PTS')
        result3 = nba_bot.process_request('@sportstatsgenie nba kyle korver 2005-06 fg3_pct')
        result4 = nba_bot.process_request('@SPORTSTATSGENIE NBA J.R. REID 1997-98 PLUS_MINUS')
        result5 = nba_bot.process_request('@sportstatsgenie nba james harden career pts')
        result6 = nba_bot.process_request("@sportstatsgenie nba shaquille o'neal career reb")
        
        self.assertEqual(result1, 'Zach Lavine averaged 27.4 pts in the 2020-21 season')
        self.assertEqual(result2, 'Michael Jordan averaged 28.7 pts in the 1997-98 season')
        self.assertEqual(result3, 'Kyle Korver averaged 0.42 fg3_pct in the 2005-06 season')
        self.assertEqual(result4, 'J.r. Reid averaged 0.3 plus_minus in the 1997-98 season')
        self.assertEqual(result5, 'James Harden averaged 24.9 pts for his career')
        self.assertEqual(result6, "Shaquille O'neal averaged 10.0 reb for his career")

    def test_errors(self):
        result1 = nba_bot.process_request('@randomat NBA Zach LaVine 2020-21 PTS')
        result2 = nba_bot.process_request('@sportstatsgenie NFL Zach LaVine 2020-21 PTS')
        result3 = nba_bot.process_request('@sportstatsgenie NBA Zach 2020-21 PTS')
        result4 = nba_bot.process_request('@sportstatsgenie NBA Zach LaVine 2020 2022 PTS')

        self.assertEqual(result1, None)
        self.assertEqual(result2, 'ERROR - I could not process your request. Please request a valid sport. Currently supported sport: NBA')
        self.assertEqual(result3, 'ERROR - I could not process your request. Incorrect number of arguments, I need 6 arguments to make a valid query (@sportstatsgenie, league, first_name, last_name, season, stat)')
        self.assertEqual(result4, 'ERROR - I could not process your request. Incorrect number of arguments, I need 6 arguments to make a valid query (@sportstatsgenie, league, first_name, last_name, season, stat)')
        
    def test_invalid_query(self):
        result1 = nba_bot.process_request('@sportstatsgenie NBA Jim Jameson 2020-21 PTS')
        result2 = nba_bot.process_request('@sportstatsgenie NBA Zach LaVine 2020-21 blks')

        self.assertEqual(result1, 'ERROR - I could not process your request. Couldn\'t complete a valid query with the information you provided')
        self.assertEqual(result2, 'ERROR - I could not process your request. Couldn\'t complete a valid query with the information you provided')


if __name__ == '__main__':
    unittest.main()