DROP TABLE IF EXISTS Stats;

CREATE TABLE Stats (
    PlayerID INT,
    rosterstatus VARCHAR(10) NOT NULL,
    position VARCHAR(50),
    bench_press VARCHAR(50),
    FOREIGN KEY (PlayerID) REFERENCES Players(PlayerID))
