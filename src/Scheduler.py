import globals
import matplotlib.pyplot as plt
from matplotlib import cm

class Scheduler:
    def __init__(self, scheduling_algorithm):
        self.tasks = []
        self.scheduling_algorithm = scheduling_algorithm
        self.timeline = []
        self.total_time = 0  # total simulated time
        self.execution_periods = {}

    def add_task(self, task):
        self.tasks.append(task)

    def run(self):
        if self.scheduling_algorithm == 'EDF':
            return self.run_edf()
        elif self.scheduling_algorithm == 'RMS':
            return self.run_rms()
        else:
            raise ValueError("Unsupported scheduling algorithm")

    def run_edf(self):
        # Initialize task info
        task_info = {
            task.process_id: {
                'remaining': task.t,
                'next_deadline': task.d,
                'period_start': 0
            } for task in self.tasks
        }
        
        self.timeline = ['idle'] * globals.time
        self.total_time = globals.time

        # Check if tasks are schedulable for EDF
        utilization, schedulable = self.check_schedulability()
        print(f"Utilization rate: {utilization}:")
        if not schedulable:
            print("These tasks are not schedulable!")
            return
        
        # for each time unit in the total time
        for current_time in range(self.total_time):
            # Prepare list of tasks that can run
            ready_tasks = [task for task in self.tasks if task_info[task.process_id]['remaining'] > 0]

            # Sort tasks based on the deadline, 'inf' deadlines get the lowest priority
            ready_tasks.sort(key=lambda x: (task_info[x.process_id]['next_deadline'] if task_info[x.process_id]['next_deadline'] != float('inf') else self.total_time))

            # Execute the highest priority task
            if ready_tasks:
                current_task = ready_tasks[0]
                process_id = current_task.process_id
                task_info[process_id]['remaining'] -= 1
                self.timeline[current_time] = f'Process {process_id}'

                # Record execution start and end times
                if task_info[process_id]['remaining'] == current_task.t - 1:
                    task_info[process_id]['period_start'] = current_time

                if task_info[process_id]['remaining'] == 0:
                    start_time = task_info[process_id]['period_start']
                    end_time = current_time
                    if process_id not in self.execution_periods:
                        self.execution_periods[process_id] = []
                    self.execution_periods[process_id].append([start_time, end_time])
                    # Reset the task if it's not aperiodic (has a finite period)
                    if current_task.p != float('inf'):
                        task_info[process_id]['next_deadline'] += current_task.p
                        task_info[process_id]['remaining'] = current_task.t
            else:
                self.timeline[current_time] = 'idle'
        
        print("Execution periods:", self.execution_periods)
        self.plot_schedule()
        return self.execution_periods

    def run_rms(self):
        # Initialize task info
        task_info = {
            task.process_id: {
                'remaining': task.t,
                'next_deadline': 0,  # Set initial activation to time 0
                'period_start': -1,  # No active period initially
                'resumption_time': 0  # Time when the task is eligible to resume after preemption
            } for task in self.tasks
        }
        
        self.timeline = ['idle'] * globals.time
        self.total_time = globals.time
        currently_executing = None

        # Check if tasks are schedulable for RMS
        utilization, schedulable = self.check_schedulability()
        print(f"Utilization rate: {utilization}:")
        if not schedulable:
            print("These tasks are not schedulable!")
            return
        
        # for each time unit in the total time
        for current_time in range(self.total_time):
            # Prepare list of tasks that can run
            ready_tasks = [task for task in self.tasks if task_info[task.process_id]['remaining'] > 0 and current_time >= task_info[task.process_id]['resumption_time']]

            # Sort tasks based on their period; shorter period means higher priority
            ready_tasks.sort(key=lambda x: x.p)

            if ready_tasks:
                current_task = ready_tasks[0]
                process_id = current_task.process_id

                # Check if a higher priority task preempts the current one
                if currently_executing is None or process_id != currently_executing:
                    # Manage preempted task
                    if currently_executing is not None and task_info[currently_executing]['remaining'] > 0:
                        task_info[currently_executing]['resumption_time'] = current_time

                    currently_executing = process_id
                    # Record the new period start if the task is starting fresh
                    if task_info[process_id]['remaining'] == current_task.t:
                        task_info[process_id]['period_start'] = current_time

                task_info[process_id]['remaining'] -= 1
                self.timeline[current_time] = f'Process {process_id}'

                if task_info[process_id]['remaining'] == 0:
                    start_time = task_info[process_id]['period_start']
                    end_time = current_time
                    if process_id not in self.execution_periods:
                        self.execution_periods[process_id] = []
                    self.execution_periods[process_id].append([start_time, end_time])
                    # Reset the task for the next period
                    task_info[process_id]['next_deadline'] = current_time + current_task.p
                    task_info[process_id]['remaining'] = current_task.t
                    task_info[process_id]['resumption_time'] = current_time + current_task.p  # Make it eligible for its next period
                    currently_executing = None  # No task is executing now
            else:
                self.timeline[current_time] = 'idle'
                currently_executing = None  # Ensure that when idle, no task is considered running
        
        print("Execution periods:", self.execution_periods)
        self.plot_schedule()
        return self.execution_periods

    def generate_plot_data(self):
        plot_data = []
        for process_id, periods in self.execution_periods.items():
            for period in periods:
                start_time, end_time = period
                plot_data.append({
                    'Task': f'Process {process_id}',
                    'Start': start_time,
                    'Finish': end_time,
                    'Duration': end_time - start_time
                })
        return plot_data

    def plot_schedule(self):
        plot_data = self.generate_plot_data()
        _, ax = plt.subplots(figsize=(10, 5))
        yticks = []
        yticklabels = []
        unique_process_ids = sorted(set(task['Task'] for task in plot_data))
        color_map = cm.get_cmap('tab20', len(unique_process_ids))
        color_index_map = {pid: idx for idx, pid in enumerate(unique_process_ids)}

        for i, task in enumerate(plot_data):
            color = color_map(color_index_map[task['Task']] % len(color_map.colors))
            ax.broken_barh([(task['Start'], task['Duration'])], (i * 10, 9), facecolors=(color))
            yticks.append(i * 10 + 5)
            yticklabels.append(task['Task'])

        ax.set_yticks(yticks)
        ax.set_yticklabels(yticklabels)
        ax.set_xlabel('Time')
        ax.set_ylabel('Tasks')
        ax.set_title('Task Execution Schedule')
        plt.show()

    def report_statistics(self):
        task_stats = {task.process_id: {'executed': 0, 'missed_deadlines': 0, 'not_executed': 0} for task in self.tasks}
        for i, entry in enumerate(self.timeline):
            if entry != 'idle':
                process_id = int(entry.split()[1])
                task_stats[process_id]['executed'] += 1
            for task in self.tasks:
                if i >= task.d and task.t > 0:  # Check for missed deadline
                    task_stats[task.process_id]['missed_deadlines'] += 1
                    task.t = 0  # Assume task cannot execute after deadline missed

        for task in self.tasks:
            task_stats[task.process_id]['not_executed'] = self.total_time - task_stats[task.process_id]['executed']
        
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

    def check_schedulability(self):
        utilization = sum(task.t / task.p for task in self.tasks if task.p != float('inf'))
        n = len([task for task in self.tasks if task.p != float('inf')])  # Count only periodic tasks

        if globals.algorithm == 'RMS':
            bound = n * (2 ** (1 / n) - 1)
        elif globals.algorithm == 'EDF':
            bound = 1

        schedulable = utilization <= bound
        return utilization, schedulable