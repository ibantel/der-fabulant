"""
    This file compiles a lists of groups that were manually added to a GoogleSheets (link private)
    These groups are then stored as list with the "Telegram username" of the group in the file "groups-usernames.txt"
    N.B.: 00-setup_telegram.py is not needed
"""


#%% imports
from datetime import datetime as dt
import pandas as pd
import numpy as np  # Google Sheets API must be enabled


#%% load data on groups from google sheet

gsheets: dict = {}  # dict to hold the sheets. form is {  [sheetname]: {"url": str, "sheet_id": str}  }

# get link(s) to google sheet(s) containing relevant groups
with open("info_gsheets.txt", "r") as f:
    for line in f.readlines():
        if line.startswith("#"):
            continue
        name_r, url = line.split("###")
        name = name_r.lower().strip().replace("ä", "ae").replace("ä", "ae").replace("ö", "oe").replace("ü", "ue").replace("ß", "ss")  # no umlaute)
        gsheets[name] = {'url': url.strip()}

# extract sheet ID(s) from URL(s) in dict
for sheet in gsheets.keys():
    id = gsheets[sheet]['url'].split("spreadsheets/d/")[1]  # take everything after the (first) occurrence of "spreadsheets/d/"
    id = id.split("/edit?")[0]  # take everything before the (first) "/edit?"

    gsheets[sheet]['sheet_id'] = id

del f, id, line, name, name_r, sheet, url

# read sheet(s)

tg_groups = pd.DataFrame()  # empty df to be filled
i = 0  # counter

for sheet in gsheets.keys():
    url = f'https://docs.google.com/spreadsheets/d/{gsheets[sheet]["sheet_id"]}/gviz/tq?tqx=out:csv&sheet={sheet}'
    tg_groups_tmp = pd.read_csv(url, encoding='utf-8')  # load data

    if i == 0:  # first round: overwrite df
        tg_groups = tg_groups_tmp
    else:  # all other rounds: append
        tg_groups = pd.concat([tg_groups, tg_groups_tmp])

    i+= 1

del i, tg_groups_tmp, sheet, url, gsheets

#%% extract links of telegram groups
tg_groups = tg_groups.loc[tg_groups['Plattform'].isin(['Telegram', 'telegram']), ['Link']].rename(columns={"Link": "link"})

#%% extract user names of groups
tg_groups['username'] = tg_groups['link'].apply(lambda x: x.split("t.me/")[1])  # extract anything after t.me/

#%% write new group names to file

existing_groupnames = []
# check which groupnames already exist
with open("./data/groups/groups-usernames.txt", "r") as f:
    for line in f.readlines():
        if not line.startswith("#"):
            existing_groupnames.append(line.strip())

# add new names from data frame
with open("./data/groups/groups-usernames.txt", "a") as f:
    for g_name in tg_groups['username'].tolist():
        if not g_name in existing_groupnames:
            f.write("\n" + g_name)  # append username to file

del existing_groupnames, f, line, g_name, tg_groups

# when reading from this file: skip "#" lines and empty lines ("\n", "")