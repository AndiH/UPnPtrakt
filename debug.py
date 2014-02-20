import trakt.tv
import json
import argparse

parser = argparse.ArgumentParser(description='Test file to debug strings failing with the trakt API', formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument('showname', type=str, help='Show name string to be tested')
args = parser.parse_args()

credFile = open("trakt-config.json")
creds = json.load(credFile)
trakt.tv.setup(apikey=creds['apikey'], username=creds['username'], password=creds['password'])
show = args.showname

show = trakt.tv.search.shows(show.replace("(", "").replace(")", "").replace(":", ""))
print show[0]
