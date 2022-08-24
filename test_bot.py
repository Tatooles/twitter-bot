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
        
        self.assertEqual(result1, 'Zach Lavine averaged 27.4 pts in the 2020-21 season')
        self.assertEqual(result2, 'Michael Jordan averaged 28.7 pts in the 1997-98 season')
        self.assertEqual(result3, 'Kyle Korver averaged 0.42 fg3_pct in the 2005-06 season')
        self.assertEqual(result4, 'J.R. Reid averaged 0.3 plus_minus in the 1997-98 season')

    def test_career_stats(self):
        result1 = nba_bot.process_request('@sportstatsgenie nba james harden career pts')
        result2 = nba_bot.process_request("@sportstatsgenie nba shaquille o'neal career reb")

        self.assertEqual(result1, 'James Harden averaged 24.9 pts for his career')
        self.assertEqual(result2, "Shaquille O'Neal averaged 10.0 reb for his career")

    def test_multiple_stats(self):
        result1 = nba_bot.process_request('@sportstatsgenie nba lebron james 2021-22 pts ast reb')
        result2 = nba_bot.process_request('@sportstatsgenie nba stephen curry 2015-16 pts fg3_pct')
        result3 = nba_bot.process_request('@sportstatsgenie nba lebron james career pts ast reb')

        self.assertEqual(result1, 'Lebron James averaged 30.3 pts, 6.2 ast, and 8.2 reb in the 2021-22 season')
        self.assertEqual(result2, 'Stephen Curry averaged 30.1 pts and 0.454 fg3_pct in the 2015-16 season')
        self.assertEqual(result3, 'Lebron James averaged 27.1 pts, 7.4 ast, and 7.5 reb for his career')


    def test_errors(self):
        result1 = nba_bot.process_request('@randomat NBA Zach LaVine 2020-21 PTS')
        result2 = nba_bot.process_request('@sportstatsgenie NFL Zach LaVine 2020-21 PTS')
        result3 = nba_bot.process_request('@sportstatsgenie NBA Zach 2020-21 PTS')
        result4 = nba_bot.process_request('@sportstatsgenie NBA Zach LaVine 2020 2022 PTS')
        result5 = nba_bot.process_request('@sportstatsgenie NBA Bill Russell 2020-21 PTS')
        result6 = nba_bot.process_request('@sportstatsgenie NBA Michael Jordan 1988-89 PTS')
        result7 = nba_bot.process_request('@sportstatsgenie NBA Zach LaVine 2001-02 PTS')
        result8 = nba_bot.process_request('@sportstatsgenie NBA Zach LaVine 2001-02 points rebounds assists')

        self.assertEqual(result1, None)
        self.assertEqual(result2, 'ERROR - I could not process your request. Invalid sport, currently supported sport: NBA')
        self.assertEqual(result3, 'ERROR - I could not process your request. Not enough arguments, I need 6 at least arguments to make a valid query (@sportstatsgenie, league, first_name, last_name, season, stat)')
        self.assertEqual(result4, 'ERROR - I could not process your request. The season you provided is invalid. I can provide NBA stats from 1996-97 to 2021-22')
        self.assertEqual(result5, "ERROR - I could not process your request. The player you requested could not be found")
        self.assertEqual(result6, 'ERROR - I could not process your request. The season you provided is invalid. I can provide NBA stats from 1996-97 to 2021-22')
        self.assertEqual(result7, 'ERROR - I could not process your request. The player you requested did not play in that season')
        self.assertEqual(result8, 'ERROR - I could not process you request. You requested a stat that I do not support. See pinned tweet thread for supported stats')


if __name__ == '__main__':
    unittest.main()