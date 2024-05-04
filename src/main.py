import sys
import argparse
from PyQt5.QtWidgets import QApplication
from GUI import GUI
from Tarea import Tarea
import globals

def run_cli(args):
    # Initialize the scheduler with algorithm
    globals.init(args.algorithm)

    # Load tasks from input file
    try:
        with open(args.input, 'r') as file:
            for line in file:
                process_id, p, d, t = map(int, line.split())
                globals.scheduler.add_task(Tarea(process_id, p, d, t))
    except Exception as e:
        print(f"Failed to read tasks from {args.input}: {e}")
        sys.exit(1)

    # Run scheduler
    globals.scheduler.run(args.time)

    # Output results to specified file
    try:
        with open(args.output, 'w') as file:
            stats = globals.scheduler.report_statistics(False)
            for process_id, stats in stats.items():
                file.write(f"Process {process_id}: Executed {stats['executed']} times, Missed Deadlines {stats['missed_deadlines']}\n")
    except Exception as e:
        print(f"Failed to write results to {args.output}: {e}")
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description="Task Scheduler Application")
    parser.add_argument("-i", "--input", required=True, help="Input file with tasks.")
    parser.add_argument("-o", "--output", required=True, help="Output file to save the results.")
    parser.add_argument("-a", "--algorithm", choices=['EDF', 'RMS'], default='EDF', help="Scheduling algorithm to use (default: EDF)")
    parser.add_argument("-t", "--time", type=int, required=True, help="Total time to run the scheduler.")
    parser.add_argument("-gui", "--graphical", action='store_true', help="Run in graphical mode")
    
    args = parser.parse_args()

    if args.graphical:
        app = QApplication(sys.argv)
        gui = GUI(args)
        gui.show()
        sys.exit(app.exec_())
    else:
        run_cli(args)

if __name__ == "__main__":
    main()

