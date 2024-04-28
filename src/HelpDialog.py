from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton

class HelpDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.init_UI()

    def init_UI(self):
        layout = QVBoxLayout()

        # Add explanations for each parameter
        layout.addWidget(QLabel("Number of Processes: The total number of processes in the simulation."))
        layout.addWidget(QLabel("Type of Synchronization: Determines how send and receive operations are synchronized."))
        layout.addWidget(QLabel("Message Format: Specifies the format of messages (fixed length, variable length, etc.)."))
        layout.addWidget(QLabel("Type of Queue: Defines the queueing strategy (FIFO, Priority, etc.)."))
        layout.addWidget(QLabel("Type of Addressing: Determines how messages are addressed (Direct, Indirect Static, Indirect Dynamic)."))

        # Add a close button
        close_button = QPushButton("Close")
        close_button.clicked.connect(self.close)
        layout.addWidget(close_button)

        self.setLayout(layout)
        self.setWindowTitle("Help - Parameter Explanations")