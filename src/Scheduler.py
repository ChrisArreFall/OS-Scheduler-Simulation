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
                'next_deadline': task.t,
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
                'resumption_time': 0,  # Time when the task is eligible to resume after preemption
                'started': False
            } for task in self.tasks
        }
        
        print("Initial task info:", task_info)
        
        self.timeline = ['idle'] * globals.time
        self.total_time = globals.time
        currently_executing = None

        # Check if tasks are schedulable for RMS
        utilization, schedulable = self.check_schedulability()
        print(f"Utilization rate: {utilization}:")
        #if not schedulable:
        #    print("These tasks are not schedulable!")
        #    return
        
        # for each time unit in the total time
        for current_time in range(self.total_time):
            # Prepare list of tasks that can run
            ready_tasks = [task for task in self.tasks if task_info[task.process_id]['remaining'] > 0 and current_time >= task_info[task.process_id]['resumption_time']]
            print(f"Ready tasks at time {current_time}: {[task.process_id for task in ready_tasks]}")

            # Sort tasks based on their period; shorter period means higher priority
            ready_tasks.sort(key=lambda x: x.p)
            print(f"Sorted tasks at time {current_time}: {[task.process_id for task in ready_tasks]}")

            if ready_tasks:
                current_task = ready_tasks[0]
                process_id = current_task.process_id

                # Check if a higher priority task preempts the current one
                if currently_executing is None or process_id != currently_executing:
                    if currently_executing is not None and task_info[currently_executing]['remaining'] > 0:
                        #task_info[currently_executing]['resumption_time'] = current_time
                        print(f"Task {currently_executing} preempted by Task {process_id} at time {current_time}")

                    currently_executing = process_id
                    # Record the new period start if the task is starting fresh
                    if task_info[process_id]['remaining'] == current_task.t:
                        task_info[process_id]['period_start'] = current_time

                task_info[process_id]['remaining'] -= 1
                self.timeline[current_time] = f'Process {process_id}'
                if not task_info[process_id]['started']:
                    task_info[process_id]['resumption_time'] = current_time
                    task_info[process_id]['started'] = True
                print(f"Executing Task {process_id}, Remaining time {task_info[process_id]['remaining']}")

                if task_info[process_id]['remaining'] == 0:
                    start_time = task_info[process_id]['period_start']
                    end_time = current_time
                    if process_id not in self.execution_periods:
                        self.execution_periods[process_id] = []
                    self.execution_periods[process_id].append([start_time, end_time])
                    # Reset the task for the next period
                    task_info[process_id]['next_deadline'] = current_time + (current_task.p - current_task.t)
                    task_info[process_id]['remaining'] = current_task.t
                    task_info[process_id]['resumption_time'] += current_task.p  # Make it eligible for its next period
                    currently_executing = None  # No task is executing now
                    print(f"Task {process_id} completed, resetting for next period starting at {task_info[process_id]['resumption_time']}")
            else:
                self.timeline[current_time] = 'idle'
                currently_executing = None  # Ensure that when idle, no task is considered running
                print(f"System idle at time {current_time}")

        print("Execution periods:", self.execution_periods)
        self.plot_schedule()
        return self.execution_periods

    def plot_schedule(self):
        # Define custom colors for clarity
        task_color_map = {
            'Process 1': 'blue',
            'Process 2': 'yellow',
            'Process 3': 'green',
            'Process 4': 'cyan',
            'Process 5': 'purple',
            'Process 6': 'orange',
            'Process 7': 'pink',
            'Process 8': 'lime',
            'Process 9': 'magenta',
            'idle': 'red'
        }
        plot_data = self.generate_plot_data()
        _, ax = plt.subplots(figsize=(10, 3))  # Reduce vertical size since it's a single line

        # Track colors actually used in the plot
        used_colors = {}

        # Create the timeline as a single line
        for task in plot_data:
            task_id = task['Task']
            color = task_color_map.get(task_id, 'gray')  # Default to gray if not specified
            if task_id not in used_colors:  # Add task and color to used_colors if it's not already there
                used_colors[task_id] = color
            start = task['Start']
            finish = task['Finish']
            ax.hlines(1, start, finish, colors=color, linewidth=10)  # Y=1, constant line with width 10

        # Remove y-axis and spines since they are not necessary
        ax.yaxis.set_visible(False)
        ax.spines['left'].set_visible(False)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)

        # Set the x-axis labels and title
        ax.set_xlabel('Time')
        ax.set_title('Task Execution Schedule')

        # Create a custom legend from the colors actually used
        custom_lines = [plt.Line2D([0], [0], color=used_colors[task], lw=4) for task in used_colors]
        ax.legend(custom_lines, [task for task in used_colors])

        plt.show()


    def generate_plot_data(self):
        last_task = self.timeline[0]
        start_time = 0
        plot_data = []

        for i, entry in enumerate(self.timeline):
            print(i,entry)
            if entry != last_task:
                plot_data.append(dict(Task=last_task, Start=start_time, Finish=i))
                last_task = entry
                start_time = i

        # Add last task
        plot_data.append(dict(Task=last_task, Start=start_time, Finish=len(self.timeline)))
        return plot_data
    
    def report_statistics(self):
        task_stats = {task.process_id: {'executed': 0, 'missed_deadlines': 0, 'not_executed': 0} for task in self.tasks}
        for i, entry in enumerate(self.timeline):
            print(entry)
            if entry != 'idle':
                process_id = int(entry.split()[1])
                task_stats[process_id]['executed'] += 1
            for task in self.tasks:
                if i >= task.t and task.t > 0:  # Check for missed deadline
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