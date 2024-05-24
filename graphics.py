import tkinter as tk
from tkinter import ttk
from collections import deque
from random import random
from constant import *
from Basic_setting_variables import *

# Gandalf.py 파일의 내용
UP = 1
DOWN = 0

class Elevator:
    def __init__(self, L, M, l=0, ignore=False):
        self.position = M
        self.direction = UP
        self.max_floor = L-1
        self.min_floor = l
        self.first_floor = M
        self.people = {}
        self.numPeople = 0
        self.available = 0
        self.openning = 0
        self.closing = 0
        self.velocity = v1
        self.destination = M
        self.isIgnore = ignore
    
    def isStop(self):
        return (self.available or self.openning or self.closing)
    
    def isFull(self):
        return (self.numPeople == capacity)
    
    def stop(self):
        self.openning = openning_time
    
    def isAvailable(self):
        return self.available
    
    def getCurrentFloor(self):
        return self.position

    def getDirection(self):
        return self.direction
    
    def getCalledList(self):
        return list(self.people.keys())
    
    def operate(self):
        if self.openning:
            self.openning -= 1
            if not self.openning: self.available = available_time
        elif self.available:
            self.available -= 1
            if not self.available: self.closing = closing_time
        elif self.closing:
            self.closing -= 1
    
    def ignore(self):
        calc_mode = "capacity"
        additional = self._additional(calc_mode)
        ignore_prob = self._calculate_ignore_prob(calc_mode, additional)
        return not self._ignore_call(ignore_prob)
    
    def _additional(self, calc_mode):
        if calc_mode == "capacity": return None
        if calc_mode == "similar": return 0
        if calc_mode == "complexity": return float('inf')
        if calc_mode == "call": return 0
    
    def _ignore_call(self, ignore_prob):
        comp_prob = random()
        return (comp_prob <= ignore_prob)
    
    def _calculate_ignore_prob(self, calc_mode="capacity", additional=0):
        if calc_mode == "capacity":
            return self.numPeople / capacity
        if calc_mode == "similar":
            return additional
        if calc_mode == "complexity":
            criteria_complexity = 0.1
            if additional < criteria_complexity:
                return (criteria_complexity - additional) / criteria_complexity
        if calc_mode == "call":
            temp = min(1, 15 / additional)
            return 1 - temp

    def determine_destination(self, waiting_list):
        if self.direction == UP:
            if self.position == self.max_floor: self.direction = DOWN
            elif self.people == {}:
                for floor in range(self.position, self.max_floor):
                    if self.isIgnore and waiting_list[floor][UP]: break
                    elif (not self.isIgnore) and waiting_list[floor][UP] and self.ignore(): break
                else:
                    self.direction = DOWN
        else:
            if self.position == self.min_floor: self.direction = UP
            elif self.people == {}:
                for floor in range(self.min_floor+1, self.position+1):
                    if self.ignore() and waiting_list[floor][DOWN]: break
                    elif (not self.isIgnore) and waiting_list[floor][DOWN] and self.ignore(): break
                else:
                    self.direction = UP
        
        if self.direction == UP:
            destination = min(self.max_floor, self.position + self.velocity)
            for possible_floor in range(self.velocity):
                curr_floor = self.position + possible_floor
                if curr_floor > self.max_floor: break
                if (curr_floor in self.people and self.people[curr_floor]): destination = curr_floor; break
                if (not self.isIgnore):
                    if (waiting_list[curr_floor][UP] and self.ignore()): destination = curr_floor; break
                elif waiting_list[curr_floor][UP]: destination = curr_floor; break
            return destination
        else:
            destination = max(self.min_floor, self.position - self.velocity)
            for possible_floor in range(self.velocity):
                curr_floor = self.position - possible_floor
                if curr_floor < self.min_floor: break
                if (curr_floor in self.people and self.people[curr_floor]): destination = curr_floor; break
                if (not self.isIgnore):
                    if (waiting_list[curr_floor][DOWN] and self.ignore()): destination = curr_floor; break
                elif waiting_list[curr_floor][DOWN]: destination = curr_floor; break
            return destination

    def add_people(self, item):
        arrival, call_time = item
        if arrival in self.people:
            self.people[arrival].append(call_time)
        else:
            self.people[arrival] = [call_time]
        self.numPeople += 1

    def remove_people(self, curr_time):
        used_time = 0
        if self.position not in self.people: return 0
        while self.people[self.position]:
            called_time = self.people[self.position].pop()
            used_time += curr_time - called_time
            self.numPeople -= 1
        return used_time
    
    def __str__(self):
        return ""

class Elevator_Simulator:
    def __init__(self, querries, L, M, K, i=False):
        self.curr_time = start_time
        self.querries = querries
        self.elevators = [Elevator(L, M, ignore=i) for _ in range(K)]
        self.waiting_list = [[deque(),deque()] for _ in range(L)]
        self.total_time = 0

    def step(self):
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

