from tables import Rentals, Stations
from create_database import create_db
import sys, os
from pandas import read_csv
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session
from datetime import datetime
from sqlalchemy.exc import NoResultFound

def load_csv(file):
    if not os.path.exists(file):
        raise Exception("CSV file does not exist")

    data = read_csv(file)
    # data = data.drop_duplicates(subset="UID wynajmu")
    return data


def get_db_station(station_name, session, stations):
    if station_name in stations.keys():
        return stations[station_name]

    query = select(Stations).where(Stations.station_name == station_name)
    station = session.scalar(query)

    if not station:
        station = Stations(station_name=station_name)

    return station

def data_to_database(data, db):
    stations = {}
    rentals = []

    date_format = "%Y-%m-%d %H:%M:%S"

    with Session(db) as session:
        for _, row in data.iterrows():
            rental_id = int(row["UID wynajmu"])
            bike_number = int(row["Numer roweru"])
            start_time = datetime.strptime(row["Data wynajmu"], date_format)
            end_time = datetime.strptime(row["Data zwrotu"], date_format)

            rental_station = get_db_station(row["Stacja wynajmu"], session, stations)
            return_station = get_db_station(row["Stacja zwrotu"], session, stations)

            stations[row["Stacja wynajmu"]] = rental_station
            stations[row["Stacja zwrotu"]] = return_station

            rentals.append(
                Rentals(
                    id=rental_id,
                    bike_number=bike_number,
                    start_time=start_time,
                    end_time=end_time,
                    rental_station=rental_station,
                    return_station=return_station
                )
            )

        session.add_all(stations.values())
        session.add_all(rentals)
        session.commit()


if __name__ == "__main__":
    if len(sys.argv) != 3:
        raise Exception("Wrong number of args")

    file = sys.argv[1]
    database = sys.argv[2]

    if not os.path.exists(database + ".sqlite3"):
        create_db(database)

    engine = create_engine(f"sqlite:///{database}.sqlite3")

    data_to_database(load_csv(file), engine)
