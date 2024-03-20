import psycopg2 as psql
from config.config import Config

class Database:
    def __init__(self, config: Config) -> None:
        self._db_con = psql.connect(
            host = config.postgres_host,
            port = config.postgres_port,
            database = config.postgres_db,
            user = config.postgres_user,
            password = config.postgres_password
        )

    def create_user(self, username: str, password: str) -> None:
        cursor = self._db_con.cursor()
        sqlRequest = "INSERT INTO users (username, password) VALUES (%s, %s)"
        cursor.execute(sqlRequest, (username, password))
        self._db_con.commit()

    def get_user(self, username: str):
        cursor = self._db_con.cursor()
        sqlRequest = "SELECT * FROM users WHERE username=%s" 
        cursor.execute(sqlRequest, (username, ))
        self._db_con.rollback()

        return cursor.fetchone()
    
    def create_note(self, user_id: int, title: str, message: str, time) -> None:
        cursor = self._db_con.cursor()
        sqlRequest = "INSERT INTO notes (user_id, title, message, created_at) VALUES (%s, %s, %s, %s)"
        cursor.execute(sqlRequest, (user_id, title, message, time))
        
        self._db_con.commit()

    def get_user_notes(self, user_id: int):
        cursor = self._db_con.cursor()
        sqlRequest = "SELECT title, message, created_at FROM notes WHERE user_id=%s"
        cursor.execute(sqlRequest, (user_id))
        self._db_con.rollback()

        return cursor.fetchall()

    def search_user_notes(self, user_id: int, search: str):
        cursor = self._db_con.cursor()
        self._db_con.rollback()
        sqlRequest = "SELECT title, message, created_at FROM notes WHERE user_id=%s and title=%s"
        cursor.execute(sqlRequest, (user_id, search))

        return cursor.fetchall()