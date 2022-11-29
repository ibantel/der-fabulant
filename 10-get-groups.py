"""
    This file compiles a lists of groups that were manually added to the account
    These groups are then stored as dictionary of the following structure:
        id [int]:     {
                            'username': [str],
                            'title': [str],
                            'participants': [int}
                      }
        'id' is the channel ID; 'username' the string username of the channel, 'title' the channel title with symbols etc., and 'participants' the number of subscribers

    The dictionary is saved as text file in data/groups

    N.B.: 00-setup_telegram.py (which sets up Telegram access) must be executed first
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


# %% Get available groupchats

channels_list = []  # empty list with dialogue slices to populate with channels that I am part of

# retrieve all dialogues (private and public chats(?))
dialogs_slice = client(GetDialogsRequest(
    offset_date=None, # set offset_date=None to get ALL entries
    offset_id=0,
    offset_peer=InputPeerEmpty(),
    limit=30000,
    hash=0))

channels_list.extend(dialogs_slice.chats)  # populate list with telethon.tl.types.Channel objects (called "chats")

try:  # check that dialogs_slice_list contains telethon.tl.types.Channel objects
    assert isinstance(channels_list[0], telethon.tl.types.Channel)
except AssertionError:
    print(f"ERROR: first element of 'dialogs_slice_list' is not <class 'telethon.tl.types.Channel'>.\n"
          f"\t   Instead, it is {type(channels_list[0])}")

channels_filtered = {}  # chats to keep

for channel in channels_list:
    try:
        print(f"\nChannel:\t{channel.title}\n\t\t\tid: {channel.id}\n\t\t\tusername: {channel.username}\n\t\t\tparticipants: {channel.participants_count})")
        ch_dict_tmp = {"username": channel.username, "title": channel.title, "participants": channel.participants_count}

        # append channels where the number of participants is >0
        if ch_dict_tmp["participants"] is not None:
            channels_filtered[channel.id] = ch_dict_tmp

    except AttributeError:
        pass

with open("./data/groups/" + datetime.datetime.now().strftime("%Y-%m-%d") + "-groups.txt", "w") as file:
    file.write(json.dumps(channels_filtered))

