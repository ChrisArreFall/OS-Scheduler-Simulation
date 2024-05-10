from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton

class HelpDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.init_UI()

    def init_UI(self):
        layout = QVBoxLayout()

        # Add explanations for each parameter
        layout.addWidget(QLabel("Period (p): The amount of time in wich a task should be regularly excecuted."))
        layout.addWidget(QLabel("Deadline (d): The time at which the task should be completed."))
        layout.addWidget(QLabel("Computation time (t): Time the CPU takes to complete the task without interruption."))
        layout.addWidget(QLabel("Statistics - Execution time: Total amount of time the task has been running, both in units of time and percentage of run time."))
        layout.addWidget(QLabel("Statistics - Missed deadlines: The number of times the task could not be completed before its deadline."))
        layout.addWidget(QLabel("Statistics - Not executed time: The time the task was not being exceuted, both in units of time and percentage of run time."))

        # Add a close button
        close_button = QPushButton("Close")
        close_button.clicked.connect(self.close)
        layout.addWidget(close_button)

        self.setLayout(layout)
        self.setWindowTitle("Help - Parameter Explanations")