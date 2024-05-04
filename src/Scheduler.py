class Scheduler:
    def __init__(self, scheduling_algorithm='EDF'):
        self.tasks = []
        self.scheduling_algorithm = scheduling_algorithm
        self.timeline = []  #  execution details per time unit
        self.total_time = 0  # total simulated time

    def add_task(self, task):
        self.tasks.append(task)

    def run(self, total_time):
        self.total_time = total_time
        self.timeline = ['idle'] * total_time 

        for current_time in range(total_time):
            # EDF prioritizes tasks with the earliest deadlines
            if self.scheduling_algorithm == 'EDF':
                active_tasks = sorted((task for task in self.tasks if task.t > 0 and current_time < task.d), key=lambda x: x.d)
            # RMS prioritizes tasks with the lowest period
            elif self.scheduling_algorithm == 'RMS':
                active_tasks = sorted((task for task in self.tasks if task.t > 0), key=lambda x: x.p)

            if active_tasks:
                task = active_tasks[0]
                task.t -= 1
                self.timeline[current_time] = f'Process {task.process_id}'

    def report_statistics(self, gui):
        task_stats = {task.process_id: {'executed': 0, 'missed_deadlines': 0} for task in self.tasks}
        
        for i, entry in enumerate(self.timeline):
            if entry != 'idle':
                process_id = int(entry.split()[1])
                task_stats[process_id]['executed'] += 1
                if i >= next(task.d for task in self.tasks if task.process_id == process_id):
                    task_stats[process_id]['missed_deadlines'] += 1
        
        # print statistics for non GUI
        if (not gui):
            for process_id, stats in task_stats.items():
                print(f"Process {process_id}: Executed {stats['executed']} times, Missed Deadlines {stats['missed_deadlines']}")
        return task_stats


