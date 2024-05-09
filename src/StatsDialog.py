from PyQt5.QtWidgets import QDialog, QTextEdit, QVBoxLayout
import globals

class StatsDialog(QDialog):
    def __init__(self, stats, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Task Statistics")
        self.setGeometry(100, 100, 400, 300)
        self.init_ui(stats)
    
    def init_ui(self, stats):
        layout = QVBoxLayout()
        text_edit = QTextEdit()
        text_edit.setReadOnly(True)
        display_text = "Scheduler Execution Statistics:\n"
        for process_id, data in stats.items():
            executed_percent = (data['executed'] / globals.scheduler.total_time) * 100
            missed_percent = (data['missed_deadlines'] / globals.scheduler.total_time) * 100
            not_executed_percent = 100 - executed_percent
            display_text += (f"Process {process_id}:\n"
                             f"  Executed {data['executed']} times ({executed_percent:.2f}%)\n"
                             f"  Missed Deadlines {data['missed_deadlines']} ({missed_percent:.2f}%)\n"
                             f"  Not Executed {data['not_executed']} times ({not_executed_percent:.2f}%)\n\n")
        text_edit.setText(display_text)
        layout.addWidget(text_edit)
        self.setLayout(layout)
