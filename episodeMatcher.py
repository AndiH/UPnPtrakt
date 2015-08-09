import guessit
import re

def getEpisodeInfo(rawString, reString='(.+)\((\d{1,2})\_(\d{1,2})\):'):
	name = season = episode = None 
	p = re.compile(reString)
	matched = p.search(rawString)
	if (matched):
		name = str(matched.group(1).rstrip())
		season = int(matched.group(2))
		episode = int(matched.group(3))
	else:
		if (not ('mkv' in rawString)):
			rawString = rawString + str('.mkv')
		guessed = guessit.guess_video_info(rawString)
		if (guessed['type'] == 'episode' and guessed.has_key('season')):
			name = str(guessed['series'])
			season = int(guessed['season'])
			episode = int(guessed['episodeNumber'])
	return (name, season, episode)
