from datetime import datetime
import remConfig

delim = ';~;'
path = remConfig.path
eventFile = remConfig.eventFile

class SingleEvent:
  def __init__(self, stamp, msg, id):
    self.date = stamp
    self.message = msg
    self.id = id

class RepeatEvent:
  def __init__(self, pat, msg, stamp, id):
    self.pattern = pat
    self.message = msg
    self.creation = stamp
    self.id = id

class EventDB:
  repeat = {'open':[], 'closed':[]}
  single = [] 
  single_id = 's0'
  repeat_id = 'r0'

  def __init__(self):
    eventlist = open(path+eventFile, 'r')
    sid = 0
    rid = 0

    for event in eventlist:
      if event[0] == '#':
        section = event[1:-1]
        continue

      data = tuple(event[:-1].split(delim))
      did = int(data[-1][1:])
      if section == 'open':
        self.repeat['open'].append(RepeatEvent(data[0], data[1], float(data[2]), data[3]))
        if did > rid:
          rid = did
      elif section == 'closed':
        self.repeat['closed'].append(RepeatEvent(data[0], data[1], float(data[2]), data[3]))
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
      eventlist.write(f'{event.pattern}{delim}{event.message}{delim}{event.creation}{delim}{event.id}\n')
    eventlist.write('#closed\n')
    for event in self.repeat['closed']:
      eventlist.write(f'{event.pattern}{delim}{event.message}{delim}{event.creation}{delim}{event.id}\n')
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
      if event.pattern[0] == 'y':
        if event.pattern[1:] == f'{str(givenDate.month).zfill(2)}{str(givenDate.day).zfill(2)}':
          events.append(event)
      elif event.pattern[0] == 'm':
        if event.pattern[1:] == f'{str(givenDate.day).zfill(2)}':
          events.append(event)
      elif event.pattern[0] == 'd':
        events.append(event)    
      elif event.pattern[0] == 'w':
        weekday = daysOfTheWeek[givenDate.weekday()]
        if weekday in event.pattern[1:]:
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

  def addRepeat(self, pat, msg):
    eid = int(self.repeat_id[1:])
    stamp = datetime.today().timestamp()
    event = RepeatEvent(f'{pat}', msg, stamp, 'r{}'.format(eid + 1))
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

