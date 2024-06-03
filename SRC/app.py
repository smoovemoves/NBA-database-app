from flask import Flask, render_template
import psycopg2

app = Flask(__name__)

def get_db_connection():
    conn = psycopg2.connect(
        dbname='nba_db',
        user='your_user',
        password='your_password',
        host='localhost'
    )
    return conn

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
