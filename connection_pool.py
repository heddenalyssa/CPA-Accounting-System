import os
from psycopg2.pool import SimpleConnectionPool
from dotenv import load_dotenv
from contextlib import contextmanager

pool = None

def init_pool(database_url: str = None):
    #Initializing the connection pool depending on if the database was provided or not.

    global pool
    load_dotenv()
    if database_url:
        pool = SimpleConnectionPool(1, 5, dsn=database_url)
    else:
        db_uri = {'user':os.environ['USER'],
            'password':os.environ['PASSWORD'],
            'host':os.environ['HOST'],
            'port':os.environ['PORT'],
            'dbname':os.environ['DBNAME']}


        pool = SimpleConnectionPool(minconn=1, maxconn=5,
                                    host=db_uri['host'],
                                    database=db_uri['dbname'],
                                    user=db_uri['user'],
                                    password=db_uri['password'],
                                    port=db_uri['port'])


@contextmanager
def get_connection():
    connection = pool.getconn()

    try:
        yield connection
    finally:
        pool.putconn(connection)