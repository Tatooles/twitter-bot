-- @block
SHOW DATABASES;

-- @block
CREATE TABLE `2021-22`(
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(255) NOT NULL,
    team VARCHAR(3),
    games INT,
    points INT,
    rebounds INT,
    assists INT
);

-- @block
INSERT INTO `2021-22`(name, team, games, points, rebounds, assists)
VALUES(
    'Stephen Curry',
    'GSW',
    64,
    1630,
    335,
    404
);

-- @block
INSERT INTO `2021-22`(name, team, games, points, rebounds, assists)
VALUES
    ('LeBron James', 'LAL', 56, 1695, 459, 349),
    ('DeMar DeRozan', 'CHI', 76, 2118, 392, 374),
    ('Giannis Antetokounmpo', 'MIL', 67, 2002, 778, 388);


-- @block Show whole table
SELECT * FROM `2021-22`

-- @block Show points per game
SELECT name, points/games FROM `2021-22`

-- @block Show single player's stats
SELECT * FROM `2021-22`
WHERE name = 'DeMar DeRozan'

-- @block Show points per game in descennding order
SELECT name, points/games FROM `2021-22`
ORDER BY points/games DESC


-- @block
CREATE TABLE `2020-21`(
    Rk INT,
    Player VARCHAR(255),
    Pos VARCHAR(10),
    Age INT,
    Tm VARCHAR(3),
    G INT,
    GS INT,
    MP INT,
    FG INT,
    FGA INT,
    FGPct INT,
    3P INT,
    3PA INT,
    3PPct INT,
    2P INT,
    2PA INT,
    2PPct INT,
    eFGPct INT,
    FT INT,
    FTA INT,
    FTPct INT,
    ORB INT,
    DRB INT,
    TRB INT,
    AST INT,
    STL INT,
    BLK INT,
    TOV INT,
    PF INT,
    PTS INT,
    Playeradditional VARCHAR(255)
);

-- @block Import the actual file
LOAD DATA INFILE '/Users/kevin/Public/text.csv' 
INTO TABLE `2020-21` 
FIELDS TERMINATED BY ',' 
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;

-- @block
DROP TABLE `2020-21`

-- Notes: a few issues I ran into, mainnly file stuff
-- Had to put the file into a public folder
-- As for formatting, had to make sure there were no double commas
-- Had to run find and replace ,, with ,0, twice

-- @block
SELECT * FROM `2020-21`

-- @block Select the top 10 scorers from that season
SELECT Player, PTS/G FROM `2020-21`
ORDER BY PTS/G DESC
LIMIT 10;