from pico2d import load_image, get_time
import random
from state_machine import *


class Idle:
    @staticmethod
    def enter(boy,e):
        boy.start_time = get_time()     #현재 시간으 기록

        #움직이다가 멈춘 경우
        if left_up(e) or right_down(e):
            boy.action = 2
            boy.face_dir = -1
        elif right_up(e) or left_down(e) or start_event(e):
            boy.action = 3
            boy.face_dir = 1
        elif time_out(e):
            if boy.dir >0:
                boy.action = 3
                boy.face_dir = 1
            elif boy.dir < 0:
                boy.action = 2
                boy.face_dir = -1

        boy.frame = 0
        boy.dir = 0
        pass

    @staticmethod
    def exit(boy,e):
        pass

    @staticmethod
    def draw(boy):
        boy.image.clip_draw(boy.frame * 100, boy.action * 100, 100, 100, boy.x, boy.y)
        pass

    @staticmethod
    def do(boy):
        boy.frame = (boy.frame + 1) % 8
        if get_time() - boy.start_time > 5:
            #이벤트를 발생
            boy.state_machine.add_event(('TIME_OUT',0))
        pass

class Sleep:
    @staticmethod
    def enter(boy,e):

        pass
    @staticmethod
    def exit(boy,e):
        pass
    @staticmethod
    def draw(boy):
        if boy.face_dir == 1:   #오른쪽 방향
            boy.image.clip_composite_draw(boy.frame * 100, boy.action * 100, 100, 100, 3.141592 / 2, '', boy.x - 25,
                                      boy.y - 25, 100, 100)
        elif boy.face_dir == -1:    #왼쪽 방향
            boy.image.clip_composite_draw(boy.frame * 100, boy.action * 100, 100, 100, -3.141592 / 2, '', boy.x + 25,
                                      boy.y - 25, 100, 100)

        pass
    @staticmethod
    def do(boy):
        boy.frame = (boy.frame + 1) % 8

        pass

class Run:
    @staticmethod
    def enter(boy,e):
        if right_down(e) or left_up(e):  # 오른쪽으로 RUN
            boy.dir, boy.action = 1, 1
        elif left_down(e) or right_up(e):  # 왼쪽으로 RUN
            boy.dir, boy.action = -1, 0
        #두 키를 동시에 눌렀을 때를 대비
        boy.frame =0
        pass

    @staticmethod
    def exit(boy,e):
        pass

    @staticmethod
    def draw(boy):
        boy.image.clip_draw(boy.frame * 100, boy.action * 100, 100, 100, boy.x, boy.y)

        pass

    @staticmethod
    def do(boy):
        boy.frame = (boy.frame + 1) % 8

        if 0>= boy.x +boy.dir * 5:
            boy.dir =0
        elif 800<= boy.x +boy.dir * 5:
            boy.dir = 0

        boy.x += boy.dir * 5

        pass


class AutoRun:
    @staticmethod
    def enter(boy,e):
        boy.start_time = get_time()


        if boy.face_dir==1:
            boy.dir = 1
        elif boy.face_dir==-1:
            boy.dir = -1


        #두 키를 동시에 눌렀을 때를 대비
        boy.frame =0
        pass

    @staticmethod
    def exit(boy,e):
        pass

    @staticmethod
    def draw(boy):
        boy.image.clip_draw(boy.frame * 100, boy.action * 100, 100, 100, boy.x, boy.y+35,200,200)
        pass

    @staticmethod
    def do(boy):
        boy.frame = (boy.frame + 1) % 8

        if get_time() - boy.start_time > 5:
            # 이벤트를 발생
            boy.state_machine.add_event(('TIME_OUT', 0))

        if boy.dir == 1:  # 오른쪽으로 RUN
            boy.action = 1
        elif boy.dir == -1:  # 왼쪽으로 RUN
            boy.action = 0

        if boy.x>=800:
            boy.dir = -1
        elif boy.x<=0:
            boy.dir = +1

        boy.x += boy.dir * 10
        pass


class Boy:
    def __init__(self):
        self.x, self.y = 400, 90
        self.frame = 0
        self.dir = 0
        self.action = 3
        self.image = load_image('animation_sheet.png')
        self. state_machine = StateMachine(self)    #어떤 객체를 위한 상태 머신인지 알려줄 필요가 있다
        self.state_machine.start(Idle)  # 객체를 생성한게 아니고, 직접 idle 클래스를 사용

        self.state_machine.set_transitions({
            Idle: {right_down: Run, left_down: Run, left_up: Run, right_up: Run,a_down : AutoRun ,time_out: Sleep},
            Run: {right_down: Idle, left_down: Idle, right_up: Idle, left_up: Idle},
            Sleep: {right_down: Run, left_down: Run, right_up: Run, left_up: Run, space_down: Idle},
            AutoRun: {right_down: Run, left_down: Run, right_up: Run, left_up: Run, time_out: Idle}


        })

    def update(self):
        self.state_machine.update()


    def handle_event(self, event):
        self.state_machine.add_event(('INPUT',event))
        pass

    def draw(self):
        self.state_machine.draw()

