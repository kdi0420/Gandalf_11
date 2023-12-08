from Basic_setting_variables import *
from Gandalf import *
from constant import *

def test_S2(querries):
    global capacity, openning_time, closing_time, available_time, v1, v2, start_time, end_time, L, K, M

    S1 = High_Low(querries, L, M, K)
    return S1.main()

with open("S2_1000.txt", 'w') as file:
    for i in range(1000):
        querries = makeNCQuery()
        answer = test_S2(querries)
        file.write(str(answer) + "\n")
        print(f"{i}-th testcase : {answer:05} seconds")

