from utils import *

END_MATCH_ID = 7486178491
MY_ID = 1125973295 # hamasi
MY_ID = 1035741118 # 借的号
MY_ID = 117198261 # 大猪
TM_ID = 317280296
#
# print(api.get_player_summaries(185102236))
# exit(0)

all_matches = query_for_n_days(MY_ID, 60)
heros = get_hero_info()

for match in all_matches:
    print(match)
print(len(all_matches))

res_info = query_stranger(all_matches, MY_ID, TM_ID, heros)
if len(res_info) == 0:
    print("没排到过, 或者此人未公开战绩")

