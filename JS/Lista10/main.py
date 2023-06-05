from queries import *
from sqlalchemy import create_engine
import datetime
import argparse

def duration(rows):
    times = [row.end_time - row.start_time for row in rows]
    if len(times) != 0:
        return sum(times, datetime.timedelta(0)) / len(times)
    else:
        return 0

def mean_time_rental(args):
    rows = find_rentals_by_rental_station(args.dur_rental, args.engine)
    print(f"Avg. duration on starting station - {args.dur_rental}: {duration(rows)}")
    

def mean_time_return(args):
    rows = find_rentals_by_return_station(args.dur_return, args.engine)
    print(f"Avg. duration on ending station - {args.dur_return}: {duration(rows)}")

def number_of_diff_bikes(args):
    rows = find_rentals_by_return_station(args.bikes, args.engine)
    print(f"Number of different bikes on ending station - {args.bikes}: {len(set([row.bike_number for row in rows]))}")

def special_duration(rows):
    times_for_rental = {}
    for row in rows:
        times_for_rental[str(row.id)] = row.end_time - row.start_time
    return times_for_rental

def special(args):
    rows_same_station = find_rentals_by_equal_station(args.engine)
    times = special_duration(rows_same_station)
    lowest_time_id = min(times, key=times.get) # pyright: ignore
    result_row = find_station_name(int(lowest_time_id), args.engine)
    print(f"Shortest rental on same station - {result_row.station_name}: {times[lowest_time_id]}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Lab nr 10")

    parser.add_argument('-p', '--path', help="Path to file")

    subparsers = parser.add_subparsers()
    parser_mean = subparsers.add_parser('dur_rental')
    parser_mean.add_argument('--dur_rental')
    parser_mean.set_defaults(func=mean_time_rental)
    parser_ipv4 = subparsers.add_parser('dur_return')
    parser_ipv4.add_argument('--dur_return')
    parser_ipv4.set_defaults(func=mean_time_return)
    parser_usr = subparsers.add_parser('bikes')
    parser_usr.add_argument('--bikes')
    parser_usr.set_defaults(func=number_of_diff_bikes)
    parser_message = subparsers.add_parser('special')
    # parser_message.add_argument('--special')
    parser_message.set_defaults(func=special)

    args = parser.parse_args()

    if not args.path:
        raise Exception("No required args were given")
    
    engine = create_engine(f"sqlite:///{args.path}.sqlite3")

    ar = vars(args)

    if len(ar.keys()) == 1:
        raise Exception("None given task to execute")

    ar['engine'] = engine
    args.func(args)
