from pydantic import BaseModel
import sqlite3
from fastapi import FastAPI

app = FastAPI()

def connect_to_database():
    return sqlite3.connect('FootballPlayer.db')

def create_table():
    connection = connect_to_database()
    cursor = connection.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Football_players(
        id INTEGER PRIMARY KEY,
        first_name TEXT NULL,
        last_name TEXT NULL,
        age INTEGER NULL,
        football_club TEXT NULL )
    ''')

    connection.commit()
    connection.close()


def insert_football_player(first_name, last_name, age, football_club):
    connection = connect_to_database()
    cursor = connection.cursor()

    cursor.execute('INSERT INTO Football_players (first_name, last_name, age, football_club) VALUES(?,?,?,?)',
                   (first_name, last_name, age, football_club))
    connection.commit()
    connection.close()


def select_all_players():
    connection = connect_to_database()
    cursor = connection.cursor()

    cursor.execute('SELECT * FROM Football_players')
    users = cursor.fetchall()
    for user in users:
        print(user)

    connection.close()


def select_player_by_first_name_or_last_name(name):
    connection = connect_to_database()
    cursor = connection.cursor()

    cursor.execute('SELECT * FROM Football_players WHERE first_name LIKE ? OR last_name LIKE ?', (name, name))
    users = cursor.fetchall()
    for user in users:
        print(user)

    connection.close()


def delete_player_by_first_name_or_last_name(name):
    connection = connect_to_database()
    cursor = connection.cursor()

    cursor.execute('DELETE FROM Football_players WHERE first_name = ? OR last_name = ?', (name, name))

    connection.commit()
    connection.close()


def update_football_club_by_name(name, new_club):
    connection = connect_to_database()
    cursor = connection.cursor()

    cursor.execute('UPDATE Football_players SET football_club = ? WHERE first_name = ? OR last_name = ?', (new_club, name, name))

    connection.commit()
    connection.close()


def main():
    create_table()

    while True:
        print("\nВыберите действие:\n"
              "1. Добавить нового футболиста\n"
              "2. Посмотреть всех футболистов\n"
              "3. Поиск футболиста по имени или фамилии\n"
              "4. Обновить футбольный клуб игрока\n"
              "5. Удалить футболиста\n"
              "0. Выйти")

        choice = input()

        if choice == "1":
            first_name = input("Введите имя: ")
            last_name = input("Введите фамилию: ")
            age = input("Введите возраст: ")
            football_club = input("Введите футбольный клуб: ")
            insert_football_player(first_name, last_name, age, football_club)

        elif choice == "2":
            select_all_players()

        elif choice == "3":
            name = input("Введите имя или фамилию футболиста: ")
            select_player_by_first_name_or_last_name(name)

        elif choice == "4":
            name = input("Введите имя или фамилию футболиста: ")
            new_football_club = input("Введите новый футбольный клуб: ")
            update_football_club_by_name(name, new_football_club)

        elif choice == "5":
            name = input("Введите имя или фамилию футболиста: ")
            delete_player_by_first_name_or_last_name(name)

        else:
            break;


class FootballPlayerCreate(BaseModel):
    first_name: str
    last_name: str
    age: int
    football_club: str=None

@app.post('/football_players/', response_model=FootballPlayerCreate)
async def create_football_player(player: FootballPlayerCreate):
    insert_player(player.first_name, player.last_name, player.age, player.football_club)
    return player

@app.get('/football_players/')
async def read_football_players():
    connection = connect_to_database()
    cursor = connection.cursor()

    cursor.execute('SELECT * FROM Football_players')
    players = cursor.fetchall()

    return {'players': players}

@app.get('/football_players/{name}')
async def read_football_player(name):
    connection = connect_to_database()
    cursor = connection.cursor()

    cursor.execute(f'SELECT * FROM Football_players WHERE first_name = "{name}"')
    results = cursor.fetchall()
    connection.close()

    if not results:
        raise HTTPException(status_code=404, detail="Player not found")

    return {'player': results[0]}

if __name__ == '__main__':
    main()
