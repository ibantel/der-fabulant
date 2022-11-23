"""
    This file sets up Telegram access
"""

# %% Credentials

dict_credentials: dict = dict()

with open("api_access_ibantel.txt", "r") as f_credentials:
    # the file should contain 4 lines according to the following patterns:
    #  name = "Nutzer"
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

dict_credentials