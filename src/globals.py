from Scheduler import Scheduler
def init(alg = "EDF"):
    global algorithm
    global scheduler

    algorithm = alg
    scheduler = Scheduler(algorithm)

