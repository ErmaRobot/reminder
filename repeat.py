from datetime import datetime

import remDB

yearly = r'y((0[0-9])|(1[0-2]))(([0-2][0-9])|(3[0-1]))'
monthly = r'm(([0-2][0-9])|(3[0-1]))'
daily = r'd'
weekly = r'w[smtwhfa]{1,7}[0-9]+:[0-9]+'
pat =r'('+yearly+r')|('+monthly+r')|('+daily+r')|('+weekly+r')'

def addRepeat(msg, db):
  split = msg.index(' ')
  pat = msg[:split]
  split += 1
  msg = msg[split:]
  db.addRepeat(pat, msg)
  return ('GOOD', '')

def closeRepeat(msg, db):
  return db.closeRepeat(msg)

def rmRepeat(msg, db):
  return db.rmRepeat(msg)

def listRepeating(msg, db):
  (result, output) = ('FAIL', 'Something went wrong with getting repeat events')
  if len(msg) == 0:
    (result, output) = db.getAllRepeatEvents(openEvents=True, closedEvents=True)
  elif msg == 'open':
    (result, output) = db.getAllRepeatEvents(openEvents=True)
  elif msg == 'closed':
    (result, output) = db.getAllRepeatEvents(closedEvents=True)
  if result == 'FAIL':
    return (resul, output)
  report = ''
  for event in output:
    report += f'{event.id}) {event.message}, {event.pattern}\n'
  return ('GOOD', report)

def patterns(msg, db):
  report  = 'Patterns for Repeating Events\n'
  report += 'Events can repeat yearly, monthly, daily, or weekly\n'
  report += 'Yearly: ymmdd - y, denotes yearly event, mm, month w/ 2  digits, dd, day w/ 2 digits\n'
  report += 'Monthly: mdd - m, denotes monthly event, dd, day w/ 2 digits\n'
  report += 'Daily: d - d, denotes daily event, no other character is necessary\n'
  report += 'Weekly: w[smtwhfa]{1,7}[0-9]+:[0-9]+ - w, denotes a weekly event, this is the most involved repeating type\n'
  report += '  [smtwhfa]{1,7} - the days of the week that the event is on\n'
  report += '  s - Sunday\n'
  report += '  m - Monday\n'
  report += '  t - Tuesday\n'
  report += '  w - Wednesday\n'
  report += '  h - Thursday\n'
  report += '  f - Friday\n'
  report += '  a - Sunday\n'
  report += '  [0-9]+:[0-9]+ - How many weeks are in the cycle : Offset into the cycle\n'
  report += '  Examples:\n'
  report += '    wmf0:0 - weekly, every monday and friday\n'
  report += '    |||| |\n'
  report += '    |||| no offset\n'
  report += '    |||no weeks skipped\n'
  report += '    ||on friday\n'
  report += '    |on monday\n'
  report += '    weekly\n'
  report += '\n'
  report += '    wmf1:0 - weekly, every other monday and friday, starting this week\n'
  report += '    wmf1:1 - weekly, every other monday and friday, starting next week\n'
  return ('GOOD', report)
