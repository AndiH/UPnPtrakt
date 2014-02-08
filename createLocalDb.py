#!/usr/bin/env python
import sqlite3 as sql
import argparse

parser = argparse.ArgumentParser(description='Initializes the local database for TV show episodes.')
parser.add_argument('--dropDB', action='store_true', help='drop the database if it already exists')
args = parser.parse_args()

dbConnection = sql.connect('episodes.db')
with dbConnection:
	dbCursor = dbConnection.cursor()
	if args.dropDB:
		dbCursor.execute("DROP TABLE IF EXISTS episodes")
	dbCursor.execute("CREATE TABLE episodes (id INTEGER PRIMARY KEY AUTOINCREMENT, date INT, seriesname TEXT, seriestvdbid INT, season INT, episode INT, episodetitle TEXT, episodetvdbid INT)")

