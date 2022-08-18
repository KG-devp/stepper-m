from machine import Pin
from rp2 import PIO, StateMachine, asm_pio
from time import sleep
import sys
import _thread

@asm_pio(set_init=(PIO.OUT_LOW,) * 4,
         out_init=(PIO.OUT_HIGH,) * 4,
         out_shiftdir=PIO.SHIFT_LEFT)

def prog():
    pull()
    mov(y, osr) # step pattern
    
    pull()
    mov(x, osr) # num steps
    
    jmp(not_x, "end")
    
    label("loop")
    jmp(not_osre, "step") # loop pattern if exhausted
    mov(osr, y)
    
    label("step")
    out(pins, 4) [31]
    nop() [31]
    nop() [31]
    nop() [31]

    jmp(x_dec,"loop")
    label("end")
    set(pins, 8) [31] # 8



sm0 = StateMachine(0, prog, freq=10000, set_base=Pin(2), out_base=Pin(2))
sm1 = StateMachine(1, prog, freq=10000, set_base=Pin(6), out_base=Pin(6))
sm2 = StateMachine(2, prog, freq=10000, set_base=Pin(10), out_base=Pin(10))



def StepperThread():
    sm0.active(1)
    sm0.put(2216789025) #1000 0100 0010 0001 1000010000100001
    sm0.put(1000)

    sm1.active(1)
    sm1.put(2216789025)
    sm1.put(1000)
    
    sm2.active(1)
    sm2.put(2216789025)
    sm2.put(1000)

    sleep(100)
    sm0.active(0)
    sm0.exec("set(pins,0)")
    sm1.active(0)
    sm1.exec("set(pins,0)")
    sm2.active(0)
    sm2.exec("set(pins,0)")


_thread.start_new_thread(StepperThread, ())

    
