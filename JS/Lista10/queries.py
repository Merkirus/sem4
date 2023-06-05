from sqlalchemy import select, select
from sqlalchemy.orm import Session
from tables import Rentals, Stations

def find_rentals_by_return_station(station_name, db):
    with Session(db) as session:
        query = select(Rentals).join(Stations, Rentals.return_station_id == Stations.station_id).where(Stations.station_name == station_name)
        rentals = session.scalars(query).all()
        return rentals


def find_rentals_by_rental_station(station_name, db):
    with Session(db) as session:
        query = select(Rentals).join(Stations, Rentals.rental_station_id == Stations.station_id).where(Stations.station_name == station_name)
        rentals = session.scalars(query).all()
        return rentals

def find_station_name(rental_id, db):
    with Session(db) as session:
        query = select(Stations).join(Rentals, Stations.station_id == Rentals.rental_station_id).where(Rentals.id == rental_id)
        stations = session.scalars(query).one()
        return stations

def find_rentals_by_equal_station(db):
    with Session(db) as session:
        query = select(Rentals).filter(Rentals.rental_station_id == Rentals.return_station_id)
        rentals = session.scalars(query).all()
        return rentals
