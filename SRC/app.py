import csv
import psycopg2
from flask import Flask, render_template
from flask import request


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
        with open('/Users/ulrikkjaer/Desktop/NBA-database-app/data/common_player_info.csv', 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                cur.execute(
                    "INSERT INTO Players (PlayerID, FullName, Team_name, height, Weight_p) VALUES (%s, %s, %s, %s)", 
                    (row['person_id'], row['display_first_last'], row['team_name'], row['height'], row['weight'])
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

@app.route('/Search', methods=['GET', 'POST'])
def search():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM Players WHERE FullName LIKE %s;', ('%'+request.form['search']+'%',))
    players = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('index.html', players=players)

@app.route('/FilterHeight', methods=['POST'])
def filter_height():
    conn = get_db_connection()
    cur = conn.cursor()

    min_height = request.form['min_height']
    max_height = request.form['max_height']

    # Convert heights to inches if they're in feet
    min_height_in_inches = int(min_height.split("-")[0]) * 12 + int(min_height.split("-")[1])
    max_height_in_inches = int(max_height.split("-")[0]) * 12 + int(max_height.split("-")[1])

    cur.execute("SELECT * FROM Players WHERE height LIKE '%%-%%' AND (CAST(SUBSTRING(height FROM 1 FOR POSITION('-' IN height) - 1) AS INTEGER) * 12 + CAST(SUBSTRING(height FROM POSITION('-' IN height) + 1) AS INTEGER)) BETWEEN %s AND %s;", (min_height_in_inches, max_height_in_inches))

    players = cur.fetchall()
    cur.close()
    conn.close()

    return render_template('index.html', players=players)

if __name__ == '__main__':
    import_data()
    app.run(debug=True)
