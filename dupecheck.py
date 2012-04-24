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

if __name__ == "__main__":

  names = [
        "House.S08E17.720p.HDTV.X264-DIMENSION.mkv.torrent",
        "House.S08E17.720p.WEB-DL.DD5.1.H.264-POD.mkv.torrent",
        "New.Girl.S01E21.720p.HDTV.X264-DIMENSION.mkv.torrent",
        "New.Girl.S01E21.720p.WEB-DL.DD5.1.H.264-NFHD.torrent",
        "Community.S03E16.720p.HDTV.X264-DIMENSION.mkv.torrent",
        "30.Rock.S06E18.720p.HDTV.X264-DIMENSION.mkv.torrent",
        "The.Office.US.S08E21.720p.HDTV.X264-DIMENSION.mkv.torrent",
        "30.Rock.S06E18.720p.WEB-DL.DD5.1.H.264-POD.mkv.torrent",
        "Grimm.S01E18.720p.HDTV.X264-DIMENSION.mkv.torrent",
        "Grimm.S01E18.720p.HDTV.X264-DIMENSION.mkv.torrent",
        "Fringe.S04E19.720p.HDTV.X264-DIMENSION.mkv.torrent",
        "Grimm.S01E18.Cat.And.Mouse.720p.WEB-DL.DD5.1.H.264-ECI.mkv.torrent",
        "Fringe.S04E19.Letters.of.Transit.720p.WEB-DL.DD5.1.H.264-Frost.mkv.torrent",
        "Game.of.Thrones.S02E04.720p.HDTV.DD5.1.x264-CEZAR.mkv%5BBmTV%5D.torrent",
        "House.S08E18.720p.HDTV.X264-DIMENSION.mkv.torrent",
        "House.S08E18.720p.WEB-DL.DD5.1.H.264-POD.mkv.torrent" ]


  try:
    duplicate_db = open('duplicate.dat', 'rb')
    db = pickle.load( duplicate_db )
    duplicate_db.close()
  except:
    db = {}

  for name in names:
    if duplicate( db, name ):
      print name

  duplicate_db = open('duplicate.dat', 'wb')
  pickle.dump( db, duplicate_db )
  duplicate_db.close()
