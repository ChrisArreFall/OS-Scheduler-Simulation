from Scheduler import Scheduler
def init(alg = "EDF"):
    global algorithm
    global scheduler
    global time
    algorithm = alg
    scheduler = Scheduler(algorithm)
    time = 0

