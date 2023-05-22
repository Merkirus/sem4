import pytest
import log_entry

@pytest.mark.parametrize(
    'raw_log, date',
    [
        ('Dec 10 06:55:46 LabSZ sshd[24200]: reverse mapping checking getaddrinfo for ns.marryaldkfaczcz.com [173.234.31.186] failed - POSSIBLE BREAK-IN ATTEMPT!',
         'Dec 10 06:55:46'),
        ('Dec 10 07:11:42 LabSZ sshd[24224]: input_userauth_request: invalid user chen [preauth]',
         'Dec 10 07:11:42'),
        ('Dec 10 11:04:42 LabSZ sshd[25539]: pam_unix(sshd:auth): authentication failure; logname= uid=0 euid=0 tty=ssh ruser= rhost=103.99.0.122 ',
         'Dec 10 11:04:42')
    ]
)
def test_date_extract(raw_log, date):
    assert log_entry.OtherEntry(raw_log).time == date

@pytest.mark.parametrize(
    'raw_log, ip',
    [
        ('Dec 10 06:55:46 LabSZ sshd[24200]: reverse mapping checking getaddrinfo for ns.marryaldkfaczcz.com [173.234.31.186] failed - POSSIBLE BREAK-IN ATTEMPT!',
         '173.234.31.186'),
        ('Dec 10 07:11:42 LabSZ sshd[24224]: input_userauth_request: invalid user chen [preauth]',
         None),
        ('Dec 10 11:04:42 LabSZ sshd[25539]: pam_unix(sshd:auth): authentication failure; logname= uid=0 euid=0 tty=ssh ruser= rhost=666.959.0.122 ',
         None)
    ]
)
def test_ip_extract(raw_log, ip):
    res = log_entry.OtherEntry(raw_log).get_ipv4()
    if res:
        assert res.ipv4 == ip
    else:
        assert res == ip

@pytest.mark.parametrize(
    'raw_log, _type',
    [
        ('Dec 10 06:55:48 LabSZ sshd[24200]: Failed password for invalid user webmaster from 173.234.31.186 port 38926 ssh2',
         log_entry.FailedEntry),
        ('Dec 10 07:27:55 LabSZ sshd[24239]: pam_unix(sshd:auth): authentication failure; logname= uid=0 euid=0 tty=ssh ruser= rhost=112.95.230.3  user=root',
         log_entry.OtherEntry),
        ('Dec 10 09:32:20 LabSZ sshd[24680]: Accepted password for fztu from 119.137.62.142 port 49116 ssh2',
         log_entry.AcceptedEntry),
        ('Dec 10 11:04:41 LabSZ sshd[25534]: error: Received disconnect from 103.99.0.122: 14: No more user authentication methods available. [preauth]',
         log_entry.ErrorEntry)
    ]
)
def test_type_append_journal(raw_log, _type):
    journal = log_entry.SSHLogJournal()
    journal.append(raw_log.rstrip())
    assert isinstance(journal[-1], _type) 

