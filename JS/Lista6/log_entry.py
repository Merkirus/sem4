import re
import abc

regex = r'(\w{3} \d{2} \d{2}:\d{2}:\d{2}) (?:(\w+) sshd(\[\d+\])): (.*)'
date_regex = r'\b\w{3} \d{2} \d{2}:\d{2}:\d{2}\b'
ipv4_regex = r'.*?((?:\d{1,3}\.){3}\d{1,3}).*'
failed_pass = r'\bFailed password\b'
accepted_pass = r'\bAccepted password\b'
error_reg = r'\berror\b'
user_validate = r'^[a-z_][a-z0-9_-]{0,31}$'
user_regex = r'.*user[ =]?(.*?)\s|.*password for (.*?)\s'

class IPv4Address():
    def __init__(self, __raw_log) -> None:
        ipv4_gr = re.match(ipv4_regex, __raw_log)
        ips = []
        if ipv4_gr:
            for entry in ipv4_gr.groups():
                ips.append(entry)
        self.ipv4 = ips[0] if len(ips) > 0 else None

class SSHLogEntry(metaclass=abc.ABCMeta):
    def __init__(self, raw_log) -> None:
        self.__raw_log = raw_log
        gr = re.match(regex, raw_log)
        self.time = gr.group(1) # pyright: ignore
        self.host_name = gr.group(2) # pyright: ignore
        self.pid = gr.group(3)[1:-1] # pyright: ignore

    def get_ipv4(self):
        ip = IPv4Address(self.__raw_log)
        return ip if ip.ipv4 else None

    @property
    def has_ip(self):
        return True if self.get_ipv4() else False

    @abc.abstractmethod
    def validate(self):
        match = re.match(regex,self.__raw_log)
        if not match:
            return False

    def __str__(self) -> str:
        return self.__raw_log

    def __repr__(self) -> str:
        return self.__raw_log

    def __eq__(self, __value) -> bool:
        if isinstance(__value, SSHLogEntry):
            return self.pid == __value.pid
        return False

    def __lt__(self, __value) -> bool:
        if isinstance(__value, SSHLogEntry):
            return self.pid < __value.pid
        return False

    def __gt__(self, __value) -> bool:
        if isinstance(__value, SSHLogEntry):
            return self.pid > __value.pid
        return False

class Creator():
    def create(self, raw_log) -> SSHLogEntry:
        if re.match(failed_pass,raw_log):
            return FailedEntry(raw_log)
        elif re.match(accepted_pass,raw_log):
            return AcceptedEntry(raw_log)
        elif re.match(error_reg,raw_log):
            return ErrorEntry(raw_log)
        else:
            return OtherEntry(raw_log)

class Accepted(Creator):
    def create(self, raw_log) -> SSHLogEntry:
        return AcceptedEntry(raw_log)

class Error(Creator):
    def create(self, raw_log) -> SSHLogEntry:
        return ErrorEntry(raw_log)

class Failed(Creator):
    def create(self, raw_log) -> SSHLogEntry:
        return FailedEntry(raw_log)

class Other(Creator):
    def create(self, raw_log) -> SSHLogEntry:
        return OtherEntry(raw_log)

class SSHLogJournal():
    def __init__(self, logs=[]) -> None:
        self.logs = logs
        self.factory = Creator()

    def append(self, string):
        log = self.factory.create(string)
        if log.validate():
            self.logs.append(log)

    def get_logs_by_ip(self, ipv4):
        results = []
        for entry in self.logs:
            entry_log = entry.get_ipv4()
            if not entry_log:
                continue
            if entry_log.ipv4 == ipv4:
                results.append(entry)
        return results

    def __len__(self):
        return len(self.logs)

    def __iter__(self):
        return self

    def __contains__(self, __value):
        if __value in self.logs:
            return True
        return False

    def __getattr__(self, attr):
        attr = str(attr)
        attr = attr[1:]
        match = re.match(date_regex,attr.replace("_",":").replace(":"," ", 2))
        if match:
            results = []
            for entry in self.logs:
                inner_match = re.match(regex, entry._SSHLogEntry__raw_log)
                if not inner_match:
                    continue
                if inner_match.group(1) == attr.replace("_",":").replace(":"," ", 2):
                    results.append(entry)
            return results

        if re.match(ipv4_regex, attr.replace("_",".")):
            return self.get_logs_by_ip(attr.replace("_","."))
        if attr.isnumeric():
            num = int(attr)
            if num >= 0 and num < len(self.logs):
                return self.logs[num]
        return f"Attribute does not exist: {attr}"

    def __getitem__(self, __value):
        return self.logs[__value]


class FailedEntry(SSHLogEntry):
    def __init__(self, raw_log) -> None:
        super().__init__(raw_log)

    def validate(self):
        super().validate()
        val = re.match(failed_pass, self.__raw_log)
        if val:
            return True
        return False

class AcceptedEntry(SSHLogEntry):
    def __init__(self, __raw_log) -> None:
        super().__init__(__raw_log)

    def validate(self):
        super().validate()
        val = re.match(accepted_pass, self.__raw_log)
        if val:
            return True
        return False

class ErrorEntry(SSHLogEntry):
    def __init__(self, __raw_log) -> None:
        super().__init__(__raw_log)

    def validate(self):
        super().validate()
        val = re.match(error_reg, self.__raw_log)
        if val:
            return True
        return False

class OtherEntry(SSHLogEntry):
    def __init__(self, __raw_log) -> None:
        super().__init__(__raw_log)

    def validate(self):
        return True

class SSHUser():
    def __init__(self, raw_log) -> None:
        match_user = re.match(user_regex,raw_log)
        user = None
        if match_user:
            for entry in match_user.groups():
                if entry:
                    user = entry
        self.user = user
        match_date = re.match(regex,raw_log)
        self.last_log_date = match_date.group(1) # pyright: ignore

    def validate(self):
        if not self.user:
            return False
        match = re.match(user_validate, self.user)
        if match:
            return True
        return False


if __name__ == "__main__":
    journal = SSHLogJournal()
    with open('SSH_2k.log') as f:
        for _ in range(10):
            line = f.readline()
            if not line:
                break
            journal.append(line.rstrip())

    test_list = journal[1:3]
    usr1 = SSHUser(test_list[0]._SSHLogEntry__raw_log)
    usr2 = SSHUser(test_list[1]._SSHLogEntry__raw_log)

    test_list.append(usr1)
    test_list.append(usr2)

    print(journal._1)
    print(journal._173_234_31_186)
    print(journal._Dec_10_06_55_46)

    for item in test_list:
        print(item.validate())
