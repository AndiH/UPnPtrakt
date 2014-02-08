import trakt_login
import trakt.tv
import episodeMatcher as matcher
import pprint
pp = pprint.PrettyPrinter(indent=4)

trakt.tv.setup(apikey=trakt_login.apikey)

# print matcher.samplestring
def getEpisodeInfo(showName, seasonNumber, episodeNumber):
	show = trakt.tv.search.shows(showName)
	episode = trakt.tv.show.episode(show[0]['tvdb_id'], seasonNumber, episodeNumber)
	return (showName, show[0]['tvdb_id'], seasonNumber, episodeNumber, episode['episode']['title'], episode['episode']['tvdb_id'])
	
# episodeInfo = matcher.getEpisodeInfo(matcher.samplestring)

# show = trakt.tv.search.shows(episodeInfo[0])
# pp.pprint(show[0])
# episode =  trakt.tv.show.episode(show[0]['tvdb_id'], episodeInfo[1], episodeInfo[2])
# pp.pprint(episode)
# print episode['episode']['title'], episode['episode']['tvdb_id']

# https://github.com/z4r/python-trakt
# http://trakt.tv/api-docs/authentication
