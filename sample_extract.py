import openpyxl
import datetime
from Basic_setting_variables import *
from Gandalf import *
from constant import *

def strategy_collective_control(queries): #S1 strategy
    S1 = Collective_Control(queries, L, M, K)
    return S1.main()

def strategy_high_low(queries): #S2 strategy
    S2 = High_Low(queries, L, M, K)
    return S2.main()

def strategy_even_odd(queries): #S3 strategy
    S3 = Even_Odd(queries, L, M, K)
    return S3.main()


def save_into_Excel(attempts, mode = 4):
    now = datetime.datetime.now()
    today = now.strftime('%Y%m%d')
    modes = 'S'+f'{mode}'
    sheet_name = '_'.join([modes, str(attempts), today])

    file_path = './history.xlsx'
    write_wb = openpyxl.load_workbook(file_path)
    write_ws = write_wb.create_sheet(title=sheet_name)
    write_ws.append(['attempt'] + ['S'+f'{i}' for i in range(1,4)])

    for attempt in range(1,attempts+1):
        queries = makeNCQuery()
        if mode == 4:
            datas = [attempt, strategy_collective_control(queries[:]), strategy_high_low(queries[:]), strategy_even_odd(queries[:])]
        elif mode == 1:
            datas = [attempt, strategy_collective_control(queries), 0, 0]
        elif mode == 2:
            datas = [attempt, 0, strategy_high_low(queries), 0]
        elif mode == 3:
            datas = [attempt, 0, 0, strategy_even_odd(queries)]
        write_ws.append(datas)
        print(f"{attempt}-th testcase : {datas[1]:05} / {datas[2]:05} / {datas[3]:05}  seconds")

    write_wb.save(file_path)


# --------- User Manual ----------
# attempt : the number of queries
#   mode  : the order of strategy 
#  
#           (1) - Collective Control
#           (2) - High-Low
#           (3) - Even-Odd
# [default] (4) - trying all kinds of strategies  
#  
# ----------- Result -------------
#  
#  those are stored in 'history.xlsx', the Excel file
#
#  sheet title = [S{mode number}_{queries number}_{date}]
# 
#  example) if mode is 3, we tried 1000 queries in 9, Dec.,
#       then, sheet title would be "S3_1000_20231209"
# 
#  
#      < following examples >
#  
#  attempt |    S1    |    S2    |    S3
#     1    |   12093  |     0    |     0      case 1) mode = 1
#     2    |     0    |   13928  |     0      case 2) mode = 2
#     3    |     0    |     0    |   10293    case 3) mode = 3
#     4    |   12093  |   13928  |   10293    case 4) mode = 4
# 
# you can check above them in 'history.xlsx' file!

save_into_Excel(attempts=100, mode=2)