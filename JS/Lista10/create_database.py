from tables import Base
from sqlalchemy import create_engine
import sys, os

def create_db(db_name):
    engine = create_engine(f"sqlite:///{db_name}.sqlite3")
    Base.metadata.create_all(engine)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise Exception("Wrong number of args")
    database_name = sys.argv[1]
    if os.path.exists(f"{database_name}.sqlite3"):
        print("Database already exists")
    else:
        create_db(database_name)
