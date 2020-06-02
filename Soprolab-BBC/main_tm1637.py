from microbit import *
from tm1637 import *

tm = TM1637(clk=pin1, dio=pin2)

num = 0
tm.number(num)

while not(button_a.is_pressed() and button_b.is_pressed()):
    if button_a.was_pressed():
        num = num + 1
        tm.number(num)
    elif button_b.was_pressed():
        num = num - 1
        tm.number(num)


