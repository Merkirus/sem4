from collections import defaultdict
import zad2
import datetime

def brute_guard(ld_logs, brute_time, user=None):
    entries = defaultdict(int)
    entry_buffer = {}
    attackers = []
    while len(ld_logs) > 0:
        log = ld_logs.pop(0)
        ip = zad2.get_ipv4s_from_log(log)
        read_user = zad2.get_user_from_log(log)
        if not user:
            if user != read_user:
                continue
        event = zad2.get_message_type(log["info"])
        if event != zad2.Event.Success.value and event != zad2.Event.Failed.value and event != zad2.Event.Connection.value:
            continue
        date = log["date"]
        month_name, day, time = date.split(" ")
        month_number = datetime.datetime.strptime(month_name, '%b').month
        dt3 = datetime.date(datetime.date.today().year, int(month_number), int(day))
        hour,minute,second = time.split(":")
        dt = datetime.time(int(hour), int(minute), int(second))
        dt2 = datetime.datetime.combine(dt3, dt)
        if event == zad2.Event.Success.value:
            entries[ip[0]] = 0
        
        if event == zad2.Event.Failed.value:
            if entries[ip[0]] == 0:
                entry_buffer[ip[0]] = dt2
                entries[ip[0]] += 1
            else:
                entries[ip[0]] += 1
                interval = dt2 - entry_buffer[ip[0]]
                if interval.seconds < brute_time:
                    attackers.append((dt2, ip[0], entries[ip[0]]))
                entry_buffer[ip[0]] = dt2

    return attackers
