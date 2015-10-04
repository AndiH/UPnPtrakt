from trakt import init, core, tv
import trakt

class traktHandler(object):
	"""Class handles the trakt.tv communication"""
	def __init__(self, args):
		super(traktHandler, self).__init__()
		self.cmdlineargs = args
		self.verbose = args.verbose
		if (self.verbose):
			print "Verbose is turned on for traktHandler"
	def getTraktEpisode(self, show, seasonNumber, episodeNumber):
		if (self.verbose):
			"Constructing trakt TVEpisode for", show, "S", seasonNumber, "E", episodeNumber
		return trakt.tv.TVEpisode(show.trakt, seasonNumber, episodeNumber)
	def getTraktEpisodeInfo(self, showName, seasonNumber, episodeNumber, seriesWhitelist, seriesMismatched):
		if (self.verbose):
			print "Generating data for:", showName, "S", seasonNumber, "E",  episodeNumber
		if (showName in seriesMismatched):
			newShowName = seriesMismatched[showName]
			if (self.verbose):
				print "Show", showName, "was MISMATCHED and is corrected to", newShowName
			showName = newShowName
		if (showName in seriesWhitelist):
			traktId = seriesWhitelist[showName]
			show = trakt.tv.TVShow(traktId)
			if (self.verbose):
				print "Show", showName, "is on WHITELIST; traktId =", traktId, "traktTVSHOW =", show
		else:
			showName = showName.replace("(", "").replace(")", "").replace(":", "")
			try:
				show = trakt.tv.search(showName, search_type="show")[0]
			except IndexError:
				print "##FAIL## Show", showName, "was not found"
				# Send an email?
				# Setup: http://askubuntu.com/questions/522431/how-to-send-an-email-using-command-line
				# Mail: https://pypi.python.org/pypi/mailtools/2
		episode = self.getTraktEpisode(show, seasonNumber, episodeNumber)
		if (self.verbose):
			print "Show: ", show, "-- Episode:", episode
		return episode
	def getTraktEpisodeInfoFlat(self, episode):
		show = trakt.tv.TVShow(episode.show)
		return (show.title, show.trakt, episode.season, episode.episode, episode.title, episode.trakt)
	def convertFlatEpisodeToTraktEpisode(self, showId, season, ep):
		return trakt.tv.TVEpisode(showId, season, ep)
	def postNewEpisodesToTrakt(self, newEpisodes):
		for episode in newEpisodes:
			episode = self.convertFlatEpisodeToTraktEpisode(episode[1], episode[2], episode[3])
			episode.scrobble(100, 1.0, 1.0).finish()
