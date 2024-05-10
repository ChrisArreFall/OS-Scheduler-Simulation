import os
import sys
import plotly.offline

import plotly.figure_factory as ff
import pandas as pd

from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QUrl
from PyQt5 import QtWebEngineWidgets


class PlotDialog(QtWebEngineWidgets.QWebEngineView):
    def __init__(self, data, exec=True):
        # Create a QApplication instance or use the existing one if it exists
        self.app = QApplication.instance() if QApplication.instance() else QApplication(sys.argv)
        
        super().__init__()

        self.setGeometry(800, 100, 800, 650)

        fig = ff.create_gantt(data, title='Task Scheduling', index_col='Task', show_colorbar=True, showgrid_y=True)
        fig.update_xaxes(title_text='Time', showgrid=True, type='linear')

        self.file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "temp.html"))
        plotly.offline.plot(fig, filename=self.file_path, auto_open=False)
        self.load(QUrl.fromLocalFile(self.file_path))
        self.setWindowTitle('Task Scheduling')

        if exec:
            self.app.exec_()

    def closeEvent(self, event):
        os.remove(self.file_path)