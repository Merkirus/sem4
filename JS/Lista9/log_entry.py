import re
import abc
import typing

regex: str = r'(\w{3} \d{2} \d{2}:\d{2}:\d{2}) (?:(\w+) sshd(\[\d+\])): (.*)'
date_regex: str = r'\b\w{3} \d{2} \d{2}:\d{2}:\d{2}\b'
# ipv4_regex: str = r'.*?((?:\d{1,3}\.){3}\d{1,3}).*'
ipv4_regex: str = r'.*?((\b25[0-5]|\b2[0-4][0-9]|\b[01]?[0-9][0-9]?)(\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)){3}).*'
failed_pass: str = r'\bFailed password\b'
accepted_pass: str = r'\bAccepted password\b'
error_reg: str = r'\berror\b'
user_validate: str = r'^[a-z_][a-z0-9_-]{0,31}$'
user_regex: str = r'.*user[ =]?(.*?)\s|.*password for (.*?)\s'

class IPv4Address():
    def __init__(self, __raw_log: str) -> None:
        ipv4_gr: re.Match[str] | None = re.match(ipv4_regex, __raw_log)
        ips: list[str] = []
        if ipv4_gr:
            for entry in ipv4_gr.groups():
                ips.append(entry)
        self.ipv4: str | None = ips[0] if len(ips) > 0 else None

class SSHLogEntry(metaclass=abc.ABCMeta):
    def __init__(self, raw_log: str) -> None:
        self.__raw_log: str = raw_log
        gr: re.Match[str] | None = re.match(regex, raw_log)
        self.time: str | None = None
        self.host_name: str | None = None
        self.pid: str | None = None
        if gr:
            self.time = gr.group(1)
            self.host_name = gr.group(2)
            self.pid = gr.group(3)[1:-1]

    def get_ipv4(self) -> IPv4Address | None:
        ip: IPv4Address = IPv4Address(self.__raw_log)
        return ip if ip.ipv4 else None

    @property
    def has_ip(self) -> bool:
        return True if self.get_ipv4() else False

    @abc.abstractmethod
    def validate(self) -> bool:
        match: re.Match[str] | None = re.search(regex,self.__raw_log)
        if not match:
            return False
        return True

    def __str__(self) -> str:
        return self.__raw_log

    def __repr__(self) -> str:
        return self.__raw_log

    def __eq__(self, __value: object) -> bool:
        if isinstance(__value, SSHLogEntry) and self.pid and __value.pid:
            return self.pid == __value.pid
        return False

    def __lt__(self, __value: object) -> bool:
        if isinstance(__value, SSHLogEntry) and self.pid and __value.pid:
            return self.pid < __value.pid
        return False

    def __gt__(self, __value: object) -> bool:
        if isinstance(__value, SSHLogEntry) and self.pid and __value.pid:
            return self.pid > __value.pid
        return False

class FailedEntry(SSHLogEntry):
    def __init__(self, raw_log: str) -> None:
        super().__init__(raw_log)
        self.__raw_log: str = raw_log

    def validate(self) -> bool:
        if not super().validate():
            return False
        val: re.Match[str] | None = re.search(failed_pass, self.__raw_log)
        if val:
            return True
        return False

class AcceptedEntry(SSHLogEntry):
    def __init__(self, __raw_log: str) -> None:
        super().__init__(__raw_log)
        self.__raw_log: str = __raw_log

    def validate(self) -> bool:
        if not super().validate():
            return False
        val: re.Match[str] | None = re.search(accepted_pass, self.__raw_log)
        if val:
            return True
        return False

class ErrorEntry(SSHLogEntry):
    def __init__(self, __raw_log: str) -> None:
        super().__init__(__raw_log)
        self.__raw_log: str = __raw_log

    def validate(self) -> bool:
        if not super().validate():
            return False
        val: re.Match[str] | None = re.search(error_reg, self.__raw_log)
        if val:
            return True
        return False

class OtherEntry(SSHLogEntry):
    def __init__(self, __raw_log) -> None:
        super().__init__(__raw_log)

    def validate(self) -> bool:
        return True

