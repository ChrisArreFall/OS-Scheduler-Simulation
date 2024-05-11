from Scheduler import Scheduler
def init(alg = "EDF"):
    global algorithm
    global scheduler
    global time
    global gui
    algorithm = alg
    scheduler = Scheduler(algorithm)
    time = 0
    gui = True

