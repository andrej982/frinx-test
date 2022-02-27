import psycopg2
import json


def connect():
    connection = psycopg2.connect(
        host="localhost",
        database="postgres",
        user="postgres",
        password="postgres")
    return connection


def read_data():
    with open('configClear_v2.json', 'r') as file:
        data = json.load(file)
        pass


if __name__ == '__main__':
    conn = connect()
    read_data()
