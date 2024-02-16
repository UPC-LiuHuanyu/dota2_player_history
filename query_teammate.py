from utils import *

END_MATCH_ID = 7549585165
# END_MATCH_ID = 7486178491
MY_ID = 1035741118
TM_ID = 1125973295

all_matches = query_all(MY_ID, END_MATCH_ID)
for match in all_matches:
    print(match)
print(len(all_matches))

win_cnt, cnt, togather_win_cnt, togather_cnt = query_win_lose(all_matches, MY_ID, TM_ID)

print("------------------all------------------")
print("cnt = ", cnt)
print("win_cnt = ", win_cnt)
print("winning rate = ", float(win_cnt) / cnt)

print("------------------togather------------------")
print("togather_cnt = ", togather_cnt)
print("togather_win_cnt = ", togather_win_cnt)
print("winning rate = ", float(togather_win_cnt) / togather_cnt)

print("------------------solo------------------")
print("cnt = ", cnt - togather_cnt)
print("win_cnt = ", win_cnt - togather_win_cnt)
print("winning rate = ", float(win_cnt - togather_win_cnt) / (cnt - togather_cnt))