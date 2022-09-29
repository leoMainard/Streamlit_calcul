

import streamlit as st
import time
import datetime
import random as rd
import pandas as pd
import shutil
from  deta import Deta
from operator import itemgetter


# ------------ FUNCTIONS
def jeu(niv):
    niv = int(niv)

    if (niv == 1):
        min, max = 1, 10
    elif (niv == 2):
        min, max = 1, 100
    elif (niv == 3):
        min, max = 10, 100

    for i in range(10):

        a = rd.randint(min, max)
        b = rd.randint(min, max)

        value = rd.randint(0, 2)

        if (niv == 3):
            cal = [a * b, f'{a} x {b} = ']
        else:
            if value == 0:
                cal = [a * b, f'{a} x {b} = ']
            elif value == 1:
                cal = [a + b, f'{a} + {b} = ']
            else:
                cal = [a - b, f'{a} - {b} = ']

        st.session_state['cal_' + str(i)] = cal[0]
        st.session_state['cal_print_' + str(i)] = cal[1]


def confirm_button():
    st.session_state['result'] = 1
    st.session_state['restart'] = 0


# ------------ PAGE DE JEU

def game():
    # ---------------------------- Définition des session_state
    # ---------------------------- Si aucune info n'est enregistré, on les initialise à 0, sinon on les récupérera pour les afficher dans les input
    for i in range(10):
        if 'cal_' + str(i) not in st.session_state:
            st.session_state['cal_' + str(i)] = 0
        if 'cal_joueur_' + str(i) not in st.session_state:
            st.session_state['cal_joueur_' + str(i)] = 0
        if 'cal_print_' + str(i) not in st.session_state:
            st.session_state['cal_print_' + str(i)] = 0

    if 'result' not in st.session_state:
        st.session_state['result'] = 0

    if 'restart' not in st.session_state:
        st.session_state['restart'] = 1

    st.title('I Want to play !')

    niv = st.selectbox(
        "Choose the level of the game",
        ("---", "1", "2", "3"),
        key='niv'
    )

    st.write("Be careful, if you put at least one answer but decide to change the level, answers will be save.")

    if (niv != '---'):


        if st.session_state['restart'] == 1:
            jeu(niv)

        if st.session_state['result'] == 1:  # Affichage des résultats
            # On regarde si le joueur a réellement joué. S'il n'a mit aucune valeur dans les input, on ne sauvegarde pas les réponses et on n'affiche pas les résultats.
            # Le niveau recommencera
            vide = 0
            for i in range(10):  # On va vérifier que tous les réponses ne sont pas nulles, sinon on en déduit que le joueur n'a pas joué
                test_joueur = str(st.session_state['cal_joueur_' + str(i)])

                if (test_joueur == ""):
                    vide += 1

            if(vide != 10): # Si le joueur a mis au moins une réponse, on lui affiche les résultats et on sauvegarde

                bon_rep, mauv_rep = 0, 0

                for i in range(10):
                    test_cal = st.session_state['cal_' + str(i)]
                    test_joueur = st.session_state['cal_joueur_' + str(i)]

                    if str(test_cal) == test_joueur:
                        bon_rep += 1
                        suc = st.session_state['cal_print_' + str(i)] + st.session_state['cal_joueur_' + str(i)]
                        st.success(suc)
                    else:
                        mauv_rep += 1
                        err = st.session_state['cal_print_' + str(i)] + st.session_state[
                            'cal_joueur_' + str(i)] + "\t >>> Correction : " + st.session_state[
                                  'cal_print_' + str(i)] + str(st.session_state['cal_' + str(i)])
                        st.error(err)

                ratio = (bon_rep / (bon_rep + mauv_rep)) * 100
                lvl = int(niv)
                date = str(datetime.date.today())

                # ENREGISTREMENT DES DONNEES

                # connexion à la base de données
                deta_key = "a08tige2_PvhsiHXAgkfPxQe1V216HBn6Js3czaoz"
                deta = Deta(deta_key)
                db = deta.Base("cal_bdd")


                cle = int(st.session_state['last_key']) + 1

                db.put(
                    {'key': str(cle), 'user': st.experimental_user.email, 'date': date, 'niveau': lvl, 'bonne_rep': bon_rep,
                     'mauvaise_rep': mauv_rep, 'ratio': ratio})

                st.session_state['last_key'] = cle
                st.session_state['result'] = 0
                st.session_state['restart'] = 1
                st.button("Retry")
            else: # Sinon on ne sauvegarde pas les résultats et on ne les affiche pas, et on le fait recommencer
                st.session_state['result'] = 0
                st.session_state['restart'] = 1
                st.experimental_rerun()

        else:  # Affichage des calculs
            with st.form("my_form"):
                st.write("Try to complete each calculation, then confirm.")

                for i in range(10):
                    st.text_input(label="label" + str(i), value="", placeholder=st.session_state['cal_print_' + str(i)],
                                  key="cal_joueur_" + str(i), label_visibility="hidden")  # Réponse du joueur

                confirm = st.form_submit_button("Confirm", on_click=confirm_button())






