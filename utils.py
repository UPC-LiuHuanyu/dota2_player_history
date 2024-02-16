import dota2api
from datetime import datetime
import json

API_KEY = "这个需要去steam打开开发者权限. 然后把key放到这里"
with open("key.json", "r") as f:
    API_KEY = json.load(f)["key"]

api = dota2api.Initialise(API_KEY)


class MatchTogether:

    def __init__(self, my_id, his_id, match_id, my_hero_id, his_hero_id, be_tm, me_win):
        self.my_id = my_id
        self.his_id = his_id
        self.match_id = match_id
        self.my_hero_id = my_hero_id
        self.his_hero_id = his_hero_id
        self.be_tm = be_tm
        self.me_win = me_win


def get_hero_info():
    heroes = api.get_heroes()
    res_map = {}
    for hero in heroes["heroes"]:
        res_map[hero["id"]] = hero
    return res_map


def query_for_n_days(my_id, n_days):
    today = datetime.now()
    print(today)
    now_sec = int(today.timestamp())
    print(now_sec)

    secs = n_days * 24 * 60 * 60
    end_sec = now_sec - secs
    print(end_sec)
    print(datetime.fromtimestamp(end_sec))

    last_game_id = None
    all_matches = []
    cnt = 0
    jump_one = False
    while True:
        print("start at ", last_game_id)
        hist1 = api.get_match_history(account_id=my_id, matches_requested=100, start_at_match_id=last_game_id)
        if len(hist1["matches"]) == 1:
            return all_matches
        for match in hist1["matches"]:
            if jump_one:
                jump_one = False
                continue
            cnt += 1
            all_matches.append(match)
            if match["start_time"] < end_sec:
                print("done! total cnt = ", cnt)
                return all_matches
            last_game_id = match["match_id"]
        jump_one = True


def query_all(my_id, end_match_id, start_match_id=None):
    last_game_id = start_match_id
    cnt = 0
    jump_one = False

    all_matches = []
    while True:
        print("start at ", last_game_id)
        hist1 = api.get_match_history(account_id=my_id, matches_requested=100, start_at_match_id=last_game_id)
        if len(hist1["matches"]) == 1:
            return all_matches
        for match in hist1["matches"]:
            if jump_one:
                jump_one = False
                continue
            cnt += 1
            all_matches.append(match)
            if match["match_id"] == end_match_id:
                print("done! total cnt = ", cnt)
                return all_matches
            last_game_id = match["match_id"]
        jump_one = True


def query_win_lose(all_matches, my_id, tm_id):
    togather_cnt = 0
    togather_win_cnt = 0

    cnt = len(all_matches)
    win_cnt = 0
    for match in all_matches:
        win = False
        with_teammate = False
        for player_info in match["players"]:
            if player_info["account_id"] == my_id:
                team_id = player_info["team_number"]
                match_info = api.get_match_details(match_id=match["match_id"])
                if match_info["radiant_win"] and team_id == 0:
                    win = True
                elif not match_info["radiant_win"] and team_id == 1:
                    win = True

            if player_info["account_id"] == tm_id:
                with_teammate = True
        if win:
            win_cnt += 1
        if with_teammate:
            togather_cnt += 1
            if win:
                togather_win_cnt += 1

        print("match_id = ", match["match_id"], ". winning: ", win, ", with teammate: ", with_teammate)

    return win_cnt, cnt, togather_win_cnt, togather_cnt


def query_stranger(all_matches, my_id, tm_id, heros):
    res = []
    for match in all_matches:
        win = False
        his_team = None
        my_team = None
        his_hero = None
        my_hero = None
        for player_info in match["players"]:
            team_id = player_info["team_number"]
            if "account_id" in player_info.keys() and player_info["account_id"] == my_id:
                my_team = team_id
                my_hero = player_info["hero_id"]

            if "account_id" in player_info.keys() and player_info["account_id"] == tm_id:
                his_team = team_id
                his_hero = player_info["hero_id"]

        if his_team is not None:  # 存在说明排到一起过
            print("-------------------")
            print("排到过一起！ match id：", match["match_id"], ", 时间: ", datetime.fromtimestamp(match["start_time"]))
            match_info = api.get_match_details(match_id=match["match_id"])
            if match_info["radiant_win"] and my_team == 0:
                win = True
            elif not match_info["radiant_win"] and my_team == 1:
                win = True
            print("该局我的胜负：", "胜" if win else "负")
            if his_team == my_team:
                print("我和他的关系： 队友。")
            else:
                print("我和他的关系： 对手。")

            print("他玩的英雄：", heros[his_hero]["localized_name"])
            print("我玩的英雄：", heros[my_hero]["localized_name"])
            res.append(MatchTogether(my_id, tm_id, match["match_id"], my_hero, his_hero, his_team == my_team, win))
    return res
