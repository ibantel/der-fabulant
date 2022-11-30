"""
    This file takes in a lists of groups from 10-get-groups.py



    N.B.:   00-setup_telegram.py (which sets up Telegram access) and
            10-get-groups.py (which compiles the groups)
            must be executed first
"""


import csv
import datetime
import json
import os
import matplotlib.pyplot as plt
import pandas as pd
import pytz
import telethon
from telethon.sync import TelegramClient
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerEmpty

# %% load groups

f: str = [file for file in os.listdir("./data/groups")][-1]

with open("./data/groups/" + f, "r") as file:
    data = file.read()

groups: dict = json.loads(data)


# %% Scrape messages from group(s)

messages = []

for channel_id in [k for k in groups.keys()][:]:
    with TelegramClient(dict_credentials["name"], api_id=dict_credentials["api_id"], api_hash=dict_credentials["api_hash"]) as client:
        client.connect()
        for message in client.iter_messages(groups[channel_id]['username'],
                                            offset_date=datetime.date(2020, 1, 1),
                                            reverse=True):  # reverse=starting from offset_date

            try:
                mess_raw = message.to_json()
                mess_dict = json.loads(mess_raw)
                if mess_dict["_"] == "Message":
                    del mess_dict["_"]
                    messages.append(mess_dict)


            except:
                pass

client.disconnect()


df_messages: pd.DataFrame = pd.json_normalize(messages)

#%% Map peer_id.channel_id to username

channels_id_to_username: dict = {}
for k in channels_filtered.keys():
    channels_id_to_username[k] = channels_filtered[k]['username']

try:
    df_messages.insert(df_messages.columns.get_loc("peer_id.channel_id"),  # insert after peer_id.ch...
                       'peer_id.channel_username',  # name
                       df_messages['peer_id.channel_id'].map(channels_id_to_username))  # content
except KeyError:
    print("Error: 'peer_id.channel_id' not in df_messages.columns.")
    print("Skipping assignment")

df_messages.to_csv("./data/messages/" + datetime.datetime.now().strftime("%Y-%m-%d--%H%M") + "-messages.csv")
