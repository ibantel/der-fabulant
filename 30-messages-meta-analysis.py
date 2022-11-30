"""
    This file takes in a dataframe produced by 20-get-messages.py

    N.B.:   00-setup_telegram.py (which sets up Telegram access) and
            10-get-groups.py (which compiles the groups)
            20-get-messages.py (which collects messages from groups specified in 10-get-groups.py)
            must be executed first
"""


import csv
import datetime
import json
import matplotlib.pyplot as plt
import numpy as np
import os
import pandas as pd
import plotly.express as px
import re
import seaborn as sns

# %% import data
f: str = [file for file in os.listdir("./data/messages")][-1]  # get newest file

df_messages: pd.DataFrame = pd.read_csv("./data/messages/" + f, index_col=0)

# %% clean data

df_messages.dropna(axis=1, how='all', inplace=True)  # drop columns with all NAs

df_messages['date'] = pd.to_datetime(df_messages['date']).dt.round('1h')  # clean date, round to hours


### TO DO:
#    parse df_messages['reactions.thumbs_up']

df_messages.info()

# %% inspect columns of interest [revisit later]
if False:
    df_messages['from_id'].value_counts()  # 'from_id', 'fwd_from.from_id', 'fwd_from.from_id._', 'fwd_from.from_id.channel_id', 'fwd_from.from_id.user_id',
    df_messages['fwd_from'].value_counts()  # 'fwd_from', 'fwd_from._', 'fwd_from.channel_post', 'fwd_from.date', 'fwd_from.from_name', 'fwd_from.imported', 'fwd_from.post_author', 'fwd_from.psa_type', 'fwd_from.saved_from_msg_id', 'fwd_from.saved_from_peer',
    df_messages['forwards'].value_counts()  # 'noforwards',
    df_messages['forward'].value_counts()
    df_messages['media._'].value_counts()  # 'media._', 'media.nopremium',
    df_messages['media.poll._'].value_counts()  # 'media.poll.answers', 'media.poll.close_date', 'media.poll.close_period', 'media.poll.closed', 'media.poll.id', 'media.poll.multiple_choice', 'media.poll.public_voters', 'media.poll.question', 'media.poll.quiz',
    df_messages['media.results._'].value_counts()  # 'media.results.min', 'media.results.recent_voters', 'media.results.results', 'media.results.solution', 'media.results.solution_entities', 'media.results.total_voters', 'media.ttl_seconds', 'media_unread',
    df_messages['media.document._'].value_counts()  # 'media.document.access_hash', 'media.document.attributes', 'media.document.date', 'media.document.dc_id', 'media.document.file_reference', 'media.document.id', 'media.document.mime_type', 'media.document.size', 'media.document.thumbs', 'media.document.video_thumbs',
    df_messages['media.geo._'].value_counts()  # 'media.geo.access_hash', 'media.geo.accuracy_radius', 'media.geo.lat', 'media.geo.long',
    df_messages['media.photo._'].value_counts()  # 'media.photo.access_hash', 'media.photo.date', 'media.photo.dc_id', 'media.photo.file_reference', 'media.photo.has_stickers', 'media.photo.id', 'media.photo.sizes', 'media.photo.video_sizes',
    df_messages['media.webpage._'].value_counts()  # 'media.webpage.attributes', 'media.webpage.author', 'media.webpage.cached_page', 'media.webpage.cached_page._', 'media.webpage.cached_page.blocks', 'media.webpage.cached_page.documents', 'media.webpage.cached_page.part', 'media.webpage.cached_page.photos', 'media.webpage.cached_page.rtl', 'media.webpage.cached_page.url', 'media.webpage.cached_page.v2', 'media.webpage.cached_page.views', 'media.webpage.description', 'media.webpage.display_url', 'media.webpage.document', 'media.webpage.document._', 'media.webpage.document.access_hash', 'media.webpage.document.attributes', 'media.webpage.document.date', 'media.webpage.document.dc_id', 'media.webpage.document.file_reference', 'media.webpage.document.id', 'media.webpage.document.mime_type', 'media.webpage.document.size', 'media.webpage.document.thumbs', 'media.webpage.document.video_thumbs', 'media.webpage.duration', 'media.webpage.embed_height', 'media.webpage.embed_type', 'media.webpage.embed_url', 'media.webpage.embed_width', 'media.webpage.hash', 'media.webpage.id', 'media.webpage.photo', 'media.webpage.photo._', 'media.webpage.photo.access_hash', 'media.webpage.photo.date', 'media.webpage.photo.dc_id', 'media.webpage.photo.file_reference', 'media.webpage.photo.has_stickers', 'media.webpage.photo.id', 'media.webpage.photo.sizes', 'media.webpage.photo.video_sizes', 'media.webpage.site_name', 'media.webpage.title', 'media.webpage.type', 'media.webpage.url',
    df_messages['media.webpage.url'].value_counts()
    # df_messages['video'].value_counts()  #
    # df_messages['video_note'].value_counts()  #
    # df_messages['voice'].value_counts()  #
    # df_messages['audio'].value_counts()  #
    df_messages['file'].value_counts()  # ?
    df_messages['views'].value_counts()  # ok
    df_messages['post_author'].value_counts()  #
    df_messages['reactions'].value_counts()  # 'reactions._', 'reactions.can_see_list', 'reactions.min', 'reactions.recent_reactions', 'reactions.results',
    df_messages['button_count'].value_counts()
    df_messages['buttons'].value_counts()
    df_messages['contact'].value_counts()
    df_messages['is_reply'].value_counts()
    df_messages['raw_text'].value_counts()
    df_messages['message'].value_counts()
    df_messages['sticker'].value_counts()
    df_messages['text'].value_counts()

