from threading import Thread
import requests
from datetime import datetime
import csv
import sys



URL = "http://127.0.0.1:8080/sleep"

def send_request(threadpool_size,out_of,number,list):
    start_time = datetime.now()
    r = requests.get(url=URL)
    end_time = datetime.now()
    print("Duration for request number {} with response {} TIME: {}".format(number, r.status_code, (end_time - start_time).microseconds))
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
    print(info_str)
    
    RANGES = [10,100,1000]
    FIELDS = ['THREAD_POOL_SIZE','RANGE OF', 'REQUEST', 'NUMBER', 'STATUS CODE', 'END_TIME', 'START_TIME']
    results = []
    for n in RANGES:
        threaded_send_requests(threadpool_size,n,results)
    save_results(filename,FIELDS,results)
    print(info_str)
    
     


    