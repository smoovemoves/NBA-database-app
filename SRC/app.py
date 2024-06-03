from flask import Flask, render_template
import psycopg2
import csv

app = Flask(__name__)

def get_db_connection():
    conn = psycopg2.connect(
        dbname='nba_db',
        user='postgres',
        password='X9xf6y8gx77m2d',
        host='localhost'
    )
    return conn

def create_tables():
    commands = [
        """
        CREATE TABLE IF NOT EXISTS Teams (
            TeamID SERIAL PRIMARY KEY,
            TeamName VARCHAR(50) NOT NULL
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS Players (
            PlayerID SERIAL PRIMARY KEY,
            Name VARCHAR(100) NOT NULL,
            TeamID INTEGER,
            Position VARCHAR(10),
            FOREIGN KEY (TeamID) REFERENCES Teams(TeamID)
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS Stats (
            StatID SERIAL PRIMARY KEY,
            PlayerID INTEGER NOT NULL,
            Points INTEGER NOT NULL,
            Assists INTEGER NOT NULL,
            Rebounds INTEGER NOT NULL,
            FOREIGN KEY (PlayerID) REFERENCES Players(PlayerID)
        )
        """
    ]
    conn = get_db_connection()
    cur = conn.cursor()
    for command in commands:
        cur.execute(command)
    conn.commit()
    cur.close()
    conn.close()

def import_data():
    conn = get_db_connection()
    cur = conn.cursor()
    
    # Import teams
    with open('data/team.csv', 'r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip the header row
        for row in reader:
            cur.execute("INSERT INTO Teams (TeamName) VALUES (%s)", (row[0],))
    
    # Import players
    with open('data/player.csv', 'r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip the header row
        for row in reader:
            cur.execute("INSERT INTO Players (Name, TeamID, Position) VALUES (%s, %s, %s)", (row[0], row[1], row[2]))

    # Import stats
    with open('data/common_player_info.csv', 'r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip the header row
        for row in reader:
            cur.execute("INSERT INTO Stats (PlayerID, Points, Assists, Rebounds) VALUES (%s, %s, %s, %s)", (row[0], row[1], row[2], row[3]))

    conn.commit()
    cur.close()
    conn.close()

@app.route('/import')
def import_csv_data():
    create_tables()
    import_data()
    return "Data imported successfully!"

@app.route('/')
def index():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM Players;')
    players = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('index.html', players=players)

@app.route('/player/<int:player_id>')
def player(player_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM Players WHERE PlayerID = %s;', (player_id,))
    player = cur.fetchone()
    cur.execute('SELECT * FROM Stats WHERE PlayerID = %s;', (player_id,))
    stats = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('player.html', player=player, stats=stats)

if __name__ == '__main__':
    app.run(debug=True)
