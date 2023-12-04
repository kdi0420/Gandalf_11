from Basic_setting_variables import *
from Gandalf import *
from constant import *

def test_S1(querries):
    global capacity, openning_time, closing_time, available_time, v1, v2, start_time, end_time, L, K, M

    S1 = Elevator_Simulator(querries, L, M, K)
    return S1.main()


with open("S1_500_231204.txt", 'w') as file:
    for i in range(500):
        querries = makeNCQuery()
        ans = str(test_S1(querries))
        file.write(ans + "\n")
        print(i, ans)

