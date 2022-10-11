import streamlit as st
import time
import datetime
import random as rd
import pandas as pd
import shutil
from deta import Deta
from operator import itemgetter
from connection_bdd import connection_cal_bdd, connection_players_stat


# ------------ FUNCTIONS

st.set_page_config(
    page_title="Calcul Master",
    page_icon="🤖",
    layout="wide",
)

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



def survival_game(progression):
    if (int(progression) <= 5):
        a = rd.randint(1, 5)
        b = rd.randint(1, 5)

        value = rd.randint(0, 2)

        if value == 0:
            cal = [a - b, f'{a} - {b} = ']
        else:
            cal = [a + b, f'{a} + {b} = ']

    elif (int(progression) <= 10):
        a = rd.randint(3, 10)
        b = rd.randint(3, 10)

        value = rd.randint(0, 2)

        if value == 0:
            cal = [a * b, f'{a} x {b} = ']
        elif value == 1:
            cal = [a + b, f'{a} + {b} = ']
        else:
            cal = [a - b, f'{a} - {b} = ']

    elif (int(progression) <= 15):
        a = round(rd.random(), 1)
        b = round(rd.random(), 1)

        cal = [round(a * b,2), f'{a} x {b} = ']

    elif (int(progression) <= 20):
        a = rd.randint(10, 20)
        b = rd.randint(10, 20)

        value = rd.randint(0, 2)
        if value == 0:
            cal = [a * b, f'{a} x {b} = ']
        elif value == 1:
            cal = [a + b, f'{a} + {b} = ']
        else:
            cal = [a - b, f'{a} - {b} = ']

    elif (int(progression) <= 30):
        a = rd.randint(10, 50)
        b = rd.randint(10, 50)

        cal = [a * b, f'{a} x {b} = ']

    elif (int(progression) <= 40):
        a = rd.randint(100, 1000)
        b = rd.randint(100, 1000)
        value = rd.randint(0, 1)
        if value == 1:
            cal = [a + b, f'{a} + {b} = ']
        else:
            cal = [a - b, f'{a} - {b} = ']

    elif (int(progression) <= 45):
        a = str(rd.randint(10, 50)) + '.' + str(rd.randint(10, 50))
        b = str(rd.randint(10, 50)) + '.' + str(rd.randint(10, 50))

        value = rd.randint(0, 1)

        if value == 1:
            cal = [round(float(a) + float(b),4), f'{a} + {b} = ']
        else:
            cal = [round(float(a) - float(b),4), f'{a} - {b} = ']

    elif (int(progression) <= 50):
        a = rd.randint(10, 100)
        b = rd.randint(3, 10)

        cal = [a * b, f'{a} x {b} = ']

    elif (int(progression) <= 60):
        a = rd.randint(10, 100)
        b = rd.randint(10, 100)

        cal = [a * b, f'{a} x {b} = ']

    elif (int(progression) <= 70):
        a = rd.randint(10, 1000)
        b = rd.randint(3, 15)

        cal = [a * b, f'{a} x {b} = ']

    elif (int(progression) <= 70):
        a = str(rd.randint(10, 50)) + '.' + str(rd.randint(10, 50))
        b = str(rd.randint(10, 50)) + '.' + str(rd.randint(10, 50))

        cal = [round(float(a) * float(b),4), f'{a} x {b} = ']

    elif (int(progression) <= 80):
        a = str(rd.randint(50, 100)) + '.' + str(rd.randint(50, 100))
        b = str(rd.randint(50, 100)) + '.' + str(rd.randint(50, 100))

        cal = [round(float(a) * float(b),6), f'{a} x {b} = ']

    elif (int(progression) <= 90):
        a = rd.randint(10, 100)
        b = rd.randint(10, 100)

        value = rd.randint(0, 1)

        if value == 1:
            cal = [(a + b) ** 2, f'({a} + {b})² = ']
        else:
            cal = [(a - b) ** 2, f'({a} - {b})² = ']

    elif (int(progression) <= 99):
        a = rd.randint(1, 10)
        b = rd.randint(1, 10)

        value = rd.randint(0, 1)

        if value == 1:
            cal = [((a ** 2) + (b ** 2)) ** 2, f'({a}² + {b}²)² = ']
        else:
            cal = [((a ** 2) - (b ** 2)) ** 2, f'({a}² - {b}²)² = ']

    else:
        cal = [1, 'exp(0) = ']

    st.session_state['survival_cal_print'] = cal[1]
    st.session_state['survival_cal'] = cal[0]



