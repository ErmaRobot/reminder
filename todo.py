from datetime import datetime

import remDB

def todo(arg, db):
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

  report = 'Reminder:\n'
  i = 1
  for event in soutput:
    report += '_{}: {}\n'.format(str(i).zfill(2), event.message)
    i += 1
  for event in routput:
    report += '_{}: {}\n'.format(str(i).zfill(2), event.message)
    i += 1

  todofilename = 'TODO_{}.txt'.format(int(stamp))
  todofile = open(todofilename, 'w') 
  todofile.write(report)

  return ('GOOD', f'{todofilename}\n')
