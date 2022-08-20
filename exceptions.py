'''
Some user defined exceptions for the NBA Twitter bot.
'''

class NBABotException(Exception):
    '''
    Base class for the Twitter bot's exceptions
    '''

class InvalidAtException(NBABotException):
    '''
    When the user does not begin their tweet with @sportstatsgenie
    '''

class InvalidLeagueException(NBABotException):
    '''
    When the bot is not able to parse a valid league from the user's input
    '''