import re

config = '/etc/reminder/config'

path = ''
eventFile = ''

with open(config, 'r') as configFile:
  contents = configFile.read()

  #get Path variable
  pathMatch = re.search('PATH', contents)
  ei = False
  if pathMatch is not None:
    for c in contents[pathMatch.start():]:
      if c == '\n':
        break
      elif c == '=':
        ei = True
        continue
      if ei:
        path += c

  #get File Name variable
  fileMatch = re.search('FILE', contents)
  ei = False
  if fileMatch is not None:
    for c in contents[fileMatch.start():]:
      if c == '\n':
        break
      elif c == '=':
        ei = True
        continue
      if ei:
        eventFile += c