# GUI 코드
class ElevatorSimulatorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Elevator Simulator")

        # 엘리베이터 시스템 초기화
        self.simulator = Elevator_Simulator(querries=makeNCQuery(), L=L, M=M, K=K)

        # 메인 프레임 설정
        self.main_frame = ttk.Frame(self.root, padding="10")
        self.main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # 현재 시간과 속도 초기화
        self.current_time = 0
        self.speed = 1.0

        # 시간 제어 추가
        self.time_controls()
        
        # 엘리베이터 표시 추가
        self.elevator_display()
        
        # 현재 승객 표시 추가
        self.passengers_display()

        # 시뮬레이션 루프 시작
        self.update_time()

    def time_controls(self):
        time_frame = ttk.Labelframe(self.main_frame, text="Time Control", padding="10")
        time_frame.grid(row=0, column=0, sticky=(tk.W, tk.E))
        
        self.time_label = ttk.Label(time_frame, text=f"Current time: {self.simulator.curr_time}s")
        self.time_label.grid(row=0, column=0)
        
        self.time_speed = tk.DoubleVar(value=1.0)
        self.speed_scale = ttk.Scale(time_frame, from_=0.1, to=100.0, orient=tk.HORIZONTAL, variable=self.time_speed, command=self.update_speed_display)
        self.speed_scale.grid(row=0, column=1)
        
        self.speed_label = ttk.Label(time_frame, text="Speed: x1.0")
        self.speed_label.grid(row=0, column=2)

        self.speed_entry = ttk.Entry(time_frame, width=5)
        self.speed_entry.grid(row=0, column=3)
        self.speed_entry.insert(0, "1.0")
        self.speed_entry.bind("<Return>", self.update_speed_from_entry)
    
    def update_speed_display(self, event):
        self.speed = self.time_speed.get()
        self.speed_label.config(text=f"Speed: x{self.speed:.1f}")
        self.speed_entry.delete(0, tk.END)
        self.speed_entry.insert(0, f"{self.speed:.1f}")

    def update_speed_from_entry(self, event):
        try:
            speed = float(self.speed_entry.get())
            if speed > 0:
                self.speed = speed
                self.speed_scale.set(min(speed, 100.0))  # 슬라이더 업데이트, 최대 가시 값은 100.0
                self.speed_label.config(text=f"Speed: x{speed:.1f}")
        except ValueError:
            pass
    
    def update_time(self):
        self.simulator.step()
        self.time_label.config(text=f"Current time: {self.simulator.curr_time}s")
        
        # 새 상태에 따라 엘리베이터 표시 업데이트
        self.update_elevator_positions()
        self.update_waiting_list()
        self.update_passenger_info()

        interval = int(1000 / self.speed)
        self.root.after(interval, self.update_time)

    def elevator_display(self):
        display_frame = ttk.Labelframe(self.main_frame, text="Elevator Display", padding="10")
        display_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        self.canvas = tk.Canvas(display_frame, width=100 + (K - 1) * 100, height=600)
        self.canvas.grid(row=0, column=0)
        
        # 엘리베이터 샤프트 및 엘리베이터 그리기
        self.elevators = {}
        for i in range(K):
            self.elevators[f'EV{i+1}'] = self.canvas.create_rectangle(50 + i * 20, 500, 60 + i * 20, 510, fill="gray")
        
        # 층 그리기
        self.floor_lines = []
        for i in range(L):
            y = 500 - i * 50
            self.floor_lines.append(self.canvas.create_line(0, y, 100 + (K - 1) * 100, y))
            self.canvas.create_text(10, y - 25, text=str(i + 1))
        
        # 중간 레벨 마커 추가
        self.canvas.create_line(0, 250, 100 + (K - 1) * 100, 250, fill="purple")

    def update_elevator_positions(self):
        # 엘리베이터 시스템 상태를 기반으로 엘리베이터 위치 업데이트
        for i, elevator in enumerate(self.simulator.elevators):
            y_position = 500 - (elevator.getCurrentFloor() * 50)
            self.canvas.coords(self.elevators[f'EV{i+1}'], 50 + i * 20, y_position, 60 + i * 20, y_position + 10)
            
            # 방향 표시
            direction_symbol = "■"
            if elevator.getDirection() == UP:
                direction_symbol = "▲"
            elif elevator.getDirection() == DOWN:
                direction_symbol = "▼"
            self.canvas.create_text(55 + i * 20, y_position + 5, text=direction_symbol)
    
    def update_waiting_list(self):
        # 층별 대기 상태를 업데이트합니다.
        for widget in self.main_frame.grid_slaves():
            if int(widget.grid_info()["row"]) == 4:
                widget.grid_forget()
                
        waiting_frame = ttk.Labelframe(self.main_frame, text="Waiting List", padding="10")
        waiting_frame.grid(row=4, column=0, sticky=(tk.W, tk.E))

        for i in range(L):
            waiting_up = ", ".join([str(call[0]) for call in self.simulator.waiting_list[i][UP]])
            waiting_down = ", ".join([str(call[0]) for call in self.simulator.waiting_list[i][DOWN]])
            ttk.Label(waiting_frame, text=f"Floor {i + 1} Up: {waiting_up}").grid(row=i, column=0, sticky=tk.W)
            ttk.Label(waiting_frame, text=f"Floor {i + 1} Down: {waiting_down}").grid(row=i, column=1, sticky=tk.W)

    def passengers_display(self):
        passenger_frame = ttk.Labelframe(self.main_frame, text="Current Passengers", padding="10")
        passenger_frame.grid(row=2, column=0, sticky=(tk.W, tk.E))
        
        self.passenger_labels = []
        for i in range(K):
            label = ttk.Label(passenger_frame, text=f"EV {i+1}: ", width=50)
            label.grid(row=i, column=0, sticky=tk.W)
            self.passenger_labels.append(label)
        
        # 승객 데이터 초기 업데이트
        self.update_passenger_info()

    def update_passenger_info(self):
        for i, elevator in enumerate(self.simulator.elevators):
            passengers = [floor for floor in elevator.getCalledList()]
            self.passenger_labels[i].config(text=f"EV {i+1}: {', '.join(map(str, passengers))}")

if __name__ == "__main__":
    root = tk.Tk()
    app = ElevatorSimulatorGUI(root)
    root.mainloop()
