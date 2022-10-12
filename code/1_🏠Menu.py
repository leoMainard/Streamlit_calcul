import streamlit as st
import time
import datetime
import random as rd
import pandas as pd
import shutil
from deta import Deta
from operator import itemgetter
from connection_bdd import connection_cal_bdd, connection_players_stat

# ------------ PAGE DE MENU

st.set_page_config(
    page_title="Calcul Master",
    page_icon="🤖",
    layout="wide",
)


user = st.experimental_user.email   #.split('@')[0]

st.title('📟 CALCUL MASTER\n')

st.header(f'Hi {user} !\n')
st.markdown('On this application, you can work your mental calculation and have a look to your progration !')
st.markdown('Acceed to the training or statistics page with the menu on the left.')

ps = connection_players_stat()

data_player = ps.fetch({"user": st.experimental_user.email}).items

nb_item = 0
for i in data_player:
    nb_item += 1

if(nb_item == 0):
    ps.put({'user': st.experimental_user.email,
            'nb_parties': 0,
            'worst_niv1': '00:00',
            'best_niv1': '59:59',
            'worst_niv2': '00:00',
            'best_niv2': '59:59',
            'worst_niv3': '00:00',
            'best_niv3': '59:59',
            'best_survival': 0,
            'worst_survival': 100,
            'score': 0
            })

# ------------ PAGE DE BASE DE DONNEES
def base():
    # On se connecte à la bdd de jeu

    db = connection_cal_bdd()

    joueur = ['dam.ravaud@gmail.com','timotheequeffelec79@gmail.com','test@localhost.com','pa-trarieux@smacl.fr','leomainard63@gmail.com','a-menage@smacl.fr']

    for jou in joueur:
        data_temp = db.fetch({"user": jou}).items

        nb_parties = len(data_temp)
        best_niv1, best_niv2, best_niv3  = time.strptime("59:59", "%M:%S"), time.strptime("59:59", "%M:%S"), time.strptime("59:59", "%M:%S")
        worst_niv1, worst_niv2, worst_niv3 = time.strptime("00:00", "%M:%S"), time.strptime("00:00", "%M:%S"), time.strptime("00:00", "%M:%S")
        best_survival, worst_survival = 0, 100
        score = 0

        for i in data_temp:
            temps = time.strptime(i['temps'], "%M:%S")
            if(i['niveau'] == 1): # 6 = ['niveau']
                if(i['ratio'] == 100):
                    score += 5
                else:
                    score-= i['mauvaise_rep']

                if(temps >= worst_niv1):
                    worst_niv1 = temps
                if (temps <= best_niv1):
                    best_niv1 = temps
            elif(i['niveau'] == 2):
                if (i['ratio'] == 100):
                    score += 5
                else:
                    score-= i['mauvaise_rep']

                if(temps >= worst_niv2):
                    worst_niv2 = temps
                if (temps <= best_niv2):
                    best_niv2 = temps
            elif (i['niveau'] == 3):
                if (i['ratio'] == 100):
                    score += 5
                else:
                    score-= i['mauvaise_rep']

                if (temps >= worst_niv3):
                    worst_niv3 = temps
                if (temps <= best_niv3):
                    best_niv3 = temps
            else:
                score += i['ratio'] / 2
                if(i['ratio'] < worst_survival):
                    worst_survival = i['ratio']
                if (i['ratio'] > best_survival):
                    best_survival = i['ratio']

        worst_niv1 = str(time.strftime("%M:%S",worst_niv1))
        best_niv1 = str(time.strftime("%M:%S",best_niv1))
        worst_niv2 = str(time.strftime("%M:%S",worst_niv2))
        best_niv2 = str(time.strftime("%M:%S",best_niv2))
        worst_niv3 = str(time.strftime("%M:%S",worst_niv3))
        best_niv3 = str(time.strftime("%M:%S",best_niv3))


        ps = connection_players_stat()

        ps.put({'user': jou,
                'nb_parties': nb_parties,
                'worst_niv1': worst_niv1,
                'best_niv1': best_niv1,
                'worst_niv2': worst_niv2,
                'best_niv2': best_niv2,
                'worst_niv3': worst_niv3,
                'best_niv3': best_niv3,
                'best_survival': best_survival,
                'worst_survival': worst_survival,
                'score':score
               })





# ------------ PAGE

# menu = st.sidebar.selectbox(
#     "Where do you go ?",
#     ('Base', 'autre')
# )
#
# if(menu == 'Base'):
#     st.write("Yo Léo")
#     #base()
# else:
#     for key in st.session_state.keys():
#         del st.session_state[key]
#     menu_page()
