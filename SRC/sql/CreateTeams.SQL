DROP TABLE IF EXISTS Teams;

CREATE TABLE Teams (
    TeamID SERIAL PRIMARY KEY,
    TeamName VARCHAR(50) NOT NULL, 
    team_abbreviation VARCHAR(20) NOT NULL, 
    team_code VARCHAR(20) NOT NULL,
    team_city VARCHAR(50) NOT NULL)
