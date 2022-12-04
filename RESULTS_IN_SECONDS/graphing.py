from matplotlib import pyplot as plt
import numpy as np
from variables import *
import multiprocessing
import statistics as stats

plt.style.use('dark_background')

graph = int(input('What would you like to graph?\n1. Low Threads 1 Second Sleep\n2. High Threads 1 Second Sleep\n'))

def unpack_csv(filename):
    test_range,status_codes,start_time,end_time,request_leng = np.loadtxt(filename,unpack = True, delimiter= ',')

    return test_range, status_codes, start_time, end_time, request_leng

def unpack_csv_times(filename):
    req_times = np.loadtxt(filename,unpack = True, delimiter= ',')

    return req_times

#Unpacking thead csv stats into arrays
test_range4, status_codes4, start_time4, end_time4, request_length4 = unpack_csv('4thread_nosleep.csv')
test_range8, status_codes8, start_time8, end_time8, request_length8 = unpack_csv('8thread_nosleep.csv')
test_range10, status_codes10, start_time10, end_time10, request_length10 = unpack_csv('10thread_nosleep.csv')
test_range12, status_codes12, start_time12, end_time12, request_length12 = unpack_csv('12thread_nosleep.csv')
test_range13, status_codes13, start_time13, end_time13, request_length13 = unpack_csv('13thread_nosleep.csv')
test_range16, status_codes16, start_time16, end_time16, request_length16 = unpack_csv('16thread_nosleep.csv')
test_range32, status_codes32, start_time32, end_time32, request_length32 = unpack_csv('32thread_nosleep.csv')

#Unpacking thread csv times with sleep into arrays
nopool_req_times= unpack_csv_times('nothread_sleep_times.csv')
req_times1= unpack_csv_times('1thread_sleep_times.csv')
req_times2= unpack_csv_times('2thread_sleep_times.csv')
req_times4= unpack_csv_times('4thread_sleep_times.csv')
req_times8= unpack_csv_times('8thread_sleep_times.csv')
req_times16= unpack_csv_times('16thread_sleep_times.csv')
req_times32= unpack_csv_times('32thread_sleep_times.csv')
req_times64= unpack_csv_times('32thread_sleep_times.csv')
req_times256= unpack_csv_times('256thread_sleep_times.csv')
req_times512 = unpack_csv_times('512thread_sleep_times.csv')
req_times1024 = unpack_csv_times('1024thread_sleep_times.csv')
req_times2048 = unpack_csv_times('2048thread_sleep_times.csv')
req_times4096 = unpack_csv_times('4096thread_sleep_times.csv')

nosleep_req_times1= unpack_csv_times('1thread_nosleep_times.csv')
nosleep_req_times2= unpack_csv_times('2thread_nosleep_times.csv')
nosleep_req_times4= unpack_csv_times('4thread_nosleep_times.csv')
nosleep_req_times8= unpack_csv_times('8thread_nosleep_times.csv')
nosleep_req_times16= unpack_csv_times('16thread_nosleep_times.csv')




tot_times_high = [req_times1[2],req_times2[2],req_times4[2],req_times8[2],req_times16[2]]
tot_times_med = [req_times1[1],req_times2[1],req_times4[1],req_times8[1],req_times16[1]]
tot_times_low = [req_times1[0],req_times2[0],req_times4[0],req_times8[0],req_times16[0]]

nosleep_tot_times_high = [nosleep_req_times1[2],nosleep_req_times2[2],nosleep_req_times4[2],nosleep_req_times8[2],nosleep_req_times16[2]]
nosleep_tot_times_med = [nosleep_req_times1[1],nosleep_req_times2[1],nosleep_req_times4[1],nosleep_req_times8[1],nosleep_req_times16[1]]
nosleep_tot_times_low = [nosleep_req_times1[0],nosleep_req_times2[0],nosleep_req_times4[0],nosleep_req_times8[0],nosleep_req_times16[0]]

