import psycopg2
import json


class Database():
    def __init__(self):
        self._connection = psycopg2.connect(
            host="localhost",
            database="postgres",
            user="postgres",
            password="postgres")
        self._cursor = self._connection.cursor()

    @property
    def connection(self):
        return self._connection

    @property
    def cursor(self):
        return self._cursor

    def execute(self, query):
        self.cursor.execute(query)

    def query(self, query):
        self.cursor.execute(query)
        return self.fetchall()

    def commit(self):
        self.connection.commit()

    # utility methods for usage with context manager
    def __enter__(self):
        return self
    
    def __exit__(self):
        self.connection.close()


def configure_db():
    with Database as db:
        schema_query = "CREATE SCHEMA IF NOT EXISTS frinx;"
        table_query = """CREATE TABLE IF NOT EXISTS frinx.interfaces (
            id SERIAL PRIMARY KEY,
            connection INTEGER,
            name VARCHAR(255) NOT NULL,
            description VARCHAR(255),
            config json,
            type VARCHAR(50),
            infra_type VARCHAR(50),
            port_channel_id INTEGER,
            max_frame_size INTEGER
            );"""

        db.execute(schema_query)
        db.execute(table_query)
        db.commit()


def _read_data():
    with open('configClear_v2.json', 'r') as file:
        return json.load(file)


def parse_data():
    data = _read_data()
    pass


if __name__ == '__main__':
    configure_db()
    parse_data()
