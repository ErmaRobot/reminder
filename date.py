from datetime import datetime

import remDB

regex = r'((0[1-9])|(1[0-2]))-(([0-2][0-9])|(3[0-1]))-([12][0-9]{3})' 

def date(arg, db):
  stamp = 0

  if len(arg) == 0:
    t = datetime.today()
    stamp = datetime(t.year, t.month, t.day).timestamp() 
  else:
    dl = arg.split('-')
    stamp = datetime(int(dl[2]), int(dl[0]), int(dl[1])).timestamp() 

  (result, soutput) = db.getSingleEvents(stamp, stamp)
  if result == 'FAIL':
    return (result, soutput)
  (result, routput) = db.getRepeatEvents(stamp)
  if result == 'FAIL':
    return (result, routput)

  report = ''
  i = 1
  for event in soutput:
    report += '{}: {}\n'.format(str(i).zfill(2), event.message)
    i += 1
  for event in routput:
    report += '{}: {}\n'.format(str(i).zfill(2), event.message)
    i += 1

  return ('GOOD', report)
