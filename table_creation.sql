DROP SCHEMA IF EXISTS nats;
CREATE SCHEMA nats;
USE nats;

DROP TABLE IF EXISTS player_lookup;
CREATE TABLE player_lookup (
player_id INT PRIMARY KEY,
name VARCHAR(30),
throws VARCHAR(1));

DROP TABLE IF EXISTS game_lookup;
CREATE TABLE game_lookup(
game_id INT PRIMARY KEY,
game_date DATE,
home_team_id INT,
away_team_id INT);

DROP TABLE IF EXISTS pitches;
CREATE TABLE pitches(
game_id INT,
FOREIGN KEY(game_id) REFERENCES game_lookup(game_id),
pitch_no SMALLINT,
at_bat_no SMALLINT,
pitch_of_at_bat SMALLINT,
inning SMALLINT,
top_inning SMALLINT,
pitcher_id INT,
batter_id INT,
FOREIGN KEY(pitcher_id) REFERENCES player_lookup(player_id),
FOREIGN KEY(batter_id) REFERENCES player_lookup(player_id),
velo FLOAT(4));