def survival_verif():
    st.session_state['survival_result'] = 1


def confirm_button():
    st.session_state['result'] = 1
    st.session_state['restart'] = 0


def rerun():
    # niv 1-2-3
    st.session_state['result'] = 0
    st.session_state['restart'] = 1
    # survival
    st.session_state['progression_bar'] = 0
    st.session_state['survival_result'] = 0
    st.session_state['survival_cal'] = 0
    st.session_state['survival_cal_joueur'] = 0
    st.session_state['survival_cal_print'] = 0
    st.session_state['survival_score'] = 0


def get_sec(time_str):
    """Get seconds from time."""
    m, s = time_str.split(':')
    return int(m) * 60 + int(s)



# ------------ PAGE DE JEU


# ---------------------------- Définition des session_state
# ---------------------------- Si aucune info n'est enregistré, on les initialise à 0, sinon on les récupérera pour les afficher dans les input

# Connexion à la bdd pour récupérer la derniere key

deta_key = "a08tige2_PvhsiHXAgkfPxQe1V216HBn6Js3czaoz"
deta = Deta(deta_key)
db = deta.Base("cal_bdd")

data = db.fetch().items
nb_item = 0

if (data is None):
    st.session_state['last_key'] = 0 # last_key est l'index de la base de donnees
else:
    st.session_state['last_key'] = len(data)

# Sessions pour les calculs, les print et les résultats des niveaux 1 - 2 - 3 ------------------------------------------------------------------------------------
for i in range(10):
    if 'cal_' + str(i) not in st.session_state:
        st.session_state['cal_' + str(i)] = 0
    if 'cal_joueur_' + str(i) not in st.session_state:
        st.session_state['cal_joueur_' + str(i)] = 0
    if 'cal_print_' + str(i) not in st.session_state:
        st.session_state['cal_print_' + str(i)] = 0

# Sessions pour les niveaux 1 - 2 - 3 ------------------------------------------------------------------------------------
if 'result' not in st.session_state:
    st.session_state['result'] = 0

if 'restart' not in st.session_state:
    st.session_state['restart'] = 1

# Sessions pour le niveau Survival ------------------------------------------------------------------------------------
if 'progression_bar' not in st.session_state:
    st.session_state['progression_bar'] = 0

if 'survival_result' not in st.session_state:  # verification des resultats et affichage si erreur
    st.session_state['survival_result'] = 0

if 'survival_cal' not in st.session_state:  # resultat attendu du calcul
    st.session_state['survival_cal'] = 0

if 'survival_cal_joueur' not in st.session_state:  # resultat du joueur
    st.session_state['survival_cal_joueur'] = 0

if 'survival_cal_print' not in st.session_state:  # calcul ecrit
    st.session_state['survival_cal_print'] = 0

if 'survival_score' not in st.session_state:
    st.session_state['survival_score'] = 0

# Sessions pour le calcul de temps ------------------------------------------------------------------------------------
if 'start' not in st.session_state:
    st.session_state['start'] = 1

if 'time' not in st.session_state:
    st.session_state['time'] = 1

st.title('🕹️I Want to play !')

niv = st.selectbox(
    "Choose the level of the game",
    ("---", "1", "2", "3", "Survival"),
    key='niv'
)


