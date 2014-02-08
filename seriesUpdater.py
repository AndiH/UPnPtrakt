import sqlite3 as sql
import datetime
import folderParser
import traktHandler
import djmountHandler

path = djmountHandler.mountFolder()
path = path + '/' + r"Serviio (Andisk2)/Video/Last Viewed"
dbFile = "episodes.db"

files = folderParser.folderParser(path)
print files
episodes = [traktHandler.getEpisodeInfo(episode[0], episode[1], episode[2]) for episode in files]

# print episodes

dbConnection = sql.connect(dbFile)
with dbConnection:
	dbCursor = dbConnection.cursor()
	dbCursor.execute("SELECT (episodetvdbid) from episodes order by id DESC limit 10")
	ids = dbCursor.fetchall()
	ids = [id[0] for id in ids]
	# print ids, episodes[-1]
	for episode in episodes:
		if not (episode[-1] in ids):
			dbCursor.execute("INSERT INTO episodes (date, seriesname, seriestvdbid, season, episode, episodetitle, episodetvdbid) VALUES (?,?,?,?,?,?,?)", (int(datetime.datetime.now().strftime("%s")),) + episode)
			print "Inserted", episode
	dbConnection.commit()
