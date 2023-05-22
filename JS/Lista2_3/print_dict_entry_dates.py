import datetime

def print_dict_entry_dates(input):
    for key, value in input.items():
        print(f"Nazwa hosta: {key}")
        nr_of_requests = 0
        first_date = datetime.datetime(2023,12,31)
        last_date = datetime.datetime(1,1,1)
        split = 0
        for request in value:
            nr_of_requests += 1
            if request["code"] == 200:
                split += 1
            if request["date"] < first_date:
                first_date = request["date"]
            if request["date"] > last_date:
                last_date = request["date"]
        print(f"Liczba żądań: {nr_of_requests}")
        print(f"Data pierwszego i ostatniego żądania: {first_date} | {last_date}")
        print(f"Stosunek żądań z kodem 200 do reszty: {split/nr_of_requests}")

