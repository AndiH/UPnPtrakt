#!/usr/bin/env python
import argparse
import os
import json
# import urllib
import requests
from hashlib import sha1
import sqlite3 as sql
import datetime
import djmountHandler
import episodeMatcher
import trakt.tv

_TRAKTAPIKEY = "09d55b38efb03d4ee5665aa1fb417f260a76d75a"

def postNewEpisodesToTrakt(newEpisodes, traktCredentials):
	apiMethod = "%s/%s/" % ("show", "scrobble")
	apiCall = apiMethod + _TRAKTAPIKEY
	data = {'username': traktCredentials['username'], 'password': traktCredentials['password']}
	for episode in newEpisodes:
		data['title'] = episode[0]
		data['tvdb_id'] = episode[1]
		data['season'] = episode[2]
		data['episode'] = episode[3]
		data['title'] = episode[4]
		data['episode_tvdb_id'] = episode[5]
		# data['year'] = 2014
		# encodedData = json.dumps(data)
		resp = requests.post("http://api.trakt.tv/" + apiCall, data)
		parsedResp = resp.json()
		# print parsedResp
		if not (parsedResp['status'] == 'success'):
			print "Error:", parsedResp['error']
		if (parsedResp['status'] == 'success'):
			print parsedResp['message']

def updateDatabase(episodes, args):
	dbConnection = sql.connect(args.database_file)
	newEpisodes = []
	with dbConnection:
		dbCursor = dbConnection.cursor()
		dbCursor.execute("SELECT (episodetvdbid) from episodes order by id DESC limit 15")
		ids = dbCursor.fetchall()
		ids = [id[0] for id in ids]
		# print ids, episodes[-1]
		for episode in episodes:
			if not (episode[-1] in ids):
				newEpisodes.append(episode)
				if not (args.dont_store):
					dbCursor.execute("INSERT INTO episodes (date, seriesname, seriestvdbid, season, episode, episodetitle, episodetvdbid) VALUES (?,?,?,?,?,?,?)", (int(datetime.datetime.now().strftime("%s")),) + episode)
					print "Inserted", episode
		dbConnection.commit()
	return newEpisodes

def initializeTraktConnection(config):
	config['password'] = sha1(config['password']).hexdigest()
	trakt.tv.setup(apikey=_TRAKTAPIKEY, username=config['username'], password=config['password'])

def getTraktEpisodeInfo(showName, seasonNumber, episodeNumber, seriesWhitelist):
	if (showName in seriesWhitelist):
		showTvDbId = seriesWhitelist[showName]
	else: 
		showTvDbId = trakt.tv.search.shows(showName)[0]['tvdb_id']
	# print showName, showTvDbId, seasonNumber, episodeNumber
	episode = trakt.tv.show.episode(showTvDbId, seasonNumber, episodeNumber)
	return (episode['show']['title'], showTvDbId, seasonNumber, episodeNumber, episode['episode']['title'], episode['episode']['tvdb_id'])

def jsonParser(file):
	data_file = open(file)
	data = json.load(data_file)
	data_file.close()
	return data

def getLastViewedContent(path):
	content = os.listdir(path)
	if '.metadata' in content: content.remove('.metadata')
	return content

def getEpisodesFromFiles(files):
	episodeList = []
	for entry in files:
		episodeInfo = episodeMatcher.getEpisodeInfo(entry)
		if (episodeInfo != (None, None, None)):
			episodeList.append(episodeInfo)
	return episodeList

def main(args):
	if (args.restart_djmount):
		djmountHandler.cleanUp(args.mount_path)
	path = djmountHandler.mountFolder(args.mount_path)
	path = os.path.join(path, r"Serviio (Andisk2)/Video/Last Viewed")

	files = getLastViewedContent(path)
	rawEpisodes = getEpisodesFromFiles(files)
	traktCredentials = jsonParser(args.trakt_config_json)
	initializeTraktConnection(traktCredentials)
	seriesWhitelist = jsonParser(args.series_whitelist_json)
	episodes = [getTraktEpisodeInfo(episode[0], episode[1], episode[2], seriesWhitelist=seriesWhitelist) for episode in rawEpisodes]
	newEpisodes = updateDatabase(episodes, args)
	if (args.dont_post):
		if (newEpisodes == []):
			print "No new shows since last check."
		else:
			print "New shows since last check"
			for episode in newEpisodes:
				print episode
	else: # not (args.dont_post)
		postNewEpisodesToTrakt(newEpisodes, traktCredentials)

if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='Monitors a UPnP Last Viewed folder for changes, writes into a database and posts to trakt.tv.', formatter_class=argparse.ArgumentDefaultsHelpFormatter)
	parser.add_argument('--dont-store', action='store_true', help="Don't store to database but print out potential database changes instead.")
	parser.add_argument('--dont-post', action='store_true', help="Don't post to trakt.tv but print out possible database changes instead.")
	parser.add_argument('--restart-djmount', action='store_true', help="Unmount and delete the UPnP FUSE folder and kill all djmount processes before reinitialize them again.")
	parser.add_argument('--mount-path', type=str, default=".upnpDevices", help="Folder where the UPnP FUSE content will be mounted in via djmount.")
	parser.add_argument('--path-to-last-viewed', type=str, default=r"Serviio (Andisk2)/Video/Last Viewed", help="Path to monitored Last Viewed folder, beginning from djmount's mount point.")
	parser.add_argument('--database-file', type=str, default="episodes.db", help="Database file name.")
	parser.add_argument('--trakt-config-json', type=str, default="trakt-config.json", help="Trakt.tv login and API credentials JSON file.")
	parser.add_argument('--series-whitelist-json', type=str, default="seriesWhitelist.json", help="File with list of TVDB IDs of shows which just won't parse properly through trakt.tv's search.")
	# add parser argument to pass custom regex string for episode matching
	# add ability to parse all parameters from json file
	args = parser.parse_args()
	# print args
	main(args)
