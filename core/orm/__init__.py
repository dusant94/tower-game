from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from core.config import config

# refactor: https://www.oreilly.com/library/view/essential-sqlalchemy-2nd/9781491916544/ch04.html
print(config)
db_conf = config.db.postgres
connection_url = (f'postgresql://{db_conf.username}'
                  f':{db_conf.password}@{db_conf.host}'
                  f'/{db_conf.db}')

db = create_engine(connection_url)

Base = declarative_base()


SessionLocal = sessionmaker(db)

def create_session():
    return SessionLocal()
