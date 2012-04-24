import re
import cPickle as pickle

def episode_data( episode_name ):
  patterns = [
    '''^((?P<name>.+?)[ \._\-]+)
    [Ss](?P<season>[0-9]+)[\.\- ]?
    [Ee](?P<episode>[0-9]+)
    [^\\/]*$''',

    '''^((?P<name>.+?)\.)
    (?P<season>[0-9]+)[x]?
    (?P<episode>[0-9]+)
    [^\\/]*$''',
    ]

  found = False
  for pattern in patterns:
    regex = re.compile(pattern, re.VERBOSE)
    match = regex.match( episode_name )
    if match:
      matchgroups = match.groupdict().keys()

      found = True

      name = match.group( "name" )
      season = int( match.group( "season" ) )
      episode = int( match.group( "episode" ) )

      return [name, season, episode]

  return [None, None, None]

def duplicate( db, name ):
  series, season, episode = episode_data( name )
  if series is None:
    return True

  if not db.has_key( series ):
    db[ series ] = {}

  if not db[series].has_key( season ):
    db[ series ][ season ] = []
  
  if episode in db[ series ][ season ]:
    return True
  else:
    db[ series ][ season ].append( episode )
    return False