#%% keep & rename columns of interest

df_mes_analysis = df_messages[[
    'date', 'peer_id.channel_username', 'peer_id.channel_id',
    # 'fwd_from.post_author', 'fwd_from.from_id.user_id',
    'fwd_from.from_id.channel_id', 'fwd_from.from_name',
    'forwards',
    'media._', 'media.webpage.url',
    'views',
    #'post_author',  # too many NAs
    'message']]

df_mes_analysis.info()

df_mes_analysis = df_mes_analysis.rename(
    columns = {"peer_id.channel_username":     "channel.name",
               "peer_id.channel_id":           "channel.id",
               "fwd_from.from_id.channel_id":  "fwded.from_channel",
               "fwd_from.from_name":           "fwded.from_user",
               "forwards":                     "fwded.number",
               "media._":                      "media.type",
               "media.webpage.url":            "webpage_url",
               "message":                      "message.text"})

#%% preliminary analysis

df_mes_analysis['message.type'] = df_mes_analysis['media.type'].fillna("MessageMessageOnly")  # create message type column
df_mes_analysis['message.type'] = df_mes_analysis['message.type'].str.replace("Message", "", n=1).str.replace("Media", "", n=1)
del df_mes_analysis['media.type']

df_mes_analysis['message.n_words'] = df_mes_analysis['message.text'].str.split().str.len()

# look up words
df_mes_analysis['message.cov']   = df_mes_analysis['message.text'].str.contains('corona|covid', na=False, flags=re.IGNORECASE).astype(int)
df_mes_analysis['message.vac']   = df_mes_analysis['message.text'].str.contains('impf(ung|en)|moderna|astra|biontech|johnson', na=False, flags=re.IGNORECASE).astype(int)
df_mes_analysis['message.gates'] = df_mes_analysis['message.text'].str.contains('gates', na=False, flags=re.IGNORECASE).astype(int)
df_mes_analysis['message.lockd'] = df_mes_analysis['message.text'].str.contains('(shut|lock)down', na=False, flags=re.IGNORECASE).astype(int)
df_mes_analysis['message.counter'] = 1

#%% Plotting

df_mes_analysis['message.topic'] = np.where(df_mes_analysis['message.cov'] > 0, 'covid',
                                            np.where(df_mes_analysis['message.vac'] > 0, 'impfung',
                                                     np.where(df_mes_analysis['message.gates'] > 0, 'gates',
                                                              np.where(df_mes_analysis['message.cov'] > 0, 'lockdown',
                                                                       np.nan))))


