Reminder Design Doc

The goal of the reminder app is to have a utility accessible on the command line
and that can be ran at startup. It will produce a list of events for the day that 
the user has asked to be reminded of. It can also write those events to a text file
in the format of a todo list.

The reminder app will be used through the command line with a few commands. 
  + reminder - list todays events
  + reminder [date] - list that days events
  + reminder todo - list todays events as a todo list in text file
  + reminder addRepeat - add a repeating event
  + reminder addSingle - add a one time event
  + reminder closeRepeat - stop displaying repeating event, but don't delete
  + reminder rmRepeat - remove repeating event
  + reminder rmSingle - remove a one time event
  + reminder patterns - display pattern format for repeating events
  + reminder listRepeating [open|closed] - list repeating events
  + reminder listSingle [future|past] - list single events, today is in future

Events will be written to the eventList file which will have three sections.
  + open   - repeat events to be shown will be in this section
      in descending of creation timestamp.
  + closed - repeat events not to be shown in current and future lists. Will
      still show up in past lists depending on date of creation and repetition
      pattern.
  + single - one time events in descending timestamp order. Event
      will be displayed on the list if the timestamp corresponds to the given 
      date.

Event structure will be different between repeating and single events. The 
information reguired of a repeating event are:
  Given:
  + pattern of repetition
  + time of event
  + message to be reminded of
  Generated
  + timestamp at creation
  + id assigned at creation

The information required of a single event are:
  Given:
  + date of the event
  + time of the event
  + message to be reminded of
  Generated
  + id assigned at creation

There are four types of repeating events with their own syntax.
  + yearly: y followed by month, 2 digits, followed by day 2 digits
  + monthly: m follwed by day, 2 digits
  + daily: d not followed by anything
  + weekly: w followed by day of the week,
      s - sunday
      m - monday
      t - tuesday
      w - wednesday
      h - thursday
      f - friday
      a - saturday
     followed by an integer number of weeks between events, followed by a colon,
     followed by an integer number as the offset into the cycle

Examples of the weekly patterns:
  every monday
    wm0:0
    ||| |
    ||| no offset
    ||no weeks skipped
    |on monday
    weekly
  every other monday
    wm1:0
  every other monday and wednesday
    wmw1:0
  every other monday and wednesday starting next week
    wmw1:1
    |||| |
    |||| offset of 1 week
    |||skip one week between events
    ||reminder on wednesday
    |reminder on monday
    weekly

remCom.py collects all the commands and makes them available to the main reminder
script. reminder will parse the command line according to the regex in the 
command dictionary, and will call functions based on the function dictionary. The
purpose of this is to make the main function agnostic to the other commands, and
make it easier to add and change commands without having to change the main code.

To add a command, one would only have to add a command to an existing .py file, or
make a new file and import it in remCom.py. After that make an entry into command
dictionary with the name of the new command paired with a regex for recognizing 
it. Then make an entry in the function dictionary with a call to the new function.

All commands are expected to take a string containing args or nothing at all.

All commands are expected to return a tuple with the first vale being:
  + 'GOOD' - the function worked as expected, the second value will be a string
      to be printed to STDOUT.
  + 'FAIL' - the funtion did not work as expected, the second value will be a 
      string breifly explaining the problem.

