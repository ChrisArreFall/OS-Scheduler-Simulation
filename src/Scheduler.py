import globals

class Scheduler:
    def __init__(self, scheduling_algorithm='EDF'):
        self.tasks = []
        self.scheduling_algorithm = scheduling_algorithm
        self.timeline = []  #  execution details per time unit
        self.total_time = 0  # total simulated time

    def add_task(self, task):
        self.tasks.append(task)

    def check_schedulability(self):
        utilization = sum(task.t / task.p for task in self.tasks if task.p != float('inf'))
        n = len([task for task in self.tasks if task.p != float('inf')])  # Count only periodic tasks

        if globals.algorithm == 'RMS':
            bound = n * (2 ** (1 / n) - 1)
        elif globals.algorithm == 'EDF':
            bound = 1

        schedulable = utilization <= bound
        return utilization, schedulable

    def run(self):
        self.total_time = globals.time
        self.timeline = ['idle'] * globals.time 

        utilization, schedulable = self.check_schedulability()
        print(f"Utilization rate: {utilization}:")
        if not schedulable:
            print("These tasks are not schedulable!")
            return
        for current_time in range(globals.time):
            if self.scheduling_algorithm == 'EDF':
                # Filter tasks that can still run
                active_tasks = [task for task in self.tasks if task.t > 0 and current_time < task.d]
                # Sort tasks deadline, then treat aperiodic tasks (p == inf) with lower priority unless the deadline is the same
                active_tasks.sort(key=lambda x: (x.d, x.p if x.p != float('inf') else float('inf')))

            elif self.scheduling_algorithm == 'RMS':
                # Filter tasks that can still run
                active_tasks = [task for task in self.tasks if task.t > 0]
                # Sort tasks by period.
                active_tasks.sort(key=lambda x: x.p)

            if active_tasks:
                task = active_tasks[0]
                task.t -= 1
                self.timeline[current_time] = f'Process {task.process_id}'
            else:
                self.timeline[current_time] = 'idle'

    def report_statistics(self):
        task_stats = {task.process_id: {'executed': 0, 'missed_deadlines': 0, 'not_executed': 0} for task in self.tasks}
        for i, entry in enumerate(self.timeline):
            if entry != 'idle':
                process_id = int(entry.split()[1])
                task_stats[process_id]['executed'] += 1
            for task in self.tasks:
                if i >= task.d and task.t > 0:  # Check for missed deadline
                    task_stats[task.process_id]['missed_deadlines'] += 1
                    task.t = 0  # Assumir task cannot execute after deadline missed

        for task in self.tasks:
            task_stats[task.process_id]['not_executed'] = self.total_time - task_stats[task.process_id]['executed']
        
        # print statistics
        print("Scheduler Execution Statistics:")
        for process_id, stats in task_stats.items():
            executed_percent = (stats['executed'] / self.total_time) * 100
            missed_percent = (stats['missed_deadlines'] / self.total_time) * 100
            not_executed_percent = 100 - executed_percent
            print(f"Process {process_id}:")
            print(f"  Executed {stats['executed']} times ({executed_percent:.2f}%)")
            print(f"  Missed Deadlines {stats['missed_deadlines']} ({missed_percent:.2f}%)")
            print(f"  Not Executed {stats['not_executed']} times ({not_executed_percent:.2f}%)")
        return task_stats


