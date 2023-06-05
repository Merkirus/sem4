import sys
import zad2
import logging
import argparse
import zad4
import zad_dod

def utf8len(log):
    return len(log.encode('utf-8'))

def read_logs(input):
    logs = input.split("\n")[:-1]
    structured_logs = []
    for log in logs:
        new_log_dict = zad2.raw_log_to_dict(log)
        message = zad2.get_message_type(new_log_dict["info"])
        if message == zad2.Event.Success.value or message == zad2.Event.Connection.value:
            logging.info(message)
        if message == zad2.Event.Failed.value:
            logging.warning(message)
        if message == zad2.Event.Invalidusr.value or message == zad2.Event.Invalidpass.value:
            logging.error(message)
        if message == zad2.Event.Break.value:
            logging.critical(message)
        structured_logs.append(new_log_dict)
    return structured_logs

def mean(args):
    m_f, s_f, u = zad4.avg_time_ssh(args.logs)
    print(f"Mean file: {m_f}\nStd file: {s_f}\nUsers: {u}")

def ipv4(args):
    print(f"Log to dict: {zad2.get_ipv4s_from_log(args.ipv4l)}")

def usr(args):
    print(f"User from log: {zad2.get_user_from_log(args.usrl)}")

def raw(args):
    print(f"Log to dict entry: {zad2.raw_log_to_dict(args.rawl)}")

def r_log(args):
    print(f"Random entries: {zad4.rand_n_logs(args.logs, args.n)}")
    

def freq(args):
    min, max = zad4.min_max_users(args.logs)
    print(f"Min: {min}\nMax: {max}")

def mess(args):
    print(f"Log to message: {zad2.get_message_type(args.info)}")

def brute(args):
    print(f"Attackers with given time, ip and number of attempts: {zad_dod.brute_guard(args.logs, args.time, args.victim)}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Lab nr 5")

    parser.add_argument('-p', '--path', help="Path to file")
    parser.add_argument('-l', '--log', help="Logging level: DEBUG, INFO, WARNING, ERROR, CRITICAL")
    parser.add_argument('-v', '--verbose', action='store_true', help='Verbose')

    logs = ''

    subparsers = parser.add_subparsers()
    parser_mean = subparsers.add_parser('mean')
    parser_mean.add_argument('--logs',type=list, default=logs)
    parser_mean.set_defaults(func=mean)
    parser_ipv4 = subparsers.add_parser('ipv4')
    parser_ipv4.add_argument('--ipv4l')
    parser_ipv4.set_defaults(func=ipv4)
    parser_usr = subparsers.add_parser('usr')
    parser_usr.add_argument('--usrl')
    parser_usr.set_defaults(func=usr)
    parser_message = subparsers.add_parser('mess')
    parser_message.add_argument('--info')
    parser_message.set_defaults(func=mess)
    parser_random_logs = subparsers.add_parser('rlogs')
    parser_random_logs.add_argument('--logs', default=logs)
    parser_random_logs.add_argument('--n', type=int, default=3)
    parser_random_logs.set_defaults(func=r_log)
    parser_freq = subparsers.add_parser('freq')
    parser_freq.add_argument('--logs', default=logs)
    parser_freq.set_defaults(func=freq)
    parser_brute = subparsers.add_parser('brute')
    parser_brute.add_argument('--logs', default=logs)
    parser_brute.add_argument('--time', type=int, default=1)
    parser_brute.add_argument('--victim', type=str, default=None)
    parser_brute.set_defaults(func=brute)
#
    args = parser.parse_args()
    
    if args.log:
        lvl = args.log.lower()
        if lvl == "info":
            logging.basicConfig(encoding='utf-8', level=logging.INFO)
        elif lvl == "warning":
            logging.basicConfig(encoding='utf-8', level=logging.WARNING)
        elif lvl == "error":
            logging.basicConfig(encoding='utf-8', level=logging.ERROR)
        elif lvl == "critical":
            logging.basicConfig(encoding='utf-8', level=logging.CRITICAL)
        else:
            logging.basicConfig(encoding='utf-8', level=logging.DEBUG)
    else:
        logging.basicConfig(encoding='utf-8', level=logging.DEBUG)

    console_handler_err = logging.StreamHandler(sys.stderr)
    console_handler_cri = logging.StreamHandler(sys.stderr)
    console_handler_debug = logging.StreamHandler(sys.stdout)
    console_handler_info = logging.StreamHandler(sys.stdout)
    console_handler_warning = logging.StreamHandler(sys.stdout)

    console_handler_err.setLevel(logging.ERROR)
    console_handler_cri.setLevel(logging.CRITICAL)
    console_handler_debug.setLevel(logging.DEBUG)
    console_handler_info.setLevel(logging.INFO)
    console_handler_warning.setLevel(logging.WARNING)

    formatter = logging.Formatter('%(levelname)s: %(message)s')

    console_handler_err.setFormatter(formatter)
    console_handler_cri.setFormatter(formatter)
    console_handler_debug.setFormatter(formatter)
    console_handler_info.setFormatter(formatter)
    console_handler_warning.setFormatter(formatter)

    logger = logging.getLogger(__name__)
    logger.addHandler(console_handler_err)
    logger.addHandler(console_handler_cri)
    logger.addHandler(console_handler_info)
    logger.addHandler(console_handler_warning)
    logger.addHandler(console_handler_debug)

    with open(args.path) as f:
        while True:
            line = f.readline()
            if not line:
                break
            logs += line
            logging.debug(utf8len(line))
    
    ar = vars(args)
    str_logs = read_logs(logs)
    ar['logs'] = str_logs
    args.func(args)
