"""
    This file provides a function to read in credentials for telegram access

    If executed on its own, it also instantiates a client and connects the client to Telegram. If the client is not
        yet authorized, the file needs manual input from the telegram device to set up access.
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

def gather_credentials(path="./", filename="file.txt"):
    """
        path [str]: path to filename
        filename [str]: name of file containing the credentials
            Structure of filename must be (one line per entry; data from Telegram access):
                name = [str]        e.g.: name = "anon"
                api_id = [int]      e.g.: api_id = 1234567
                api_hash = [str]    e.g.: api_hash = '0a1b2c3d4e5f6g7h8i9j1k1l1m1n1o1p'
                phone = [str]       e.g.: phone = '+4916912345678'
        This function gathers the telegram credentials from the file at [path]/[filename]
    :return: dict of form {"name": [str], "api_id": [int], "api_hash": [str], "phone": [str]}
    """

    dict_credentials: dict = dict()

    with open(path + "/" + filename, "r") as f_credentials:
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

    return dict_credentials


#%% if __name__ == "__main__"

if __name__ == "__main__":
    dict_credentials = gather_credentials(path="../", filename="../api_access_ibantel.txt")

    # Connect client
    tg_client = TelegramClient("Nutzer", dict_credentials["api_id"], dict_credentials["api_hash"])  # instantiate client
    tg_client.connect()

    # ensure client is authorized
    try:
        assert tg_client.is_user_authorized()
    except AssertionError:
        print("Client not connected. Connecting now.")
        tg_client.send_code_request(dict_credentials["phone"])
        tg_client.sign_in(dict_credentials["phone"], input('Enter the code sent to Telegram app: '))

