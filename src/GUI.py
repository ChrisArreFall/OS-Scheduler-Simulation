import sys
from Tarea import Tarea
from StatsDialog import StatsDialog
from HelpDialog import HelpDialog
from PyQt5.QtWidgets import QWidget, QComboBox, QVBoxLayout, QListWidget, QLabel, QLineEdit, QApplication, QPushButton, QFormLayout, QGraphicsView, QGraphicsScene
from PyQt5.QtCore import Qt
import globals

globals.init()

class GUI(QWidget):
    def __init__(self):
        super().__init__()
        self.tasks = []
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Task Scheduler GUI')
        self.setGeometry(100, 100, 800, 600)
        main_layout = QVBoxLayout()
        form_layout = QFormLayout()
        self.time_input = QLineEdit()
        self.process_id_input = QLineEdit()
        self.p_input = QLineEdit()
        self.d_input = QLineEdit()
        self.t_input = QLineEdit()

        # Variables
        form_layout.addRow(QLabel('Time:'), self.time_input)
        form_layout.addRow(QLabel('Process ID:'), self.process_id_input)
        form_layout.addRow(QLabel('Period (p):'), self.p_input)
        form_layout.addRow(QLabel('Deadline (d):'), self.d_input)
        form_layout.addRow(QLabel('Execution Time (t):'), self.t_input)

        #Algorithm selection
        self.algorithm_selector = QComboBox()
        self.algorithm_selector.addItems(["EDF", "RMS"])
        form_layout.addRow(QLabel('Scheduling Algorithm:'), self.algorithm_selector)

        # buttons
        self.tasks_list = QListWidget()
        self.add_task_btn = QPushButton('Add Task')
        self.add_task_btn.clicked.connect(self.add_task)
        self.start_scheduler_btn = QPushButton('Start Scheduler')
        self.start_scheduler_btn.clicked.connect(self.start_scheduler)
        self.stats_btn = QPushButton('Show Statistics')
        self.stats_btn.clicked.connect(self.show_stats)
        self.help_btn = QPushButton('Show Help')
        self.help_btn.clicked.connect(self.show_help)

        # timeline
        self.scene = QGraphicsScene()
        self.view = QGraphicsView(self.scene)
        self.view.setFixedSize(600, 200)
        self.view.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.view.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        main_layout.addLayout(form_layout)
        main_layout.addWidget(self.add_task_btn)
        main_layout.addWidget(self.tasks_list)
        main_layout.addWidget(self.start_scheduler_btn)
        main_layout.addWidget(self.stats_btn)
        main_layout.addWidget(self.help_btn)

        self.setLayout(main_layout)

    def add_task(self):
        process_id = int(self.process_id_input.text())
        p = float('inf') if self.p_input.text() == 'inf' else int(self.p_input.text())
        d = int(self.d_input.text())
        t = int(self.t_input.text())

        # Create task
        new_task = Tarea(process_id, p, d, t)
        # Add task
        self.tasks.append(new_task)
        self.tasks_list.addItem(f'ID: {process_id}, p: {p}, d: {d}, t: {t}')

        # printing to verify input
        print(f'Added task: Process ID={process_id}, p={p}, d={d}, t={t}')

    def start_scheduler(self):
        algorithm = self.algorithm_selector.currentText()
        globals.init(algorithm)
        globals.time = int(self.time_input.text())
        print(globals.time)
        for task in self.tasks:
            globals.scheduler.add_task(task)
        globals.scheduler.run()


    def show_stats(self):
        stats = globals.scheduler.report_statistics()
        self.stats_dialog = StatsDialog(stats)
        self.stats_dialog.show()

    def show_help(self):
        self.help_dialog = HelpDialog()
        self.help_dialog.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = GUI()
    ex.show()
    sys.exit(app.exec_())



