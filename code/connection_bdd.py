from deta import Deta


def connection_cal_bdd():
    """

    :return: base de données cal_bdd
    """
    deta_key = "a08tige2_PvhsiHXAgkfPxQe1V216HBn6Js3czaoz"
    deta = Deta(deta_key)
    db = deta.Base("cal_bdd")

    return db


def connection_players_stat():
    """

    :return: base de données players_stat
    """
    players_key = "a08tige2_XzyWbFaNJTjuhwHuZzMaZxQA4humpKrW"
    deta = Deta(players_key)
    ps = deta.Base("players_stat")

    return ps
