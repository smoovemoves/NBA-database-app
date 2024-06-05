DROP TABLE IF EXISTS Players;    

CREATE TABLE Players (
    PlayerID INT,
    FullName VARCHAR(100) NOT NULL,
    Team_name VARCHAR(50),
    height VARCHAR(50),
    Weight_p VARCHAR(10), 
    PRIMARY KEY (PlayerID)
)
        
