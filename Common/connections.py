from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from Settings.settings import *
from urllib.parse import quote_plus


def getPostgresConnections():
    # SQL Alchemy URL: dialect+driver://username:password@host:port/database
    engine = create_engine(
        "{}+{}://{}:{}@{}:{}/{}".format(DIALECT, DRIVER, DB_UNAME, quote_plus(DB_PASS), DB_HOST, DB_PORT, DB_NAME), 
        query_cache_size=QUERY_CACHE_SIZE
    )
    session = Session(engine)
    return session
