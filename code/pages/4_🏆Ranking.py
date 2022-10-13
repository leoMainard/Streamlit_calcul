import streamlit as st
from connection_bdd import connection_cal_bdd, connection_players_stat

st.set_page_config(
    page_title = "Calcul Master",
    page_icon="🤖",
    layout="wide",
)

def get_sec(time_str):
    """Get seconds from time."""
    m, s, c = time_str.split(':')
    return int(m) * 60 + int(s) + (int(c)/10)

st.title('🏆 The best are here !')

db = connection_players_stat()

data_temp = db.fetch().items

data = sorted(data_temp, key=lambda d: float(d['score']))  # On tri les données par le score

top = 1
best1, best2, best3 = "59:59:99", "59:59:99", "59:59:99"
best_surv = 0
user1, user2, user3 = "","",""

col1, col2 = st.columns(2)

#temps_diff = get_sec(temps)


col1.header("1️⃣Ranking of score")
col2.header("2️⃣Goals to beat")


for i in data[::-1]:

    if(get_sec(i['best_niv1']) < get_sec(best1)):
        best1 = i['best_niv1']
        user1 = i['user'].split("@")[0]

    if(get_sec(i['best_niv2']) < get_sec(best2)):
        best2 = i['best_niv2']
        user2 = i['user'].split("@")[0]

    if(get_sec(i['best_niv3']) < get_sec(best3)):
        best3 = i['best_niv3']
        user3 = i['user'].split("@")[0]

    if(i['best_survival'] > best_surv):
        best_surv = i['best_survival']
        user_surv = i['user'].split("@")[0]

    emoji_list = ['🥇','🥈','🥉']
    if(top == 1):
        emoji = emoji_list[0]
    elif (top == 2):
        emoji = emoji_list[1]
    elif (top == 3):
        emoji = emoji_list[2]
    else:
        emoji = ""

    texte = f'{emoji} {i["user"].split("@")[0]} ➡️score : {i["score"]}'

    if(top < 4):
        col1.success(texte)
    else:
        col1.warning(texte)

    top += 1

text_best1 = f'🙂Best time for level 1️⃣ : {best1} ➡️ {user1}'
text_best2 = f'🤗Best time for level 2️⃣ : {best2} ➡️ {user2}'
text_best3 = f'😮Best time for level 3️⃣ : {best3} ➡️ {user3}'
text_surv = f'🤯Best score for survival level : {best_surv} ➡️ {user_surv}'
col2.info(text_best1)
col2.info(text_best2)
col2.info(text_best3)
col2.info(text_surv)