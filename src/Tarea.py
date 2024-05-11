class Tarea:
    def __init__(self, process_id, p, d, t):
        if not isinstance(process_id, int):
            print("Error: process_id must be an integer.")
            return None
        self.process_id = process_id
        self.p = p
        self.d = d
        self.t = t
    