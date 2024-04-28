import sys
from Tarea import Tarea
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QListWidget, QLabel, QLineEdit, QApplication, QPushButton, QFormLayout
import globals

globals.init()

class GUI(QWidget):
    def __init__(self, args):
        super().__init__()
        self.args = args
        self.init_scheduler()
        self.init_ui()

    def init_scheduler(self):
        # Initialize the scheduler with algorithm
        globals.init(self.args.algorithm)

    def init_ui(self):
        self.setWindowTitle('Task Scheduler GUI')
        self.setGeometry(100, 100, 600, 400)
        main_layout = QVBoxLayout()
        form_layout = QFormLayout()
        self.process_id_input = QLineEdit()
        self.p_input = QLineEdit()
        self.d_input = QLineEdit()
        self.t_input = QLineEdit()
        form_layout.addRow(QLabel('Process ID:'), self.process_id_input)
        form_layout.addRow(QLabel('Period (p):'), self.p_input)
        form_layout.addRow(QLabel('Deadline (d):'), self.d_input)
        form_layout.addRow(QLabel('Execution Time (t):'), self.t_input)
        self.tasks_list = QListWidget()
        self.add_task_btn = QPushButton('Add Task')
        self.add_task_btn.clicked.connect(self.add_task)
        self.start_scheduler_btn = QPushButton('Start Scheduler')
        self.start_scheduler_btn.clicked.connect(self.start_scheduler)
        self.stats_btn = QPushButton('Show Statistics')
        self.stats_btn.clicked.connect(self.show_stats)
        main_layout.addLayout(form_layout)
        main_layout.addWidget(self.add_task_btn)
        main_layout.addWidget(self.tasks_list)
        main_layout.addWidget(self.start_scheduler_btn)
        main_layout.addWidget(self.stats_btn)

        self.setLayout(main_layout)

    def add_task(self):
        process_id = int(self.process_id_input.text())
        p = int(self.p_input.text())
        d = int(self.d_input.text())
        t = int(self.t_input.text())

        # Create task
        new_task = Tarea(process_id, p, d, t)
        # Add task
        globals.scheduler.add_task(new_task)

        self.tasks_list.addItem(f'ID: {process_id}, p: {p}, d: {d}, t: {t}')

        # printing to verify input
        print(f'Added task: Process ID={process_id}, p={p}, d={d}, t={t}')

    def start_scheduler(self):
        print("Scheduler started...")

    def show_stats(self):
        print("Displaying statistics...")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = GUI()
    ex.show()
    sys.exit(app.exec_())



