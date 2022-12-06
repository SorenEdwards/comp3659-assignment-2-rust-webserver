from threading import Thread
import requests
from datetime import datetime
import timeit
import time
import csv
from variables import *

# field names
fields = ['RANGE OF', 'REQUEST', 'NUMBER', 'STATUS CODE', 'END_TIME', 'START_TIME', 'TOTAL_TIME']

# data rows of csv file
URL = "http://127.0.0.1:8080/"
def send_request(range,number,list):
    start_time = time.time()
    r = requests.get(url=URL)
    end_time = time.time()
    total_time = end_time - start_time
    #print("Duration for request number {} with response {} TIME:{}".format(number, r.status_code, (end_time - start_time)))
    list.append([range,r.status_code,start_time, end_time, total_time])

def threaded_send_requests(ran,list):
    threads = []
    for n in range(ran):
        t = Thread(target=send_request,args=(ran,n,list,))
        t.start()
        threads.append(t)

    for t in threads:
        t.join()


#if name == "main":
results = []
req_times = []


for n in RANGES:
    start = time.time()
    threaded_send_requests(n,results)
    end = time.time()
    req_times.append(end-start)
    print(end-start)

with open('16thread_nosleep_times.csv', mode='w') as csv_file:
    # using csv.writer method from CSV package
    csv_writer = csv.writer(csv_file)
    #write.writerow(fields)
    csv_writer.writerow(req_times)
    csv_file.close()


with open('16thread_nosleep.csv', mode='w') as csv_file:

    # using csv.writer method from CSV package
    csv_writer = csv.writer(csv_file)

    #write.writerow(fields)
    csv_writer.writerows(results)
    csv_file.close()

