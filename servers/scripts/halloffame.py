#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ddnet import *
import sys
import msgpack
from cgi import escape

reload(sys)
sys.setdefaultencoding('utf8')

def printFooter():
  print """
  </section>
  </article>
  </body>
</html>"""

rankLadder = {}
teamrankLadder = {}
pointsLadder = {}
serversString = ""
players = {}
maps = {}
totalPoints = 0
serverRanks = {}

print header("Hall of Fame - DDraceNetwork", "", "")

f = open("halloffame")
entries = []
for line in f:
  words = line.rstrip('\n').split('\t')
  entries.append(tuple(words))

f = open("releases")
releases = []
for line in f:
  words = line.rstrip('\n').split('\t')
  releases.append(tuple(words))

serversString = ""
mapsString = ""

for x in entries:
  originalMapName, players, time, video = x

  for a in releases:
    date, server, y = a
    try:
      stars, originalMapName2, mapperName = y.split('|')
    except ValueError:
      stars, originalMapName2 = y.split('|')
      mapperName = ""

    if originalMapName2 == originalMapName:
      break

  stars = int(stars)

  mapName = normalizeMapname(originalMapName)

  if not mapperName:
    mbMapperName = ""
  else:
    names = splitMappers(mapperName)
    newNames = []
    for name in names:
      newNames.append('<a href="%s">%s</a>' % (mapperWebsite(name), escape(name)))

    mbMapperName = "<strong>by %s</strong><br/>" % makeAndString(newNames)

  names = splitMappers(players)
  newNames = []
  for name in names:
    newNames.append('<a href="%s">%s</a>' % (playerWebsite(name), escape(name)))

  playerNames = "%s" % makeAndString(newNames)

  formattedMapName = escape(originalMapName)
  mbMapInfo = ""
  try:
    with open('maps/%s.msgpack' % originalMapName, 'rb') as inp:
      unpacker = msgpack.Unpacker(inp)
      width = unpacker.unpack()
      height = unpacker.unpack()
      tiles = unpacker.unpack()

      formattedMapName = '<span title="%dx%d">%s</span>' % (width, height, escape(originalMapName))

      mbMapInfo = "<br/>"
      for tile in sorted(tiles.keys(), key=lambda i:order(i)):
        mbMapInfo += '<span title="%s"><img alt="%s" src="/tiles/%s.png" width="32" height="32"/></span> ' % (description(tile), description(tile), tile)
  except IOError:
    pass

  mapsString += u'<div class="blockreleases release" id="map-%s"><h2 class="inline">%s - %s</h2><br/><h3 class="inline">on <a href="/ranks/%s/#map-%s">%s</a> %s</h3><h3 class="inline"><a href="/ranks/%s">%s Server</a></h3><br/><p>Difficulty: %s, Points: %d<br/><a href="http://youtu.be/%s?list=UUehuq_sbMTEATWVgDvnVy7w"><img class="screenshot" alt="Screenshot" src="/ranks/maps/%s.png" /></a>%s<br/></div>\n' % (escape(mapName), playerNames, time, server, escape(normalizeMapname(originalMapName)), formattedMapName, mbMapperName, server, server.title(), escape(renderStars(stars)), globalPoints(server, stars), video, escape(mapName), mbMapInfo)

serversString += mapsString
serversString += '<span class="stretch"></span></div>\n'

print '<div id="global" class="block"><h2>Hall of Fame</h2>'
print '<p>The Hall of Fame features the best runs of DDraceNetwork, which means:</p>'
print '<ul>'
print '<li>You have the first rank in /top5 or in /top5teams</li>'
print '<li>The map has been released for at least 2 weeks</li>'
print '<li>There are more than a few finishes</li>'
print '</ul>'
print serversString
printFooter()
