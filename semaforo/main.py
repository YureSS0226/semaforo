from machine import Pin, ADC, mem32
from time import sleep

# salidas digitales
GPIO = const(0x3FF44004)
vectorPines = [4, 2, 15, 19, 18, 5, 26, 25, 12, 23, 22, 14, 27]
for i in range(0, 13):
    Pin(vectorPines[i], Pin.OUT)

# entradas digitales
btnSw = Pin(32, Pin.IN, Pin.PULL_DOWN)
btnTemp = Pin(35, Pin.IN, Pin.PULL_DOWN)

# sensor temperatura
temp = ADC(Pin(34))
temp.atten(ADC.ATTN_11DB)
temp.width(ADC.WIDTH_10BIT)

# variables
estado = 0
bandera = 0
datoTemp = 0
valorTemp = 0.0

# tiempos
t1 = 4
t2 = 2
t3 = 4

# Interrupciones
def cambiarModoSemaforo(pin):
    global estado
    if estado == 0:
        print("Esperando modo 2 semaforo...")
        estado = 1
    else:
        print("Modo 1 semaforo")
        estado = 0
        
btnSw.irq(handler=cambiarModoSemaforo, trigger=Pin.IRQ_RISING)

def cambiarModoTemperatura(pin):
    global bandera
    if bandera == 0:
        print("Esperando modo temperatura...")
        bandera = 1
    else:
        print("Modo semaforo")
        bandera = 0
        
btnTemp.irq(handler=cambiarModoTemperatura, trigger=Pin.IRQ_RISING)

# leds apagados
mem32[GPIO] = 0B00000000000000000000000000000000

while True:
    if bandera == 0:
        if estado == 0:
            mem32[GPIO] = 0B00000100100000000100000000110000
            sleep(t1)
            for i in range(3):
                mem32[GPIO] = 0B00000100100000000100000000010000
                sleep(0.5)
                mem32[GPIO] = 0B00000100100000000100000000110000
                sleep(0.5)
            mem32[GPIO] = 0B00000100100001000100000000010000
            sleep(3)
            mem32[GPIO] = 0B00001100010010000000000000010000
            sleep(t2)
            for i in range(3):
                mem32[GPIO] = 0B00000100010010000000000000010000
                sleep(0.5)
                mem32[GPIO] = 0B00001100010010000000000000010000
                sleep(0.5)
            mem32[GPIO] = 0B00000000010010001101000000000000
            sleep(t3)
            for i in range(3):
                mem32[GPIO] = 0B00000000010010000100000000000000
                sleep(0.5)
                mem32[GPIO] = 0B00000000010010001101000000000000
                sleep(0.5)
            mem32[GPIO] = 0B00000010010010000100000000000100
            for i in range(3):
                mem32[GPIO] = 0B00000010000010000100000000000100
                sleep(0.5)
                mem32[GPIO] = 0B00000010010010000100000000000100
                sleep(0.5)
        elif estado == 1:
            mem32[GPIO] = 0B00001100010010000000000000010000
    else:
        mem32[GPIO] = 0B00000000000000000000000000000000
        datoTemp = temp.read()
        valorTemp = (datoTemp * (5/1023))/0.1
        print(valorTemp)
        sleep(1)