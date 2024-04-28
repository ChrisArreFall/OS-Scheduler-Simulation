import cmd
import re
import globals
from Tarea import Tarea


class CLI(cmd.Cmd):
    intro = 'Welcome to the Scheduler CLI. Type help or ? to list commands.'
    prompt = '(scheduler) '

    def do_add(self, arg):
        'Add a new task: add process_id p d t'
        args = arg.split()
        if len(args) != 4:
            print("Invalid number of arguments. Usage: add process_id p d t")
            return
        process_id, p, d, t = map(int, args)
        globals.scheduler.add_task(Tarea(process_id, p, d, t))
        print(f"Task {process_id} added.")

    def do_run(self, arg):
        'Run the scheduler for a set number of time units: run time'
        try:
            total_time = int(arg)
            globals.scheduler.run(total_time)
            print("Scheduler run complete.")
        except ValueError:
            print("Please provide an integer for the time.")

    def do_stats(self, arg):
        'Display scheduler statistics'
        globals.scheduler.report_statistics()

    def do_exit(self, arg):
        'Exit the scheduler CLI'
        print("Exiting the scheduler CLI.")
        return True  # Return True to exit the cmd loop

    def do_EOF(self, line):
        'Exit on end-of-file (Ctrl-D)'
        return True

if __name__ == '__main__':
    globals.init()  # Initialize with default or specified algorithm
    CLI().cmdloop()

