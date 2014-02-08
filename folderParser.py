import os
import episodeMatcher as matcher

# path = "/Users/Andi/dlna/Serviio (Andisk2)/Video/Last Viewed"
path = "fakeDataFolder"

def folderParser(path):
	content = os.listdir(path)
	# print content
	if '.metadata' in content: content.remove('.metadata')
# print content

	episodeList = []
	for entry in content:
		episodeInfo = matcher.getEpisodeInfo(entry)
		if (episodeInfo != (None, None, None)):
			episodeList.append(episodeInfo)
	return episodeList

if __name__ == '__main__':
	print folderParser(path)
