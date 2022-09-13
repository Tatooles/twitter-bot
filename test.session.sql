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