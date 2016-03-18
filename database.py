import sqlite3

conn = sqlite3.connect("players_data.db")
cursor = conn.cursor()


def create_clients_table():

    create_query = '''create table if not exists
        players(username TEXT,
                score REAL)'''

    cursor.execute(create_query)


def add_player(name, score):
    player_score = [name, score]
    cursor.execute('INSERT INTO players VALUES (?, ?)', player_score)
    conn.commit()


def best_player():
    scores =  cursor.execute("SELECT * FROM players ORDER BY score DESC")
    return scores
    #for score in scores:

       #print(str(score[0]) + " : " + str(score[1]) )

create_clients_table()