if True:  # over time plot
    df_mes_plot_time: pd.DataFrame = \
        df_mes_analysis[['date',
                         'message.cov', 'message.vac', 'message.gates', 'message.lockd',
                         'message.counter']].groupby("date").agg(
            {'message.cov': sum, 'message.vac': sum, 'message.gates': sum,
             'message.lockd': sum, 'message.counter': sum}).reset_index()

    plt.rcParams["figure.figsize"] = [10, 3]
    plt.rcParams["figure.autolayout"] = True
    ax = sns.lineplot (x = "date", y = "message.counter", data = df_mes_plot_time, linewidth=1)
    ax.tick_params (rotation = 60)
    ax.set_title("Number of messages over time")
    plt.savefig('./plots/1-dateplot.pdf', dpi=300)
    plt.show()



    # pd.wide_to_long(df_mes_plot_time.rename(columns={'message.counter':'counter'}), stubnames='message', i='date', j='topic')

if True:  # keyword plot

    df_mes_plot_time_topic: pd.DataFrame = \
        df_mes_analysis[['date',
                         'message.topic',
                         'message.counter']].groupby(["date", 'message.topic']).agg(
            {'message.counter': sum}).reset_index()

    df_mes_plot_time_topic = df_mes_plot_time_topic.loc[df_mes_plot_time_topic['message.topic'] != "nan", :]

    plt.rcParams["figure.figsize"] = [10, 3]
    plt.rcParams["figure.autolayout"] = True
    ax = sns.lineplot(x="date", y="message.counter", hue='message.topic', data=df_mes_plot_time_topic, linewidth=1)
    ax.tick_params(rotation=60)
    ax.set_title("Number of messages over time, by topic")
    plt.savefig('./plots/10-dateplot_topic.pdf', dpi=300)
    plt.show()


if True:  # channel over time plot
    df_mes_plot_time_channel: pd.DataFrame = \
        df_mes_analysis[['date', "channel.name",
                         'message.cov', 'message.vac', 'message.gates', 'message.lockd',
                         'message.counter']].groupby(["date", "channel.name"]).agg(
            {'message.cov': sum, 'message.vac': sum, 'message.gates': sum,
             'message.lockd': sum, 'message.counter': sum}).reset_index()

    plt.rcParams["figure.figsize"] = [10, 3]
    plt.rcParams["figure.autolayout"] = True
    ax = sns.lineplot (x = "date", y = "message.counter", hue="channel.name", data = df_mes_plot_time_channel, linewidth=.5)
    sns.move_legend(ax, "upper left", bbox_to_anchor=(1, 1))
    ax.tick_params (rotation = 60)
    ax.set_title("Number of messages over time, by channel")
    plt.savefig('./plots/2-dateplot_channels.pdf', dpi=300)
    plt.show()

if True:  # message types over time
    df_mes_plot_time_media: pd.DataFrame = \
        df_mes_analysis[['date', 'message.type',
                         'message.cov', 'message.vac', 'message.gates', 'message.lockd',
                         'message.counter']].groupby(["date", 'message.type']).agg(
            {'message.cov': sum, 'message.vac': sum, 'message.gates': sum,
             'message.lockd': sum, 'message.counter': sum}).reset_index()

    plt.rcParams["figure.figsize"] = [10, 3]
    plt.rcParams["figure.autolayout"] = True
    ax = sns.lineplot(x="date", y="message.counter", hue="message.type", data=df_mes_plot_time_media, linewidth=.5)
    sns.move_legend(ax, "right", bbox_to_anchor=(1, 1))
    ax.tick_params(rotation=60)
    ax.set_title("Number of messages over time, by message type")
    plt.savefig('./plots/3-dateplot_message-type.pdf', dpi=300)
    plt.show()

if True:  #
    df_mes_plot_views_messtype: pd.DataFrame = \
        df_mes_analysis[['message.type', 'views']].groupby(['message.type']).agg({'views': sum}).reset_index()

    plt.rcParams["figure.figsize"] = [10, 10]
    plt.rcParams["figure.autolayout"] = True
    ax = sns.barplot(x="message.type", y="views", data=df_mes_plot_views_messtype)
    ax.tick_params(rotation=60)
    ax.set_title("Number of views, by message type")
    plt.savefig('./plots/4-views_message-type.pdf', dpi=300)
    plt.show()

