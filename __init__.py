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

    def close(self):
        self.connection.commit()
        self.connection.close()


def configure_db():
    db = Database()
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
    db.close()


def read_data():
    with open('configClear_v2.json', 'r') as file:
        data = json.load(file)
        pass
        return data


def parse_data():
    pass


if __name__ == '__main__':
    configure_db()
    # network_data = read_data()
    # parse_data(network_data)
