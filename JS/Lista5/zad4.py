import random
import zad2
import statistics
import datetime
from collections import defaultdict

def rand_n_logs(ld_logs, n):
    while True:
        log = random.choice(ld_logs)
        user = zad2.get_user_from_log(log)
        if user:
            break
    user_logs = [x for x in ld_logs if zad2.get_user_from_log(x) == user]
    if len(user_logs) < n:
        n = len(user_logs)
    result = random.sample(user_logs, n)
    return result

def avg_time_ssh(ld_logs):
    usr_ip = {} # ip => user
    start_times = []
    durations = []
    while len(ld_logs) > 0:
        log = ld_logs.pop(0)
        ip = zad2.get_ipv4s_from_log(log)
        user = zad2.get_user_from_log(log)
        if not user and len(ip) > 0:
            usr_ip[ip[0]] = user
        event = zad2.get_message_type(log["info"])
        if event != zad2.Event.Success.value and event != zad2.Event.Failed.value and event != zad2.Event.Connection.value:
            continue
        date = log["date"]
        month, day, time = date.split(" ")
        hour,minute,second = time.split(":")
        dt = datetime.time(int(hour), int(minute), int(second))
        dt2 = datetime.datetime.combine(datetime.date.today(), dt)
        if event == zad2.Event.Success.value or event == zad2.Event.Failed.value:
            start_times.append((dt2, user, ip))
        if event == zad2.Event.Connection.value:
            def pred(x):
                if x[2] == ip:
                    return True
                else:
                    return False
            match_elem = [x for x in start_times if pred(x)]
            if len(match_elem) == 0:
                continue
            match_elem = match_elem[0]
            result = (dt2 - match_elem[0], match_elem[1], match_elem[2])
            # start_times.remove(match_elem)
            durations.append(result)

    whole_file_dur = [x[0].seconds for x in durations]
    mean_whole_file = statistics.mean(whole_file_dur)
    std_whole_file = statistics.stdev(whole_file_dur)
    stats_users = defaultdict(list)
    result_users = {}
    for x in durations:
        stats_users[x[1]].append(x[0].seconds)
    for key in stats_users.keys():
        entry = {}
        if len(stats_users[key]) > 2:
            entry["mean"] = statistics.mean(stats_users[key])
            entry["std"] = statistics.stdev(stats_users[key])
        result_users[key] = entry
    return mean_whole_file, std_whole_file, result_users

def min_max_users(ld_logs):
    users = defaultdict(int)
    while len(ld_logs) > 0:
        log = ld_logs.pop(0)
        event = zad2.get_message_type(log["info"])
        if event == zad2.Event.Success.value or event == zad2.Event.Failed.value:
            user = zad2.get_user_from_log(log)
            if user:
                users[user] += 1
    min_val = min(users.values())
    max_val = max(users.values())
    min_users = [k for k, v in users.items() if v == min_val]
    max_users = [k for k, v in users.items() if v == max_val]
    return min_users, max_users
