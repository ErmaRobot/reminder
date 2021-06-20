from datetime import datetime
import re

import remDB
import date

def addSingle(msg, db):
  match = re.match(date.regex, msg)
  dl = msg[match.start():match.end()].split('-')
  eventDate = datetime(int(dl[2]), int(dl[0]), int(dl[1])).timestamp()
  eventMsg = msg[match.end() + 1:]
  return db.addSingle(eventDate, eventMsg)

def rmSingle(msg, db):
  return db.rmSingle(msg)

def listSingle(msg, db):
  if msg == 'future':
    today = datetime.today()
    (result, output) = db.getSingleEvents(minstamp = datetime(today.year, today.month, today.day).timestamp())
  elif msg == 'past':
    today = datetime.today()
    (result, output) = db.getSingleEvents(maxstamp = datetime(today.year, today.month, today.day).timestamp())
  else:
    (result, output) = db.getSingleEvents()
  
  if result == 'FAIL':
    return (result, output)

  report = ''
  for event in output:
    date = datetime.fromtimestamp(event.date)
    report += f'{event.id}) {event.message}; {date.month}/{date.day}/{date.year}\n'
  return ('GOOD', report)
