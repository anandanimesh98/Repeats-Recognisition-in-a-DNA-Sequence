import numpy as np
from matplotlib import pyplot as plt
from repseeker import rep_timer
from threading import Thread as th

data_file = 'data3.txt'

def plotter():
    x = [i for i in range(6, 15)]
    # print('--x done')
    y = [rep_timer(data_file, i) for i in x]
    # print('-- y done')

    plt.title('')
    plt.xlabel('window length')
    plt.ylabel('')
    plt.plot(x, y, label='Time -v/s- Window size')
    plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad = 0.0)
    plt.show()

plotter()

# def thread_fn(i, list_t):
#     for i in range(i, 100, 8):
#         if i < 10: continue
#         list_t[i] = rep_timer(data_file, i)    

# def main():
#     list_t = [0] * 100
#     threads = [th(target = thread_fn, args = [i, list_t]) for i in range(8)]

#     for thread in threads:
#         thread.start()

#     for thread in threads:
#         thread.join()
    
#     plt.title('')
#     plt.xlabel('window length')
#     plt.ylabel('')
#     plt.plot([i for i in range(100)], list_t, label='Time -v/s- Window size')
#     plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad = 0.0)
#     plt.show()

# main()