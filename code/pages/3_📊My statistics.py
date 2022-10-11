import streamlit as st
from deta import Deta


st.set_page_config(
    page_title="Calcul Master",
    page_icon="🤖",
    layout="wide",
)

st.title('📊My Statistics')

option = st.selectbox(
    'Which level you need to see the statistics ?',
    ('All', '1', '2', '3', 'Survival'))

# --------------------------------------------------------------------------
# --------------------------------------------------------------------------

st.session_state['stat_lvl'] = option

# connexion à la base de données
deta_key = "a08tige2_PvhsiHXAgkfPxQe1V216HBn6Js3czaoz"
deta = Deta(deta_key)
db = deta.Base("cal_bdd")

if (option == "All"):
    data_temp = db.fetch({"user": st.experimental_user.email}).items
elif(option == "Survival"):
    data_temp = db.fetch({"user": st.experimental_user.email, "niveau": 4}).items
else:
    data_temp = db.fetch({"user": st.experimental_user.email, "niveau": int(option)}).items

data = sorted(data_temp, key=lambda d: int(d['index']))  # On tri les données par la clé (la clé étant du string dans la bdd, le '10' se situe avant le '2')

mean_ratio = 0
bon_rep = 0
mauv_rep = 0
niv_max = 0
niv_min = 100
ratio = []
nb_item = 0  # Permet de savoir si le joueur a déjà fait des parties

if(option == "Survival"):
    for i in data:
        nb_item += 1

        mean_ratio += i['ratio']
        if(int(i['bonne_rep']) > niv_max):
            niv_max = int(i['bonne_rep'])

        if (int(i['bonne_rep']) < niv_min):
            niv_min = int(i['bonne_rep'])

        ratio.append(i['ratio'])
else:
    for i in data:
        nb_item += 1

        mean_ratio += i['ratio']
        bon_rep += i['bonne_rep']
        mauv_rep += i['mauvaise_rep']

        ratio.append(i['ratio'])

if (nb_item == 0):
    st.write("No data for the moment, start to play to see your statistics.")
else:
    if(option == "Survival"):
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Games played", nb_item)
        col2.metric("Average ratio", f'{round(mean_ratio / nb_item, 2)} %')
        col3.metric("Best score", niv_max)
        col4.metric("Worst score", niv_min)

        st.subheader("Evolution of your score")
        st.line_chart(ratio)
    else:
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Games played", nb_item)
        col2.metric("Average ratio", f'{round(mean_ratio / nb_item, 2)} %')
        col3.metric("Good answers", bon_rep)
        col4.metric("Bad answers", mauv_rep)

        st.subheader("Evolution of your ratio")
        st.line_chart(ratio)