if (niv == '---'):

    # Explication des règles
    st.subheader("Rules : ")
    st.write("Level 1 to 3")
    st.warning("Be careful, when you chose a level, you have 3 seconds to prepare yourself.\n"
            "After that, the level start and a timer is activated. If you are not ready, you can restart by re-choosing the level or by clicking on the 'Retry' button.\n\n"
            "If you put at least one answer but decide to change the level, answers will be save.\n\n"
            "Good luck !")
    st.write("Survival level")
    st.info("Survival mode start when you chose it. You have all your time to complete 100 levels. Of course, the difficulty will increase. \n\n"
            "When you put an answer, you can validate it with <Enter> or <Tabulation>, and an other calculation will appear.\n\n"
            "Good luck ! For real !")

    # reboot session niv 1-2-3
    st.session_state['result'] = 0
    st.session_state['restart'] = 1
    # reboot session survival
    st.session_state['progression_bar'] = 0
    st.session_state['survival_result'] = 0
    st.session_state['survival_cal'] = 0
    st.session_state['survival_cal_joueur'] = 0
    st.session_state['survival_cal_print'] = 0
    st.session_state['survival_score'] = 0



elif (niv == 'Survival'):
    # reboot session niv 1-2-3
    st.session_state['result'] = 0
    st.session_state['restart'] = 1

    if (st.session_state['survival_score'] == 0):
        st.session_state['start'] = time.time()

    if (st.session_state['survival_score'] == 100):

        st.balloons()
        st.header('Congratulations ! You are the best')

        time.sleep(3)

        st.session_state['survival_result'] = 0
        st.session_state['progression_bar'] = 0
        st.session_state['survival_score'] = 0
        st.experimental_rerun()

    if (st.session_state['survival_result'] == 0):

        st.subheader("Your progression : ")
        my_bar = st.progress(st.session_state['progression_bar'])  # On met à jour la barre de progression

        survival_game(st.session_state['progression_bar'])  # On met en place les calculs du jeu

        st.text_input(label="survival_label", value="", key='survival_cal_joueur',
                      placeholder=st.session_state['survival_cal_print'], label_visibility="hidden",
                      on_change=survival_verif())  # Réponse du joueur

    else:
        if (str(st.session_state['survival_cal_joueur']) == str(st.session_state['survival_cal'])):
            st.session_state['survival_result'] = 0
            st.session_state['progression_bar'] += 1
            st.session_state['survival_score'] += 1
            st.experimental_rerun()
        else:
            if(st.session_state['progression_bar'] != 0):
                temps = time.time() - st.session_state['start']

                seconds = temps % 60
                minutes = temps // 60

                temps = "%02d:%02d" % (minutes, seconds)

                err = st.session_state['survival_cal_print'] + st.session_state['survival_cal_joueur'] + ' >>> ' + \
                      st.session_state['survival_cal_print'] + str(st.session_state['survival_cal'])

                st.error(err)
                st.info(f"Your score : {st.session_state['survival_score']} / 100")
                st.info(f"Your time : {temps}")


                # ENREGISTREMENT DES DONNEES
                # connexion à la base de données
                deta_key = "a08tige2_PvhsiHXAgkfPxQe1V216HBn6Js3czaoz"
                deta = Deta(deta_key)
                db = deta.Base("cal_bdd")

                cle = int(st.session_state['last_key']) + 1
                date = str(datetime.date.today())
                bon_rep = int(st.session_state['survival_score'])
                mauv_rep = 100 - int(st.session_state['survival_score'])
                niv = 4

                db.put({'index': str(cle), 'user': st.experimental_user.email, 'date': date, 'niveau': niv,
                     'bonne_rep': bon_rep,
                     'mauvaise_rep': mauv_rep, 'ratio': bon_rep, 'temps': temps})

                ps = connection_players_stat()
                players_stat = ps.fetch({"user": st.experimental_user.email}).items

                key = ""
                updates = {}
                for i in players_stat:
                    key = i['key']
                    if(bon_rep < int(i['worst_survival'])):
                        updates['worst_survival'] = bon_rep
                    if (bon_rep > int(i['best_survival'])):
                        updates['best_survival'] = bon_rep
                    updates['score'] = i['score'] + (bon_rep/2)
                    updates['nb_parties'] = i['nb_parties'] + 1

                ps.update(updates, key)

                st.session_state['survival_result'] = 0
                st.session_state['progression_bar'] = 0
                st.session_state['survival_score'] = 0

                st.button('Try again !')
            else:
                st.session_state['survival_result'] = 0
                st.session_state['progression_bar'] = 0
                st.session_state['survival_score'] = 0
                st.experimental_rerun()
