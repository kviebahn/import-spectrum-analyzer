''' Created by Konrad on
2016-01-28 Thu 11:34 AM

This module imports csv files from the Keysight spectrum analyzer and plots the data in matplotlib.
'''

import numpy as np
import matplotlib.pyplot as plt
import csv
import time

my_title = 'AOM driver SerNo #2 signal'

my_date = time.strftime("%Y/%m/%d/")

my_folder = 'AOM drivers/'

fname = 'AOM2.csv'

datadir = '//Volumes/data/Shared/'

datapath = datadir + my_date + my_folder + fname

importbool = True
loadnpy = False


if importbool:
    #initialize array
    a = np.array([])
    my_file = open(datapath)
    reader = csv.reader(my_file, dialect='excel', delimiter=',')
    count = 0
    my_len = 2
    #skip first two rows
    for i0 in xrange(58):
        next(reader) 
    #import csv as numpy array, leaving out blank rows
    for row in reader:
        print row
        if (count == 0):
            a = np.append(a,np.array(row[:my_len]).astype(np.float))
            count += 1
        else:
            a = np.vstack((a,np.array(row[:my_len]).astype(np.float)))
    my_file.close()
    np.save(datapath[:-4] + '.npy',a)

#once you imported the file to npy it is much quicker to just load the npy rather than reading the whole csv again:
if loadnpy:
    a = np.load(datapath[:-4] + '.npy')

# Make nice freq labels

unitHzNo = np.int(np.floor(np.log10(a[-1,0])/3.))

unitHzdict = {
    0:'Hz',
    1:'kHz',
    2:'MHz',
    3:'GHz'
}

freqlabel = 'Frequency/%s' % unitHzdict[unitHzNo]
a[:,0]/=(10**(unitHzNo*3))

# Make plot

fig = plt.figure(figsize = (16,9))

ax = fig.add_subplot(111)

plt.title(my_title)
ax.set_xlabel(freqlabel)
ax.set_ylabel('Power/dBm')

ax.plot(a[:,0], a[:,1], 'g-')#, label = 'AOM driver output')

#ax.legend(loc = 0)


#plt.ylim(ymin = 40, ymax = 50)
plt.xlim(xmin = a[0,0], xmax = a[-1,0])


plt.savefig(datapath[:-4] + '.pdf', format = 'pdf')
plt.savefig(datapath[:-4] + '.png', format = 'png')

plt.show()
