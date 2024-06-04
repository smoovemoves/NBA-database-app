DROP TABLE IF EXISTS Stats;

CREATE TABLE Stats (
    PlayerID INT,
    rosterstatus VARCHAR(10) NOT NULL,
    FOREIGN KEY (PlayerID) REFERENCES Players(PlayerID)
);
