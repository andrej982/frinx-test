from plistlib import FMT_BINARY
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

    def execute(self, query, params=None):
        self.cursor.execute(query, params)

    def query(self, query, params=None):
        self.cursor.execute(query, params)
        return self.fetchall()

    def commit(self):
        self.connection.commit()

    # utility methods for usage with context manager
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.connection.close()


def configure_db():
    with Database() as db:
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
        return json.load(file)['frinx-uniconfig-topology:configuration']['Cisco-IOS-XE-native:native']['interface']


def parse_data():
    with Database() as db:
        data = _read_data()
        for interface_type in ['Port-channel', 'TenGigabitEthernet', 'GigabitEthernet']:
            for interface in data[interface_type]:
                insert_query = """INSERT INTO frinx.interfaces (name, description, max_frame_size, config, port_channel_id)
                    VALUES ( %s, %s, %s, %s, %s);"""
                params = (
                    interface_type + str(interface['name']),
                    interface.get('description', None),
                    interface.get('mtu', None),
                    json.dumps(interface),
                    interface.get('Cisco-IOS-XE-ethernet:channel-group', {}).get('number', None)
                )
                db.execute(insert_query, params)
                db.commit()


if __name__ == '__main__':
    configure_db()
    parse_data()
