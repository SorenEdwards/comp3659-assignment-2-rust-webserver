import requests
import csv
import sys
import time
import numpy

from threading import Thread
from datetime import datetime

from matplotlib.backends.qt_compat import QtWidgets
from matplotlib.backends.backend_qtagg import (
    FigureCanvas, NavigationToolbar2QT as NavigationToolbar)
from matplotlib.figure import Figure


URL = "http://127.0.0.1:8080/sleep"

def send_request(threadpool_size,out_of,number,list):
    start_time = datetime.now()
    r = requests.get(url=URL)
    end_time = datetime.now()
 #   print("Duration for request number {} with response {} TIME: {}".format(number, r.status_code, (end_time - start_time).microseconds))
    list.append([threadpool_size,out_of, number, r.status_code, end_time, start_time])

def threaded_send_requests(threadpool_size,ran,list):
    threads = []
    for n in range(ran):
        t = Thread(target=send_request,args=(threadpool_size,ran,n,list,))
        t.start()
        threads.append(t)

    for t in threads:
        t.join()    

def save_results(filename,fields,results):
    with open(filename, 'w') as f:
        write = csv.writer(f)
        write.writerow(fields)
        write.writerows(results)

        
class ApplicationWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self._main = QtWidgets.QWidget()
        self.setCentralWidget(self._main)
        layout = QtWidgets.QVBoxLayout(self._main)  
        dialog = QtWidgets.QFileDialog(self)
        dialog.setFileMode(QtWidgets.QFileDialog.ExistingFiles)
        dialog.setWindowTitle("Selected the collected file(s)")
        dialog.setNameFilter(self.tr("Comma Seperated Files (*.csv)"))
        dialog.setViewMode(QtWidgets.QFileDialog.Detail)
        self._files = None
        if dialog.exec_() == QtWidgets.QDialog.Accepted:
            self._files = dialog.selectedFiles()
        if self._files:
            self.fname = str( self._files[0])
            
        print(self._files)
        print(self.fname)

        # if single file selected create plots for:
        if len(self._files) < 1:
            print("No file seleceted")
        elif len(self._files) > 9:
            print("Select less files")
        else:
            if len(self._files) == 1:
                print("single file:")
            else:
                print("multi-file type")

        # if comparison files selected create plots for:

        static_canvas = FigureCanvas(Figure(figsize=(5, 3)))
        layout.addWidget(NavigationToolbar(static_canvas, self))
        layout.addWidget(static_canvas)


        dynamic_canvas = FigureCanvas(Figure(figsize=(5, 3)))
        layout.addWidget(dynamic_canvas)
        layout.addWidget(NavigationToolbar(dynamic_canvas, self))

        self._static_ax = static_canvas.figure.subplots()
        t = numpy.linspace(0, 10, 501)
        self._static_ax.plot(t, numpy.tan(t), ".")

        self._dynamic_ax = dynamic_canvas.figure.subplots()
        t = numpy.linspace(0, 10, 101)
        # Set up a Line2D.
        self._line, = self._dynamic_ax.plot(t, numpy.sin(t + time.time()))
        self._timer = dynamic_canvas.new_timer(50)
        self._timer.add_callback(self._update_canvas)
        self._timer.start()
    
    def _update_canvas(self):
        t = numpy.linspace(0, 10, 101)
        # Shift the sinusoid as a function of time.
        self._line.set_data(t, numpy.sin(t + time.time()))
        self._line.figure.canvas.draw()

    def _file_canvas(self):
        dialog = QtWidgets.QFileDialog(self)
        dialog.setFileMode(QtWidgets.QFileDialog.AnyFile)
        dialog.setNameFilter(self.tr("Comma Seperated Files (*.csv)"))
        dialog.setViewMode(QtWidgets.QFileDialog.Detail)
        if dialog.exec_():
            self._files = dialog.selectedFiles()


if __name__ == "__main__":   
    filename = "SERVER_TEST"
    LOW = 10
    MED = 100
    HIH= 1000
    if len(sys.argv) > 1 and len(sys.argv) < 3: 
        # filename = sys.argv[1]
        threadpool_size = sys.argv[1]
    elif len(sys.argv) > 4:
        # filename = sys.argv[1]
        threadpool_size = sys.argv[1]
        LOW = int(sys.argv[2])
        MED = int(sys.argv[3])
        HIH = int(sys.argv[4])
    
    message_str = "Starting Tests"
    user_provided_filename = "User Provided Filename: {}".format(filename)
    filename = "{}_{}_{}_{}_{}.{}".format(filename,threadpool_size,LOW,MED,HIH, "csv")
    created_filename = "Filename will be: {}".format(filename)
    choosen_threadpool_size = "Threadpool size of tested server: {}".format(threadpool_size)
    choosen_low = "LOW RANGE TEST (amount of threaded requests to be sent): {}".format(LOW)
    choosen_med = "MED RANGE TEST (amount of threaded requests to be sent): {}".format(MED)
    choosen_high = "HIGH RANGE TEST (amount of threaded requests to be sent): {}".format(HIH)

    start_str = "{}\n{}\n{}\n".format(message_str,user_provided_filename,created_filename)
    choosen_ranges = "{}\n{}\n{}\n{}\n".format(choosen_threadpool_size,choosen_low,choosen_med,choosen_high)
    info_str = start_str + choosen_ranges 
    print(info_str + "\nSTARTING TEST COLLECTION\n")
    RANGES = [10,100,1000]
    FIELDS = ['THREAD_POOL_SIZE','RANGE OF', 'REQUEST', 'NUMBER', 'STATUS CODE', 'END_TIME', 'START_TIME']
    results = []
    for n in RANGES:
        threaded_send_requests(threadpool_size,n,results)
    print("saving results")
    save_results(filename,FIELDS,results)
    print(info_str + "\nStarting Data Analysis\n")
    qapp = QtWidgets.QApplication.instance()
    if not qapp:
        qapp = QtWidgets.QApplication(sys.argv)

    app = ApplicationWindow()
    app.show()
    app.activateWindow()
    app.raise_()
    qapp.exec()