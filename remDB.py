from datetime import datetime
from datetime import timedelta

import remConfig

delim = remConfig.delim
path = remConfig.path
eventFile = remConfig.eventFile

class SingleEvent:
  def __init__(self, stamp, msg, iden):
    self.date = stamp
    self.message = msg
    self.id = iden

class RepeatEvent:
  y_month  = 0
  y_day    = 1 
  m_day    = 0
  w_days   = 0
  w_period = 1
  w_offset = 2

  def __init__(self, period, idata, msg, stamp, iden):
    self.period = period
    self.data = []
    for i in range(len(idata)):
      if i >= 3:
        break
      self.data.append(idata[i])
    self.message = msg
    self.creation = stamp
    self.id = iden

  def pattern(self):
    pattern = f'{self.period}'
    if self.period == 'w':
      pattern += self.data[RepeatEvent.w_days]
      pattern += f'{self.data[RepeatEvent.w_period]}:'
      pattern += f'{self.data[RepeatEvent.w_offset]}'
    elif self.period == 'y':
      pattern += f'{self.data[RepeatEvent.y_month]}'.zfill(2)
      pattern += f'{self.data[RepeatEvent.y_day]}'.zfill(2)
    elif self.period == 'm':
      pattern += f'{self.data[RepeatEvent.m_day]}'.zfill(2)
    return pattern

  def parse(pattern_string):
    data = []
    if pattern_string[0] == 'w':
      period = 1
      while pattern_string[period] not in '0123456789':
        period += 1
      data.append(pattern_string[1:period])
      colon = period
      while pattern_string[colon] != ':':
        colon += 1
      data.append(int(pattern_string[period:colon]))
      offset = colon + 1
      data.append(int(pattern_string[offset:]))
    elif pattern_string[0] == 'y':
      data.append(int(pattern_string[1:3]))
      data.append(int(pattern_string[3:]))
    elif pattern_string[0] == 'm':
      data.append(int(pattern_string[1:]))
    else: #pattern_string[0] == 'd'
      pass
    return (pattern_string[0], data)

class EventDB:
  repeat = {'open':[], 'closed':[]}
  single = [] 
  single_id = 's0'
  repeat_id = 'r0'

  def __init__(self):
    try:
      eventlist = open(path+eventFile, 'r')
    except:
      open(path+eventFile, 'w').close()
      return
    sid = 0
    rid = 0

    for event in eventlist:
      if event[0] == '#':
        section = event[1:-1]
        continue

      data = tuple(event[:-1].split(delim))
      did = int(data[-1][1:])
      if section == 'open':
        (pat, d) = RepeatEvent.parse(data[0])
        self.repeat['open'].append(RepeatEvent(pat, d, data[1], float(data[2]), data[3]))
        if did > rid:
          rid = did
      elif section == 'closed':
        (pat, d) = RepeatEvent.parse(data[0])
        self.repeat['closed'].append(RepeatEvent(pat, d, data[1], float(data[2]), data[3]))
        if did > rid:
          rid = did
      elif section == 'single':
        self.single.append(SingleEvent(float(data[0]), data[1], data[2]))
        if did > sid:
          sid = did

    self.single.sort(key=lambda x: x.date)
    self.single_id = f's{sid}'
    self.repeat_id = f'r{rid}'
    eventlist.close()

  def save(self):
    eventlist = open(path+eventFile, 'w')

    eventlist.write('#open\n')
    for event in self.repeat['open']:
      eventlist.write(f'{event.pattern()}{delim}{event.message}{delim}{event.creation}{delim}{event.id}\n')
    eventlist.write('#closed\n')
    for event in self.repeat['closed']:
      eventlist.write(f'{event.pattern()}{delim}{event.message}{delim}{event.creation}{delim}{event.id}\n')
    eventlist.write('#single\n')
    for event in self.single:
      eventlist.write(f'{event.date}{delim}{event.message}{delim}{event.id}\n')

    eventlist.close()

  def getSingleEvents(self, minstamp=None, maxstamp=None):
    if minstamp is None and maxstamp is None or len(self.single) == 0:
      return ('GOOD', self.single)

    minindex = 0
    maxindex = len(self.single) - 1

    while minstamp is not None and minstamp > self.single[minindex].date:
      minindex += 1
      if minindex > len(self.single) - 1:
        break

    if minindex >= len(self.single):
      return ('GOOD', [])
  
    while maxstamp is not None and maxstamp < self.single[maxindex].date:
      maxindex -= 1
      if maxindex < 0:
        break

    if maxindex < 0:
      return ('GOOD', [])

    if minindex > maxindex:
      return ('GOOD', [])

    return ('GOOD', self.single[minindex:maxindex+1])

  def getRepeatEvents(self, stamp):
    givenDate = datetime.fromtimestamp(stamp)
    daysOfTheWeek = ['m', 't', 'w', 'h', 'f', 'a', 's']
    events = []
    for event in self.repeat['open']:
      if event.period == 'y':
        if event.data[RepeatEvent.y_month] == givenDate.month and event.data[RepeatEvent.y_day] == givenDate.day:
          events.append(event)
      elif event.period == 'm':
        if event.data[RepeatEvent.m_day] == givenDate.day:
          events.append(event)
      elif event.period == 'd':
        events.append(event)    
      elif event.period == 'w':
        if daysOfTheWeek[givenDate.weekday()] in event.data[RepeatEvent.w_days]:
          origin = datetime.fromtimestamp(event.creation)
          weeks = int((givenDate - origin - timedelta(days=givenDate.weekday()) - timedelta(days=origin.weekday())).days / 7)
          if event.data[RepeatEvent.w_offset] == weeks % (event.data[RepeatEvent.w_period] + 1):
            events.append(event)
    return ('GOOD', events)

  def getAllRepeatEvents(self, openEvents=False, closedEvents=False):
    events = []
    if openEvents:
      events += self.repeat['open']
    if closedEvents:
      events += self.repeat['closed']

    return ('GOOD', events)

  def addSingle(self, stamp, msg):
    eid = int(self.single_id[1:])
    event = SingleEvent(stamp, msg, 's{}'.format(eid + 1))
    self.single.append(event)
    self.single.sort(key=lambda x: x.date)
    self.single_id = event.id 
    return ('GOOD', '')

  def rmSingle(self, eid):
    for i in range(len(self.single)):
      if (self.single[i]).id == eid:
        self.single.pop(i)
        return ('GOOD', '')
    return ('FAIL', 'No such event')

  def addRepeat(self, period, data, msg):
    eid = int(self.repeat_id[1:])
    stamp = datetime.today().timestamp()
    event = RepeatEvent(period, data, msg, stamp, f'r{eid + 1}')
    self.repeat['open'].append(event)
    self.repeat_id = event.id
    return ('GOOD', '')

  def closeRepeat(self, eid):
    for i in range(len(self.repeat['open'])):
      if self.repeat['open'][i].id == eid:
        self.repeat['closed'].append(self.repeat['open'].pop(i))
        return ('GOOD', '')
    return ('FAIL', 'No such event')

  def rmRepeat(self, eid):
    for i in range(len(self.repeat['open'])):
      if self.repeat['open'][i].id == eid:
        self.repeat['open'].pop(i)
        return ('GOOD', '')
    for i in range(len(self.repeat['closed'])):
      if self.repeat['closed'][i].id == eid:
        self.repeat['closed'].pop(i)
        return ('GOOD', '')
    return ('FAIL', 'No such event')

