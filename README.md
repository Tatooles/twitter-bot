# Sports Stats Twitter Bot
Playing around with the Twitter API attempting to make a Twitter bot

But is deployed at https://twitter.com/sportstatsgenie and currently supports NBA stats from 1996 to present

## How to Use
Here's how to use me! Tweet in the format:

"@sportstatsgenie LEAGUE PLAYER_FIRSTNAME PLAYER_LASTNAME SEASON STAT1 STAT2"

Requests to the bot are NOT case sensitive so no need to worry about that!

You can include as many stats as you want after the season, as long as the bot can fit them in it's 280 character response tweet

Examples below!

Currently the only supported league is "NBA" but more are coming soon!

Supported seasons are 1996-97 through 2021-22, you can also replace the season with "career" to request the career stats of that player (since 1996).

Here are the supported stats:

nickname, team_abbreviation, age, gp, w, l, w_pct, min, fgm, fga, fg_pct, fg3m, fg3a, fg3_pct, ftm, fta, ft_pct, oreb, dreb, reb, ast, tov, stl, blk, blka, pf, pfd, pts, plus_minus, nba_fantasy_pts, dd2, td3, wnba_fantasy_pts, gp_rank, w_rank,l_rank, w_pct_rank, min_rank,fgm_rank, fga_rank, fg_pct_rank, fg3m_rank, fg3a_rank, fg3_pct_rank, ftm_rank, fta_rank, ft_pct_rank, oreb_rank, dreb_rank, reb_rank, ast_rank, tov_rank,  stl_rank, blk_rank, blka_rank, pf_rank, pfd_rank, pts_rank, plus_minus_rank, nba_fantasy_pts_rank, dd2_rank, td3_rank, wnba_fantasy_pts_rank

Here are the stats you might actually want to use:

team_abbreviation, age, gp, w_pct, min, fg_pct, fg3_pct, ft_pct reb, ast, tov, stl, blk, blka, pf, pts, plus_minus, nba_fantasy_pts


## Examples
TODO

## Future Features
Ability to compare the stats of two players

Support for MLB and NFL stats