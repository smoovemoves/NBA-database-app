import csv
import psycopg2
from flask import Flask, render_template
from flask import request
import re


app = Flask(__name__)

def get_db_connection():
    conn = psycopg2.connect(
        dbname='Your database name',
        user='your username',
        password='your password',
        host='localhost'
    )
    return conn

def import_data():
    conn = get_db_connection()
    cur = conn.cursor()
    
    try:
        with open('path to data file/common_player_info.csv', 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                cur.execute(
                    "INSERT INTO Teams (TeamName, team_abbreviation, team_code, team_city) VALUES (%s, %s, %s, %s)",
                    (row['team_name'], row['team_abbreviation'], row['team_code'], row['team_city'])
                )
                cur.execute("SELECT * FROM Players WHERE PlayerID = %s", (row['person_id'],))
                if cur.fetchone() is None:
                    cur.execute(
                        "INSERT INTO Players (PlayerID, FullName, Team_name, height, Weight_p) VALUES (%s, %s, %s, %s, %s)", 
                        (row['person_id'], row['display_first_last'], row['team_name'], row['height'], row['weight'])
                    )
                    cur.execute(
                        "INSERT INTO Stats (PlayerID, rosterstatus, position, bench_press) VALUES (%s, %s, %s, %s)",
                        (row['person_id'], row['rosterstatus'], row['position'], 'No data')
                    )
        conn.commit()

        with open('your path to data file/draft_combine_stats.csv', 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                bench_press = str(row['bench_press'])
                cur.execute(
                    "UPDATE Stats SET bench_press = %s WHERE PlayerID = %s",
                    (bench_press, row['player_id'])
            )
        conn.commit()
    except Exception as e:
        print("Error occurred:", e)
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
    print(player_id)
    cur.execute('SELECT * FROM Players WHERE PlayerID = %s;', (player_id,))
    player = cur.fetchone()
    cur.execute('SELECT * FROM Stats WHERE PlayerID = %s;', (player_id,))
    stats = cur.fetchone()
    cur.close()
    conn.close()
    return render_template('player.html', player=player, stats=stats)

@app.route('/Search', methods=['GET', 'POST'])
def search():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM Players WHERE FullName ILIKE %s;', ('%'+request.form['search']+'%',))
    players = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('index.html', players=players)

@app.route('/FilterHeight', methods=['POST'])
def filter_height():
    conn = get_db_connection()
    cur = conn.cursor()

    def is_valid_height_format(height):
        pattern = r'^\d+-\d+$'
        return bool(re.match(pattern, height))

    min_height = request.form['min_height']
    max_height = request.form['max_height']
    error_message = ""

    if not is_valid_height_format(min_height) or not is_valid_height_format(max_height):
        error_message = "Invalid height format. Please enter height as 'feet-inches' as whole numbers."
        return render_template('index.html', error_message=error_message)

    min_height_in_inches = int(min_height.split("-")[0]) * 12 + int(min_height.split("-")[1])
    max_height_in_inches = int(max_height.split("-")[0]) * 12 + int(max_height.split("-")[1])

    cur.execute("SELECT * FROM Players WHERE height LIKE '%%-%%' AND (CAST(SUBSTRING(height FROM 1 FOR POSITION('-' IN height) - 1) AS INTEGER) * 12 + CAST(SUBSTRING(height FROM POSITION('-' IN height) + 1) AS INTEGER)) BETWEEN %s AND %s;", (min_height_in_inches, max_height_in_inches))

    players = cur.fetchall()
    cur.close()
    conn.close()

    return render_template('index.html', players=players, error_message=error_message)

@app.route('/team/<team_name>', methods=['GET', 'POST'])
def team_stats(team_name):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM Teams WHERE TeamName = %s", (team_name,))
    team = cur.fetchone()
    cur.execute("SELECT * FROM Players WHERE players.team_name = %s", (team_name,))
    players = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('team_stats.html', team=team, players=players)

@app.route('/teams')
def teams():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT DISTINCT teams.teamname FROM Teams") 
    teams = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('teams.html', teams=teams)
                           
if __name__ == '__main__':
    import_data()
    app.run(debug=True)
