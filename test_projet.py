from maxpar import Task, TaskSystem
import time

A, B, C = 0, 0, 0

def f1():
    global A
    time.sleep(0.1)
    A = 10

def f2():
    global B
    time.sleep(0.1)
    B = 20

def f_somme():
    global A, B, C
    C = A + B


t1 = Task(); t1.name = "T1"; t1.writes = ["A"]; t1.run = f1
t2 = Task(); t2.name = "T2"; t2.writes = ["B"]; t2.run = f2
t3 = Task(); t3.name = "Somme"; t3.reads = ["A", "B"]; t3.writes = ["C"]; t3.run = f_somme

# Système
systeme = TaskSystem([t1, t2, t3], {"T1": [], "T2": [], "Somme": ["T1", "T2"]})

# --- APPELS M3 ---
systeme.draw()          # ici c les flèches
systeme.parCost()       # chrono
systeme.detTestRnd(globals()) # chiffre (on peut en mettre au hasard pour tester si ça marche)