else:
    # reboot session survival
    st.session_state['progression_bar'] = 0
    st.session_state['survival_result'] = 0
    st.session_state['survival_cal'] = 0
    st.session_state['survival_cal_joueur'] = 0
    st.session_state['survival_cal_print'] = 0
    st.session_state['survival_score'] = 0

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

        if (vide != 10):  # Si le joueur a mis au moins une réponse, on lui affiche les résultats et on sauvegarde

            # Ajouter du temps ici ------------------------------------------------------------------------------------
            st.session_state['time'] = time.time()
            temps = time.time() - st.session_state['start']

            seconds = temps % 60
            minutes = temps // 60

            temps = "%02d:%02d" % (minutes, seconds)

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

            # Affichage du temps ------------------------------------------------------------------------------------
            st.info(f'Your time : {temps}')

            # ENREGISTREMENT DES DONNEES

            # connexion à la base de données
            deta_key = "a08tige2_PvhsiHXAgkfPxQe1V216HBn6Js3czaoz"
            deta = Deta(deta_key)
            db = deta.Base("cal_bdd")

            cle = int(st.session_state['last_key']) + 1

            db.put(
                {'index': str(cle), 'user': st.experimental_user.email, 'date': date, 'niveau': lvl,
                 'bonne_rep': bon_rep,
                 'mauvaise_rep': mauv_rep, 'ratio': ratio, 'temps': temps})

            ps = connection_players_stat()
            players_stat = ps.fetch({"user": st.experimental_user.email}).items

            key = ""
            updates = {}
            for i in players_stat:
                temps_diff = get_sec(temps)

                key = i['key']
                if (temps_diff > get_sec(i['worst_niv' + str(lvl)])):
                    updates['worst_niv' + str(lvl)] = temps
                if (temps_diff < get_sec(i['best_niv' + str(lvl)])):
                    updates['best_niv' + str(lvl)] = temps
                if(bon_rep == 10):
                    updates['score'] = i['score'] + (5 * lvl)
                else:
                    updates['score'] = i['score'] - mauv_rep
                updates['nb_parties'] = i['nb_parties'] + 1

            ps.update(updates, key)


            st.session_state['last_key'] = cle
            st.session_state['result'] = 0
            st.session_state['restart'] = 1
            st.button("Retry")

        else:  # Sinon on ne sauvegarde pas les résultats et on ne les affiche pas, et on le fait recommencer
            st.session_state['result'] = 0
            st.session_state['restart'] = 1
            st.experimental_rerun()

    else:  # Affichage des calculs

        with st.spinner(' Be ready !'):
            time.sleep(3)

        with st.form("my_form"):

            # Ajouter du temps ici ------------------------------------------------------------------------------------
            st.session_state['start'] = time.time()

            st.write("Try to complete each calculation, then confirm.")

            for i in range(10):
                st.text_input(label="label" + str(i), value="", placeholder=st.session_state['cal_print_' + str(i)],
                              key="cal_joueur_" + str(i), label_visibility="hidden")  # Réponse du joueur

            confirm = st.form_submit_button("Confirm", on_click=confirm_button())
