from Basic_setting_variables import *
from Gandalf import *
from constant import *

def test_S1(querries):
    global capacity, openning_time, closing_time, available_time, v1, v2, start_time, end_time, L, K, M

    S1 = Elevator_Simulator(querries, L, M, K)
    return S1.main()

for i in range(100):
    querries = makeNCQuery()
    print(test_S1(querries))

