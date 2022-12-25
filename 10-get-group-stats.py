"""
    This file retrieves group summary statistics for a lists of groups (usernames)
    The results are then stored in a dataframe with the following structure:


    N.B.: 00-setup_telegram.py (which sets up Telegram access) must be executed first
"""

# %% Imports
import numpy as np
import pandas as pd
import pytz
import telethon
from telethon.sync import TelegramClient
from telethon import client
from telethon.tl.functions.channels import GetFullChannelRequest
import time

from helpers.aa_credentials_telegram import gather_credentials  # import helper function to gather credentials

local_timezone=pytz.timezone("Europe/Berlin")

# %% Connect client (connection via 00-setup_telegram.py)

dict_credentials = gather_credentials(path="./", filename="api_access_ibantel.txt")

tg_client = TelegramClient("Nutzer", dict_credentials["api_id"], dict_credentials["api_hash"])  # instantiate tg_client with values from 00-setup_telegram.py
tg_client.connect()

try:
    assert tg_client.is_user_authorized()
except AssertionError:
    print("Client not connected. Connecting now.")
    tg_client.send_code_request(dict_credentials["phone"])
    tg_client.sign_in(dict_credentials["phone"], input('Enter the code sent to Telegram app: '))

# %% load names of groups to query

groups = []
with open("./data/groups/groups-usernames.txt", "r") as f:
    for line in f.readlines():
        if not line.startswith("#"):
            groups.append(line.strip())

# %% go through the groups and write

groups_summary: dict = {}  # empty dictionary to populate with summary statistics of the groups

for group in groups:
    try:
        channel_connect = tg_client.get_entity(group)
    except ValueError:
        print(f"Error with {group} in tg_client.get_entity({group})")

    try:
        channel_full_info = tg_client(GetFullChannelRequest(channel=channel_connect))  # channel_full_info is a  <telethon.tl.types.messages.ChatFull> object (https://tl.telethon.dev/types/messages/chat_full.html)
        # looks like no additional, interesting attributes from this object
        groups_summary[group] = {'participants': channel_full_info.full_chat.participants_count}
    except ValueError:
        print(f"Error with {group} in ttg_client(GetFullChannelRequest(...))")
        groups_summary[group] = {'participants': np.nan}

    # to avoid getting a
    # telethon.errors.rpcerrorlist.FloodWaitError: A wait of 82590 seconds is required (caused by ResolveUsernameRequest)
    # wait a random number of ca. 10 seconds before performing the next request
    wait_time = np.random.normal(loc=10, scale=1.0, size=None)
    time.sleep(wait_time)