class SSHUser():
    def __init__(self, raw_log) -> None:
        match_user: re.Match[str] | None = re.match(user_regex,raw_log)
        user: str | None = None
        if match_user:
            for entry in match_user.groups():
                if entry:
                    user = entry
        self.user: str | None = user
        match_date: re.Match[str] | None = re.match(regex,raw_log)
        self.last_log_date: str | None = None
        if match_date:
            self.last_log_date = match_date.group(1)

    def validate(self) -> bool:
        if not self.user:
            return False
        match: re.Match[str] | None = re.search(user_validate, self.user)
        if match:
            return True
        return False

class Creator():
    def create(self, raw_log: str) -> SSHLogEntry:
        if re.search(failed_pass,raw_log):
            return FailedEntry(raw_log)
        elif re.search(accepted_pass,raw_log):
            return AcceptedEntry(raw_log)
        elif re.search(error_reg,raw_log):
            return ErrorEntry(raw_log)
        else:
            return OtherEntry(raw_log)

class Accepted(Creator):
    def create(self, raw_log: str) -> AcceptedEntry:
        return AcceptedEntry(raw_log)

class Error(Creator):
    def create(self, raw_log: str) -> ErrorEntry:
        return ErrorEntry(raw_log)

class Failed(Creator):
    def create(self, raw_log: str) -> FailedEntry:
        return FailedEntry(raw_log)

class Other(Creator):
    def create(self, raw_log: str) -> OtherEntry:
        return OtherEntry(raw_log)

class SSHLogJournal():
    def __init__(self, logs:list[SSHLogEntry] = []) -> None:
        self.logs: list[SSHLogEntry] = logs
        self.factory: Creator = Creator()

    def append(self, string: str) -> None:
        log: SSHLogEntry = self.factory.create(string)
        if log.validate():
            self.logs.append(log)

    def get_logs_by_ip(self, ipv4: str) -> list[SSHLogEntry]:
        results: list[SSHLogEntry] = []
        for entry in self.logs:
            entry_log: IPv4Address | None = entry.get_ipv4()
            if not entry_log:
                continue
            if entry_log.ipv4 == ipv4:
                results.append(entry)
        return results

    def __len__(self) -> int:
        return len(self.logs)

    def __iter__(self) -> typing.Self:
        return self

    def __contains__(self, __value: SSHLogEntry) -> bool:
        if __value in self.logs:
            return True
        return False

    def __getattr__(self, attr: str) -> list[SSHLogEntry] | SSHLogEntry | str:
        attr = attr[1:]
        match: re.Match[str] | None = re.match(date_regex,attr.replace("_",":").replace(":"," ", 2))
        if match:
            results: list[SSHLogEntry] = []
            for entry in self.logs:
                inner_match: re.Match[str] | None = re.match(regex, str(entry))
                if not inner_match:
                    continue
                if inner_match.group(1) == attr.replace("_",":").replace(":"," ", 2):
                    results.append(entry)
            return results

        if re.match(ipv4_regex, attr.replace("_",".")):
            return self.get_logs_by_ip(attr.replace("_","."))
        if attr.isnumeric():
            num: int = int(attr)
            if num >= 0 and num < len(self.logs):
                return self.logs[num]
        return f"Attribute does not exist: {attr}"

    def __getitem__(self, __value: slice | int) -> list[SSHLogEntry] | SSHLogEntry:
        return self.logs[__value]

if __name__ == "__main__":
    journal: SSHLogJournal = SSHLogJournal()
    with open('SSH_2k.log') as f:
        for _ in range(10):
            line: str = f.readline()
            if not line:
                break
            journal.append(line.rstrip())

    test_list: typing.Any = journal[1:3]
    usr1: SSHUser = SSHUser(str(test_list[0]))
    usr2: SSHUser = SSHUser(str(test_list[1]))

    test_list.append(usr1)
    test_list.append(usr2)

    print(journal._1)
    print(journal._173_234_31_186)
    print(journal._Dec_10_06_55_46)

    for item in test_list:
        print(item.validate())
