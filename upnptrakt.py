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
from trakt import init, core, tv
import trakt
import traktHandler

def updateDatabase(episodes, args):
	dbConnection = sql.connect(args.database_file)
	newEpisodes = []
	with dbConnection:
		dbCursor = dbConnection.cursor()
		dbCursor.execute("SELECT (episodeid) from episodes order by id DESC limit 40")
		ids = dbCursor.fetchall()
		ids = [id[0] for id in ids]
		# print ids, episodes[1][-1]
		for episode in episodes:
			if not (episode[-1] in ids):
				newEpisodes.append(episode)
				if not (args.dont_store):
					dbCursor.execute("INSERT INTO episodes (date, seriesname, seriesid, season, episode, episodetitle, episodeid) VALUES (?,?,?,?,?,?,?)", (int(datetime.datetime.now().strftime("%s")),) + episode)
					print "Inserted", episode
		dbConnection.commit()
	return newEpisodes

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
	if (args.verbose):
		print "Raw Episodes: ", rawEpisodes
	# traktCredentials = jsonParser(args.trakt_config_json)
	# initializeTraktConnection(traktCredentials)
	seriesWhitelist = jsonParser(args.series_whitelist_json)
	seriesMismatched = jsonParser(args.series_mismatched_json)
	episodes = [traktHandler.getTraktEpisodeInfo(episode[0], episode[1], episode[2], seriesWhitelist=seriesWhitelist, seriesMismatched=seriesMismatched) for episode in rawEpisodes]
	if (args.verbose):
		print "Processed Episodes: ", episodes
	episodes = [traktHandler.getTraktEpisodeInfoFlat(e) for e in episodes]
	if (args.verbose):
		print "Processed, Strippd Episodes: ", episodes
	episodes = [traktHandler.getTraktEpisodeInfoFlat(e) for e in episodes]
	newEpisodes = updateDatabase(episodes, args)
	if (args.verbose):
		print "New Episodes: ", newEpisodes
	if (args.dont_post):
		if (newEpisodes == []):
			print "No new shows since last check."
		else:
			print "New shows since last check"
			for episode in newEpisodes:
				print episode
	else: # not (args.dont_post)
		traktHandler.postNewEpisodesToTrakt(newEpisodes)

if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='Monitors a UPnP Last Viewed folder for changes, writes into a database and posts to trakt.tv.', formatter_class=argparse.ArgumentDefaultsHelpFormatter)
	parser.add_argument('--verbose', action='store_true', help="Print verbose information.")
	parser.add_argument('--dont-store', action='store_true', help="Don't store to database but print out potential database changes instead.")
	parser.add_argument('--dont-post', action='store_true', help="Don't post to trakt.tv but print out possible database changes instead.")
	parser.add_argument('--restart-djmount', action='store_true', help="Unmount and delete the UPnP FUSE folder and kill all djmount processes before reinitialize them again.")
	parser.add_argument('--mount-path', type=str, default=".upnpDevices", help="Folder where the UPnP FUSE content will be mounted in via djmount.")
	parser.add_argument('--path-to-last-viewed', type=str, default=r"Serviio (Andisk2)/Video/Last Viewed", help="Path to monitored Last Viewed folder, beginning from djmount's mount point.")
	parser.add_argument('--database-file', type=str, default="episodes.db", help="Database file name.")
	parser.add_argument('--trakt-config-json', type=str, default="trakt-config.json", help="Trakt.tv login and API credentials JSON file.")
	parser.add_argument('--series-whitelist-json', type=str, default="seriesWhitelist.json", help="File with list of TVDB IDs of shows which just won't parse properly through trakt.tv's search.")
	parser.add_argument('--series-mismatched-json', type=str, default="seriesMismatched.json", help="Sometimes, your UPnP server displays the wrong show name. This file provides the proper names for mismatched ones.")
	# add parser argument to pass custom regex string for episode matching
	# add ability to parse all parameters from json file
	args = parser.parse_args()
	# print args
	main(args)
