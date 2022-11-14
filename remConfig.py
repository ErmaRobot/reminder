import os
import pwd

curUserNm = pwd.getpwuid(os.getuid()).pw_name

path = '/var/local/reminder/'
eventFile = f'{curUserNm}.el'
delim = ';~;'