# ------------ PAGE DE STATISTIQUES

def stat():
    # --------------------------------------------------------------------------
    # --------------------------------------------------------------------------

    st.title('My Statistics')

    option = st.selectbox(
        'Which level you need to see the statistics ?',
        ('All', '1', '2', '3'))

    # --------------------------------------------------------------------------
    # --------------------------------------------------------------------------

    st.session_state['stat_lvl'] = option

    # connexion à la base de données
    deta_key = "a08tige2_PvhsiHXAgkfPxQe1V216HBn6Js3czaoz"
    deta = Deta(deta_key)
    db = deta.Base("cal_bdd")

    if (option == "All"):
        data_temp = db.fetch({"user": st.experimental_user.email}).items
    else:
        data_temp = db.fetch({"user": st.experimental_user.email, "niveau": int(option)}).items

    data = sorted(data_temp, key=lambda d: int(d['key'])) # On tri les données par la clé (la clé étant du string dans la bdd, le '10' se situe avant le '2')

    mean_ratio = 0
    bon_rep = 0
    mauv_rep = 0
    ratio = []
    nb_item = 0  # Permet de savoir si le joueur a déjà fait des parties

    for i in data:
        nb_item += 1

        mean_ratio += i['ratio']
        bon_rep += i['bonne_rep']
        mauv_rep += i['mauvaise_rep']

        ratio.append(i['ratio'])

    if (nb_item == 0):
        st.write("No data for the moment, start to play to see your statistics.")
    else:
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Games played", nb_item)
        col2.metric("Average ratio", f'{round(mean_ratio / nb_item, 2)} %')
        col3.metric("Good answers", bon_rep)
        col4.metric("Bad answers", mauv_rep)

        st.subheader("Evolution of your ratio")
        st.line_chart(ratio)


# ------------ PAGE DE MENU


def menu_page():
    st.title(f'Hi {st.experimental_user.email} !')
    st.markdown('On this application, you can work your mental calculation and have a look to your progration !')
    st.markdown('Acceed to the training or statistics page with the menu on the left.')



# ------------ PAGE

# Connexion à la bdd pour récupérer la derniere key

deta_key = "a08tige2_PvhsiHXAgkfPxQe1V216HBn6Js3czaoz"
deta = Deta(deta_key)
db = deta.Base("cal_bdd")

data = db.fetch().items
nb_item = 0

if (data is None):
    st.session_state['last_key'] = 0
else:
    for i in data:
        nb_item += 1
    st.session_state['last_key'] = len(data)

menu = st.sidebar.selectbox(
    "Where do you go ?",
    ("Menu", "Game", "My statistics")
)

if (menu == 'Game'):
    game()
elif (menu == 'My statistics'):
    for key in st.session_state.keys():
        del st.session_state[key]
    stat()
else:
    for key in st.session_state.keys():
        del st.session_state[key]
    menu_page()


