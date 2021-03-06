import psycopg2
import psycopg2.extras
import os


connection = psycopg2.connect(
    dbname=os.getenv('DB_DATABASE'),
    user=os.environ.get("DB_USER"),
    host=os.environ.get("DB_HOST"),
    password=os.environ.get("DB_PASSWORD"),
    port=os.environ.get("DB_PORT")
)
connection.autocommit = True
cursor = connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
curs = connection.cursor()

