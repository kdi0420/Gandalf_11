from Basic_setting_variables import *
from Gandalf import *
from constant import *

def test_S1(querries):
    S1 = Collective_Control(querries, L, M, K)
    return S1.main()

with open("just_test.txt", 'w') as file:
    for i in range(100):
        querries = makeNCQuery()
        answer = test_S1(querries)
        file.write(str(answer) + "\n")
        print(f"{i}-th testcase : {answer:05} seconds")

