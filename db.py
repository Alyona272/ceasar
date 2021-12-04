from config import settings
import psycopg2

connection = psycopg2.connect(
    dbname = 'caesar',
    user = 'postgres',
    password = '11',
    host = 'localhost',
    port = 5432
)

