class Scheduler:
    def __init__(self, scheduling_algorithm='EDF'):
        self.tasks = []
        self.scheduling_algorithm = scheduling_algorithm
        self.time = 0

    def add_task(self, task):
        self.tasks.append(task)

    def run(self, total_time):
        timeline = []
        for time in range(total_time):
            if self.scheduling_algorithm == 'EDF':
                self.tasks.sort(key=lambda x: x.d)  # Sort by d
            elif self.scheduling_algorithm == 'RMS':
                self.tasks.sort(key=lambda x: x.p)  # Sort by p
            
            for task in self.tasks:
                if task.t > 0 and time < task.d:
                    timeline.append(f'Process {task.process_id} running at time {time}')
                    task.t -= 1
                    break

        return timeline

    def report_statistics(self):
        print("Scheduler Statistics Report:")
        for task in self.tasks:
            executed = sum(1 for t in self.timeline if t == f'Process {task.process_id}')
            missed_deadlines = sum(1 for t in self.timeline if t == f'Process {task.process_id} (missed deadline)')
            not_executed = self.total_time - executed - missed_deadlines
            print(f"Task {task.process_id}:")
            print(f"  Total Execution Periods: {executed}")
            print(f"  Missed Deadlines: {missed_deadlines}")
            print(f"  Periods Not Executed: {not_executed}")
            execution_percent = (executed / self.total_time) * 100
            print(f"  Execution Time (%): {execution_percent:.2f}%")