tot_times_high2 = [req_times256[2],req_times512[2],req_times1024[2],req_times2048[2],req_times4096[2]]
tot_times_med2 = [req_times256[1],req_times512[1],req_times1024[1],req_times2048[1],req_times4096[1]]
tot_times_low2 = [req_times256[0],req_times512[0],req_times1024[0],req_times2048[0],req_times4096[0]]



performance_increase1 = [req_times1[2]/req_times2[2],req_times2[2]/req_times4[2], req_times4[2]/req_times8[2],req_times8[2]/req_times16[2]]
performance_increase2 = [req_times256[2]/req_times512[2],req_times512[2]/req_times1024[2], req_times1024[2]/req_times2048[2], req_times2048[2]/req_times4096[2]]

threads = [1,2,4,8,16]
threads2 = [256,512,1024,2048,4096]
performance = ['1-2', '2-4', '4-8','8-16']
performance2 = ['256-512', '512-1024', '1024-2048', '2048-4096']


if graph == 1:
    #low threads with one second sleep graph
    x_indexes = np.arange(len(threads))
    plt.bar(x_indexes -0.25,tot_times_high, width = 0.25, label = '100 Requests')
    plt.bar(x_indexes, tot_times_med, width = 0.25, label = '50 requests')
    plt.bar(x_indexes +0.25, tot_times_low, width = 0.25, label = '25 requests')
    plt.xticks(ticks = x_indexes, labels = threads)
    plt.title('Time of Reqeusts With 1 Second Sleep')
    plt.xlabel('Threads')
    plt.ylabel('Seconds')
    plt.legend()
elif graph == 2:
    #high threads with one second sleep graph
    x_indexes = np.arange(len(threads2))
    plt.bar(x_indexes -0.25,tot_times_high2, width = 0.25, label = '25 600 Requests')
    plt.bar(x_indexes, tot_times_med2, width = 0.25, label = '12 800 requests')
    plt.bar(x_indexes +0.25, tot_times_low2, width = 0.25, label = '6400 requests')
    plt.xticks(ticks = x_indexes, labels = threads2)
    plt.title('Time of Reqeusts With 1 Second Sleep')
    plt.xlabel('Threads')
    plt.ylabel('Seconds')
    plt.legend()
elif graph == 3:
    #Speedup from doubling thread counts of low threads
    #Done using the results of 100 requests
    x_indexes = np.arange(len(performance))
    plt.axhline(y=2.0, color='y', linestyle='-')
    plt.plot(x_indexes, performance_increase1,marker = 'o', markerfacecolor = 'green')
    plt.xticks(ticks = x_indexes, labels = performance)
    plt.ylim((0.8,2.2))
    plt.title('Speedup From Doubling Thread Counts (Low Threads)')
    plt.xlabel('Thread Jump')
    plt.ylabel('Speedup')
elif graph == 4:
    #Speedup of doubling thread counts of high threads
    #Done using the results of 25600 requests
    x_indexes = np.arange(len(performance2))
    plt.axhline(y=2.0, color='y', linestyle='-')
    plt.plot(x_indexes, performance_increase2, marker = 'o', markerfacecolor = 'green')
    plt.xticks(ticks = x_indexes, labels = performance2)
    plt.ylim((0.8,2.2))
    plt.title('Speedup From Doubling Thread Counts (High Threads)')
    plt.xlabel('Thread Jump')
    plt.ylabel('Speedup')
elif graph == 5:
     x_indexes = np.arange(len(threads))
     plt.bar(x_indexes -0.25,nosleep_tot_times_high, width = 0.25, label = '100 000 Requests')
     plt.bar(x_indexes, nosleep_tot_times_med, width = 0.25, label = '50 000 requests')
     plt.bar(x_indexes +0.25, nosleep_tot_times_low, width = 0.25, label = '25 000 requests')
     plt.xticks(ticks = x_indexes, labels = threads)
     plt.ylim((0,200))
     plt.title('Time of Reqeusts With No Sleep')
     plt.xlabel('Threads')
     plt.ylabel('Seconds')
     plt.legend()



plt.show()

