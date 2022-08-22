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

class InvalidArgumentCountException(NBABotException):
    '''
    When the user's request does not have the correct number of arguments to make a valid query
    '''

class InvalidQueryException(NBABotException):
    '''
    When we encounter an error attempting to query the user's data via pandas
    '''

class PlayerNotFoundException(NBABotException):
    '''
    When the user request data for a player not found in the database
    '''

class InvalidSeasonException(NBABotException):
    '''
    When the user requests stats from a season that is unsupported
    '''