import date
import todo

import repeat
#addRepeat
#closeRepeat
#rmRepeat
#patterns
#listRepeating

import single
#addSingle
#rmSingle
#listSingle

eid = r'[rs][0-9]+'
msg = r'(\S| ){1,140}'

command = {
            'date':date.regex,
            'todo':r'todo( '+date.regex+')?',
            'addRepeat':r'addRepeat ('+repeat.pat+') ('+msg+')',
            'addSingle':r'addSingle ('+date.regex+') ('+msg+')',
            'closeRepeat':r'closeRepeat( '+eid+')',
            'rmRepeat':r'rmRepeat( '+eid+')',
            'rmSingle':r'rmSingle( '+eid+')',
            'patterns':r'patterns',
            'listRepeat':r'listRepeat(( open)|( closed))?',
            'listSingle':r'listSingle(( future)|( past))?'
          }

function = {
             'date':date.date,
             'todo':todo.todo,
             'addRepeat':repeat.addRepeat,
             'addSingle':single.addSingle,
             'closeRepeat':repeat.closeRepeat,
             'rmRepeat':repeat.rmRepeat,
             'rmSingle':single.rmSingle,
             'patterns':repeat.patterns,
             'listRepeat':repeat.listRepeating,
             'listSingle':single.listSingle,
          }
