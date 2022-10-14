import streamlit as st
from deta import Deta
from connection_bdd import connection_cal_bdd, connection_players_stat
import pandas as pd
import numpy as np

st.set_page_config(
    page_title="Calcul Master",
    page_icon="🤖",
    layout="wide",
)

def get_sec(time_str):
    """Get seconds from time."""
    m, s, c = time_str.split(':')
    return int(m) * 60 + int(s) + (int(c)/10)

st.title('📊My Statistics')

option = st.selectbox(
    'Which level you need to see the statistics ?',
    ('All', '1', '2', '3', 'Survival'))

# --------------------------------------------------------------------------
# --------------------------------------------------------------------------

st.session_state['stat_lvl'] = option

# connexion à la base de données
db = connection_cal_bdd()

if (option == "All"):
    data_temp = db.fetch({"user": st.experimental_user.email}).items
elif(option == "Survival"):
    data_temp = db.fetch({"user": st.experimental_user.email, "niveau": 4}).items
else:
    data_temp = db.fetch({"user": st.experimental_user.email, "niveau": int(option)}).items

data = sorted(data_temp, key=lambda d: int(d['index']))  # On tri les données par la clé (la clé étant du string dans la bdd, le '10' se situe avant le '2')

mean_ratio = 0
mean_time = 0
bon_rep = 0
mauv_rep = 0
niv_max = 0
niv_min = 100
ratio = []
temps = []
nb_item = 0  # Permet de savoir si le joueur a déjà fait des parties

if(option == "Survival"):
    for i in data:
        nb_item += 1

        mean_ratio += i['ratio']
        mean_time += get_sec(i['temps'])
        if(int(i['bonne_rep']) > niv_max):
            niv_max = int(i['bonne_rep'])

        if (int(i['bonne_rep']) < niv_min):
            niv_min = int(i['bonne_rep'])

        ratio.append(i['ratio'])
        temps.append(get_sec(i['temps'])/60)
else:
    for i in data:
        nb_item += 1

        mean_ratio += i['ratio']
        mean_time += get_sec(i['temps'])
        bon_rep += i['bonne_rep']
        mauv_rep += i['mauvaise_rep']

        ratio.append(i['ratio'])
        temps.append(get_sec(i['temps']))

if(nb_item != 0):
    mean_time = mean_time / nb_item
    seconds = mean_time % 60
    minutes = mean_time // 60
    centieme = str(seconds)
    centieme = int(centieme.split(".")[1][:2])

    mean_time = "%02d:%02d:%02d" % (minutes, seconds, centieme)

if (nb_item == 0):
    st.write("No data for the moment, start to play to see your statistics.")
else:
    if(option == "Survival"):
        chart = pd.DataFrame(list(zip(ratio, temps)), columns=['Ratio', 'Time (in minutes)'])

        col1, col2, col3, col4, col5 = st.columns(5)
        col1.metric("Games played", nb_item)
        col2.metric("Average ratio", f'{round(mean_ratio / nb_item, 2)} %')
        col3.metric("Best score", niv_max)
        col4.metric("Worst score", niv_min)
        col5.metric("Average time", mean_time)

        st.subheader("Evolution of your score")
        st.line_chart(chart)
    else:
        chart = pd.DataFrame(list(zip(ratio, temps)), columns=['Ratio', 'Time (in seconds)'])

        col1, col2, col3, col4, col5 = st.columns(5)
        col1.metric("Games played", nb_item)
        col2.metric("Average ratio", f'{round(mean_ratio / nb_item, 2)} %')
        col3.metric("Good answers", bon_rep)
        col4.metric("Bad answers", mauv_rep)
        col5.metric("Average time", mean_time)

        st.subheader("Evolution of your ratio")
        st.line_chart(chart)
