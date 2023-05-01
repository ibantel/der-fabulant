# creating data set for coding task

import pandas as pd

tg_messages = pd.read_csv("./data/messages/2022-11-30--1023-messages.csv")
tg_messages['date'] = pd.to_datetime(tg_messages['date']).dt.date
tg_messages.info()
[col for col in tg_messages.columns
 if not col.startswith("media")
 and not col.startswith("repl")
 and not col.startswith("fwd_")
 and not col.startswith("peer")
 and not col.startswith("react")
 and not col. startswith("edit")
 and not col in ["ttl_period", "from_id", "via_bot_id", "Unnamed: 0", "pinned", "mentioned", "entities",
                 "from_scheduled", "restriction_reason", "views", "noforwards", "grouped_id", "post", "out", "silent", "legacy"]]


# encode names of channels separately
channels = tg_messages[['peer_id.channel_username', 'peer_id.channel_id']].drop_duplicates()
ids =  channels.iloc[:, 0].to_list()
names =  channels.iloc[:, 1].to_list()

dict_names_ids = dict(zip(ids, names))

import json
with open('./data/messages/coding-task_mapping.json', 'w') as f:
    json.dump(dict_names_ids, f)

# data
tg_export_messages = tg_messages[['date', 'peer_id.channel_id', 'message', 'views', "forwards", "post_author"]].rename(
    columns={'peer_id.channel_username': 'channel_name', 'peer_id.channel_id': 'channel_id'})

tg_export_messages.loc[tg_export_messages['date'] == "2020-01-01", 'date']


tg_export_messages.to_csv("./data/messages/coding-task_main.csv", index=False)

df = pd.read_csv("./data/messages/coding-task_main.csv").drop(columns="message")

pd.to_datetime(df['date'])

# training data
df_3 = pd.read_excel("./data/messages/2022-11-30--1023-messages_annotated_001.xlsx")
df_3.columns
tg_examples = df_3.loc[df_3['conspiracy_narrative_sgl_de'].notna(), ['message', 'conspiracy_narrative_sgl_de', 'conspiracy_narrative_sgl_en']].rename(
    columns={'conspiracy_narrative_sgl_de': 'conspiracy_narrative_GER', 'conspiracy_narrative_sgl_en': 'conspiracy_narrative_ENG'})
tg_examples.to_csv("./data/messages/coding-task_examples.csv", index=False)
