#GanDalP November Project
from collections import deque

def time_to_second(hour, minute, second):
    return 3600*hour + 60*minute + second

def upward(departure, arrival):
    return (arrival > departure)

def downward(departure, arrival):
    return (arrival < departure)

UP = 1; DOWN = 0
class Elevator:

    global UP, DOWN
    v1 = 1; v2 = 3
    T = 11
    capacity = 17

    def __init__(self, L, M):
        self.position = M
        self.direction = UP
        self.max_floor = L-1
        self.first_floor = M
        self.people = {} #key = arrival floor, value = call_time
        self.remained_time_to_move = 0 #if elevator stops, it initialize with T
    
    def isStop(self):
        if self.remained_time_to_move: 
            self.remained_time_to_move -= 1
            return True
        return False
    
    def stop(self):
        self.remained_time_to_move = T
    
    def move_to(self, destination, isStop):
        self.position = destination

        if self.direction == UP and downward(self.position, destination):
            self.direction = DOWN
        elif self.direction == DOWN and upward(self.position, destination):
            self.direction = UP

        if isStop: self.stop()
    
    def add_people(self, item): return None

    def remove_people(self):
        return None
    
    def __str__(self):
        return ""

class Elevator_Simulator:

    global UP, DOWN
    start_time = 32400
    end_time = 86399
    buildings_data = {"Samsung":(49,4), "63-Building":(63, 5),"ESB":(102, 4)} #edit here!
    L, K, M = buildings_data["Samsung"]

    def __init__(self, querries):
        self.curr_time = start_time
        self.querries = querries #should be sorted time-decreasing order
        self.elevators = [Elevator(L, M) for _ in range(K)]
        self.floor = [[deque(),deque()] for _ in range(L)]
        self.total_time = 0

    def main(self, strategy):
        while self.curr_time <= end_time:
            if self.querries[-1][2] == self.curr_time:
                arrival, departure, call_time = self.querries.pop()
                if departure < arrival:
                    self.floor[departure][UP].append((arrival, call_time))
                else:
                    self.floor[departure][DOWN].append((arrival, call_time))
            for EV in self.elevators:
                if EV.isStop():
                    pass
                    #fill here!
            self.curr_time += 1

    def select_strategy(self, strategy):
        if strategy == "": return self.__func()
