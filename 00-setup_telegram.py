"""
    This file sets up Telegram access
"""

# %% Imports

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

local_timezone=pytz.timezone("Europe/Berlin")

# %% Credentials

dict_credentials: dict = dict()

with open("api_access_ibantel.txt", "r") as f_credentials:
    # the file should contain 4 lines according to the following patterns:
    #  name = "anon"
    #  api_id = [API ID, integer]
    #  api_hash = [API hash, alphanumeric string]
    #  phone = [phone number used for registration; pattern: string, starting with "+", followed by country code, e.g. "+4916900000000"]
    for line in f_credentials:
        k, v = line.split(" = ")
        if k == 'api_id':
            try: v = int(v.strip().strip("'").strip('"'))
            except: v = v.strip().strip("'").strip('"')
        else:
            v = v.strip().strip("'").strip('"')

        dict_credentials[k] = v

del line, k, v, f_credentials


# %% Connect client

client = TelegramClient("Nutzer", dict_credentials["api_id"], dict_credentials["api_hash"])  # instantiate client
client.connect()

try:
    assert client.is_user_authorized()
except AssertionError:
    print("Client not connected. Connecting now.")
    client.send_code_request(dict_credentials["phone"])
    client.sign_in(dict_credentials["phone"], input('Enter the code sent to Telegram app: '))

