#GanDalP November Project
def time_to_second(hour, minute, second):
    return 3600*hour + 60*minute + second

class Elevator:

    UP = 1; DOWN = 0
    v1 = 1; v2 = 3

    def __init__(self, L, M):
        self.position = 0
        self.direction = UP
        self.max_floor = L
        self.first_floor = M
        self.velocity = v1
        self.open_time = T #edit here!
    
    def __str__(self):
        return ""

class Elevator_Simulator:

    start_time = 32400
    end_time = 86399
    buildings_data = {"Samsung":(49,4), "63-Building":(63, 5),"ESB":(102, 4)}
    L, K = buildings_data["Samsung"]

    def __init__(self, querries):
        self.curr_time = start_time
        self.querries = querries
        self.elevators = [Elevator(L, M) for _ in range(K)]
    
    