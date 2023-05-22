import re
from enum import Enum

my_regex = r'(\w{3} \d{2} \d{2}:\d{2}:\d{2}) (\w+ sshd\[\d+\]): (.*)'
ipv4_regex2 = r'\b((?:\d{1,3}\.){3}\d{1,3})\b'
ipv4_regex = r'.*?((?:\d{1,3}\.){3}\d{1,3}).*'
user_regex = r'.*user[ =]?(.*?)\s|.*password for (.*?)\s'
break_in = r'\bPOSSIBLE BREAK-IN ATTEMPT!$'
connection_closed = r'\bConnection closed\b'
received_disconnect = r'\bReceived disconnect\b'
failed_pass = r'\bFailed password\b'
accepted_pass = r'\bAccepted password\b'
invalid_user = r'\binvalid\b'
invalid_pass = r'\bauthentication failure\b'

class Event(Enum):
    Break = "Break-in event"
    Connection = "Connection closed event"
    Failed = "Failed login attempt event"
    Success = "Successful login attempt event"
    Invalidusr = "Invalid user event"
    Invalidpass = "Invalid password event"
    Other = "Other"

def raw_log_to_dict(raw_log):
    groups = re.match(my_regex, raw_log)
    return {"raw_log": raw_log,
            "date": groups.group(1),#pyright: ignore
            "sshd": groups.group(2),#pyright: ignore
            "info": groups.group(3) #pyright: ignore
            }

def get_ipv4s_from_log(log):
    ipv4_groups = re.match(ipv4_regex, log["raw_log"])
    if ipv4_groups:
        return [x for x in ipv4_groups.groups()]
    return []

def get_user_from_log(log):
    regex_groups = re.match(user_regex, log["raw_log"]) # if user then group either 1 or 2 not None
    if not regex_groups:
        return None
    for entry in regex_groups.groups(): #pyright: ignore
        if entry:
            return entry

def get_message_type(event):
    result = re.match(break_in, event)
    if result:
        return Event.Break.value
    result = re.match(connection_closed, event)
    if result:
        return Event.Connection.value
    result = re.match(received_disconnect,event)
    if result:
        return Event.Connection.value
    result = re.match(failed_pass, event)
    if result:
        return Event.Failed.value
    result = re.match(accepted_pass, event)
    if result:
        return Event.Success.value
    result = re.match(invalid_user, event)
    if result:
        return Event.Invalidusr.value
    result = re.match(invalid_pass, event)
    if result:
        return Event.Invalidpass.value
    return Event.Other.value
