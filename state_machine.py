# event ( 종류 문자열, 실제 값 )
from sdl2 import *


def space_down(e):
    return e[0]=='INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_SPACE

def time_out(e):
    return e[0]=='TIME_OUT'

def start_event(e): #start 가상의 이벤트
    return e[0] == 'START'

def right_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_RIGHT

def right_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_RIGHT

def left_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_LEFT

def left_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_LEFT

def a_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_a


# 상태 머신을 처리 관리 해주는 클래스
class StateMachine:
    def __init__(self, o):
        self.o = o  #boy self가 전달, self.o 상태머신과 연결된 캐릭터 객체
        self.event_que = [] # 발생하는 이벤트를 담는 곳
        pass

    def update(self):
        self.cur_state.do(self.o) #Idle.do()

        # 이벤트가 발생했는지 확인하고, 거기에 따라서 상태변화를 수행.
        if self.event_que: # list에 요소가 있으면 list 값들은 True
            e = self.event_que.pop(0)   #list의 첫번째 요소를 꺼내

            for check_event, next_state in self.transitions[self.cur_state].items():
                if check_event(e): # e가 지금 check_event으로 들어오면? space_donw(e) ?
                    self.cur_state.exit(self.o,e)
                    print(f'EXIT from {self.cur_state}')
                    self.cur_state = next_state
                    self.cur_state.enter(self.o,e)
                    print(f'ENTER into {next_state}')
                    return
        pass

    def start(self,start_state):
        # 현재 상태를 시작 상태로 만듬.
        self.cur_state = start_state    #Idle
        self.cur_state.enter(self.o,('START',0)) # 새로운 상태로 시작 됐기 때문에, enter을 실행해야 된다.
                                                #dummy 이벤트
        print(f'ENTER into {self.cur_state}')

        pass

    def draw(self):
        self.cur_state.draw(self.o)
        pass

    def set_transitions(self, transitions):
        self.transitions = transitions
        pass

    def add_event(self, event):
        self.event_que.append(event)    #상태 머신용 이벤트 추가
        print(f'    DEBUG: new event {event} is added.')
        pass

