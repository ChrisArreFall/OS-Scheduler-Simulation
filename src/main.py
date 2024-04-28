import sys
import argparse
from PyQt5.QtWidgets import QApplication
from GUI import GUI
from CLI import CLI
import globals

globals.init()

def main():
    parser = argparse.ArgumentParser(description="Run the scheduler in GUI or CLI mode.")
    parser.add_argument("-i", "--input", help="Input file with tasks.")
    parser.add_argument("-o", "--output", help="Output file to save the results.")
    parser.add_argument("-a", "--algorithm", choices=['EDF', 'RMS'], default='EDF',
                        help="Scheduling algorithm to use (EDF or RMS).")
    parser.add_argument("-t", "--time", type=int, default=1000, help="Total time to run the scheduler.")
    parser.add_argument("-gui", "--graphical", action='store_true', help="Run in graphical mode.")

    args = parser.parse_args()

    if args.graphical:
        app = QApplication(sys.argv)
        gui = GUI(args)
        gui.show()
        sys.exit(app.exec_())
    else:
        CLI().cmdloop()

if __name__ == "__main__":
    main()

