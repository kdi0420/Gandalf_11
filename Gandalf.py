#GanDalP November Project
from collections import deque
from constant import *

UP = 1; DOWN = 0

class Elevator:

    global UP, DOWN, capacity, openning_time, closing_time, available_time, v1, v2

    def __init__(self, L, M, l=0):
        self.position = M
        self.direction = UP
        self.max_floor = L-1
        self.min_floor = l
        self.first_floor = M
        self.people = {} #key = arrival floor, value = call_time
        self.available = 0
        self.openning = 0
        self.closing = 0
        self.velocity = v1 #v1 = 1, v2 = 3
        self.destination = M
    
    def isStop(self):
        return (self.available or self.openning or self.closing)
    
    def isFull(self):
        return (len(self.people) == capacity)
    
    def stop(self):
        self.openning = openning_time
    
    def isAvailable(self):
        return self.available
    
    def operate(self):
        if self.openning:
            self.openning -= 1
            if not self.openning: self.available = available_time
        elif self.available:
            self.available -= 1
            if not self.available: self.closing = closing_time
        elif self.closing:
            self.closing -= 1

    def determine_destination(self, waiting_list):
        #determine_direction part
        if self.direction == UP:
            if self.position == self.max_floor: self.direction = DOWN
            elif self.people == {}:
                for floor in range(self.position, self.max_floor):
                    if waiting_list[floor][UP]: break
                else:
                    self.direction = DOWN
        
        else:
            if self.position == self.min_floor: self.direction = UP
            elif self.people == {}:
                for floor in range(1, self.position+1):
                    if waiting_list[floor][DOWN]: break
                else:
                    self.direction = UP
        
        #determine destination part
        if self.direction == UP:
            destination = min(self.max_floor, self.position + self.velocity)
            for possible_floor in range(self.velocity):
                curr_floor = self.position + possible_floor
                if curr_floor > self.max_floor: break
                if curr_floor in self.people and self.people[curr_floor] or waiting_list[curr_floor][UP]: destination = curr_floor; break
            return destination
        
        else:
            destination = max(self.min_floor, self.position - self.velocity)
            for possible_floor in range(self.velocity):
                curr_floor = self.position - possible_floor
                if curr_floor < self.min_floor: break
                if (curr_floor in self.people and self.people[curr_floor]) or waiting_list[curr_floor][DOWN]: destination = curr_floor; break
            return destination

    
    def add_people(self, item):
        arrival, call_time = item
        if arrival in self.people: 
            self.people[arrival].append(call_time)
        else:
            self.people[arrival] = [call_time]
        return None

    def remove_people(self, curr_time):
        used_time = 0
        if self.position not in self.people: return 0
        while self.people[self.position]:
            called_time = self.people[self.position].pop()
            used_time += curr_time - called_time
        return used_time
    
    def __str__(self):
        return ""

class Even_Odd_Elevator(Elevator):
    
    global UP, DOWN, capacity, openning_time, closing_time, available_time, v1, v2

    def __init__(self, isEven, L, M, l=0):
        self.position = M
        self.direction = UP
        self.max_floor = L-1
        self.min_floor = l
        self.first_floor = M
        self.people = {} #key = arrival floor, value = call_time
        self.available = 0
        self.openning = 0
        self.closing = 0
        self.velocity = v1 #v1 = 1, v2 = 3
        self.destination = M
        self.available_floor = []

        if isEven:
            self.available_floor = set( range(M+1, L, 2) + range(l, M, 2) + [M] )
        else:
            self.available_floor = set(range(l,L,2)) | set([M])


class Elevator_Simulator:

    global UP, DOWN, capacity, openning_time, closing_time, available_time, v1, v2

    def __init__(self, querries, L, M, K):
        self.curr_time = start_time
        self.querries = querries
        self.elevators = [Elevator(L, M) for _ in range(K)]
        self.waiting_list = [[deque(),deque()] for _ in range(L)]
        self.total_time = 0
    
    def add_query(self, query):
        arrival, departure, call_time = query
        if departure < arrival:
            self.waiting_list[departure][UP].append((arrival, call_time))
        else:
            self.waiting_list[departure][DOWN].append((arrival, call_time))

    def main(self):
        while self.curr_time <= end_time:
            while self.querries and self.querries[-1][2] == self.curr_time:
                self.add_query(self.querries.pop())
            
            for EV in self.elevators:
                if EV.isStop():
                    if not EV.isAvailable(): EV.operate(); continue
                    direction = EV.direction; curr_floor = EV.position
                    self.total_time += EV.remove_people(self.curr_time)
                    while (not EV.isFull()) and self.waiting_list[curr_floor][direction]:
                        EV.add_people(self.waiting_list[curr_floor][direction].popleft())
                    EV.operate()
                else:
                    destination = EV.determine_destination(self.waiting_list)
                    if (destination in EV.people and EV.people[destination]) or (self.waiting_list[destination][EV.direction]):
                        EV.stop()
                    elif destination == EV.position:
                        EV.stop()
                    EV.position = destination
            self.curr_time += 1
        return self.total_time

class High_Low(Elevator_Simulator):

    def __init__(self, querries, L, M, K):
        self.curr_time = start_time
        self.querries = querries
        self.elevators = [Elevator(L, L//2, L//2) for _ in range(K//2)] + [Elevator(L//2+1, M) for _ in range(K - K//2)]
        self.waiting_list = [[deque(),deque()] for _ in range(L)]
        self.total_time = 0
    
    def main(self):
        while self.curr_time <= end_time:
            while self.querries and self.querries[-1][2] == self.curr_time:
                arrival, departure, call_time = self.querries.pop()
                if departure < arrival:
                    self.waiting_list[departure][UP].append((arrival, call_time))
                else:
                    self.waiting_list[departure][DOWN].append((arrival, call_time))
            
            for EV in self.elevators:
                if EV.isStop():
                    if not EV.isAvailable(): EV.operate(); continue
                    direction = EV.direction; curr_floor = EV.position
                    self.total_time += EV.remove_people(self.curr_time)
                    while (not EV.isFull()) and self.waiting_list[curr_floor][direction]:
                        EV.add_people(self.waiting_list[curr_floor][direction].popleft())
                    EV.operate()
                else:
                    destination = EV.determine_destination(self.waiting_list)
                    if (destination in EV.people and EV.people[destination]) or (self.waiting_list[destination][EV.direction]):
                        EV.stop()
                    elif destination == EV.position:
                        EV.stop()
                    EV.position = destination
            self.curr_time += 1
        return self.total_time



class Even_Odd(Elevator_Simulator):

    def __init__(self, querries, L, M, K):
        self.curr_time = start_time
        self.querries = querries
        self.elevators = [Elevator(L, M) for _ in range(K)]
        self.waiting_list = [[deque(),deque()] for _ in range(L)]
        self.total_time = 0


class Collective_Control(Elevator_Simulator):

    def __init__(self, querries, L, M, K):
        self.curr_time = start_time
        self.querries = querries
        self.elevators = [Elevator(L, M) for _ in range(K)]
        self.waiting_list = [[deque(),deque()] for _ in range(L)]
        self.total_time = 0
