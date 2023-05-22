import sys
import zad2
import logging
import argparse
import zad4
import zad_dod
import click

logs = [""]

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

@click.group()
def commands():
    pass

@click.command()
@click.option('--path', required=True)
def path_to_file(path):
    logs = ""
    with open(path) as f:
        while True:
            line = f.readline()
            if not line:
                break
            logs += line
            logging.debug(utf8len(line))
    return logs

@click.command()
@click.option('--logs',default=logs[0])
def mean(logs):
    m_f, s_f, u = zad4.avg_time_ssh(logs)
    print(f"Mean file: {m_f}\nStd file: {s_f}\nUsers: {u}")

@click.command()
@click.option('--ipv4log')
def ipv4(ipv4log):
    print(f"Log to dict: {zad2.get_ipv4s_from_log(ipv4log)}")

@click.command()
@click.option('--userlog')
def usr(userlog):
    print(f"User from log: {zad2.get_user_from_log(userlog)}")

@click.command()
@click.option('--rawlog')
def raw(rawlog):
    print(f"Log to dict entry: {zad2.raw_log_to_dict(rawlog)}")

@click.command()
@click.option('--logs',default=logs[0])
@click.option('--n', default=3)
def r_log(logs, n):
    print(f"Random entries: {zad4.rand_n_logs(logs, n)}")


@click.command()
@click.option('--logs', default=logs[0])
def freq(logs):
    min, max = zad4.min_max_users(logs)
    print(f"Min: {min}\nMax: {max}")

@click.command()
@click.option('--info')
def mess(info):
    print(f"Log to message: {zad2.get_message_type(info)}")

@click.command()
@click.option('--logs', default=logs[0])
@click.option('--time', default=1)
@click.option('--victim', default=None)
def brute(args):
    print(f"Attackers with given time, ip and number of attempts: {zad_dod.brute_guard(args.logs, args.time, args.victim)}")

@click.command()
@click.option('--logging', default="debug")
def lvl(logging):
    if logging.lower() == "info":
        logging.basicConfig(encoding='utf-8', level=logging.INFO)
    elif logging.lower() == "warning":
        logging.basicConfig(encoding='utf-8', level=logging.WARNING)
    elif logging.lower() == "error":
        logging.basicConfig(encoding='utf-8', level=logging.ERROR)
    elif logging.lower() == "critical":
        logging.basicConfig(encoding='utf-8', level=logging.CRITICAL)
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

commands.add_command(path_to_file)
commands.add_command(mean)
commands.add_command(raw)
commands.add_command(usr)
commands.add_command(ipv4)
commands.add_command(r_log)
commands.add_command(freq)
commands.add_command(mess)
commands.add_command(brute)
commands.add_command(lvl)

if __name__ == "__main__":
    commands()
