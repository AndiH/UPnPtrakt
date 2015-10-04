from trakt import init, core, tv
import trakt

def getTraktEpisode(show, seasonNumber, episodeNumber):
	return trakt.tv.TVEpisode(show.trakt, seasonNumber, episodeNumber)
	

def getTraktEpisodeInfo(showName, seasonNumber, episodeNumber, seriesWhitelist, seriesMismatched):
	if (showName in seriesMismatched):
		showName = seriesMismatched[showName]

	if (showName in seriesWhitelist):
		traktId = seriesWhitelist[showName]
		show = trakt.tv.TVShow(traktId)
	else:
		showName = showName.replace("(", "").replace(")", "").replace(":", "")
		# print showName
		# print trakt.tv.search(showName, search_type="show")
		show = trakt.tv.search(showName, search_type="show")[0]
	episode = getTraktEpisode(show, seasonNumber, episodeNumber)
	# print episode
	return episode

def getTraktEpisodeInfoFlat(episode):
	show = trakt.tv.TVShow(episode.show)
	return (show.title, show.trakt, episode.season, episode.episode, episode.title, episode.trakt)

def convertFlatEpisodeToTraktEpisode(showId, season, ep):
	return trakt.tv.TVEpisode(showId, season, ep)

def postNewEpisodesToTrakt(newEpisodes):
	for episode in newEpisodes:
		episode = convertFlatEpisodeToTraktEpisode(episode[1], episode[2], episode[3])
		episode.scrobble(100, 1.0, 1.0).finish()
