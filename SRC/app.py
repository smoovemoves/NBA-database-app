import csv
import psycopg2
from flask import Flask, render_template

app = Flask(__name__)

def get_db_connection():
    conn = psycopg2.connect(
        dbname='nba_db',
        user='postgres',
        password='X9xf6y8gx77m2d',
        host='localhost'
    )
    return conn

def import_data():
    conn = get_db_connection()
    cur = conn.cursor()
    
    try:
        with open('/Users/ulrikkjaer/Desktop/NBA-database-app/data/player.csv', 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                print(f"Reading row: {row}")
                print(f"Inserting player: {row['full_name']}, FirstName: {row['first_name']}, LastName: {row['last_name']}, IsActive: {row['is_active']}")
                cur.execute(
                    "INSERT INTO Players (FullName, FirstName, LastName, IsActive) VALUES (%s, %s, %s, %s)", 
                    (row['full_name'], row['first_name'], row['last_name'], row['is_active'])
                )
        conn.commit()
    except Exception as e:
        conn.rollback()
    finally:
        cur.close()
        conn.close()

@app.route('/import')
def import_csv_data():
    import_data() 
    return "Data imported successfully!"

@app.route('/')
def index():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM Players;')
    players = cur.fetchall()
    print(f"Fetched players: {players}")
    cur.close()
    conn.close()
    return render_template('index.html', players=players)

@app.route('/player/<int:player_id>')
def player(player_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM Players WHERE PlayerID = %s;', (player_id,))
    player = cur.fetchone()
    cur.close()
    conn.close()
    return render_template('player.html', player=player)

if __name__ == '__main__':

    import_data()
    app.run(debug=True)
