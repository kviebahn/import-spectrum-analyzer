''' Created by Konrad on
2016-01-28 Thu 11:34 AM

This module imports csv files from the Keysight spectrum analyzer and plots the data in matplotlib.
'''

import numpy as np
import matplotlib.pyplot as plt
import csv
import time

my_title = 'AOM driver #1 signal'

my_date = time.strftime("%Y/%m/%d/")

my_folder = 'AOM drivers/'

fname = 'AOM_driver_1.csv'

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
    my_len = 0
    #skip first two rows

    #import csv as numpy array, leaving out blank rows
    for row in reader:
        print row
        print len(row)
        if not str.isdigit(row[0][1]):
            my_len = len(row)
        else:
            if (count == 0)*(str.isdigit(row[0][1]))*('' not in row[:my_len]):
                a = np.append(a,np.array(row).astype(np.float))
                count += 1
            else:
                if (len(row) == my_len)*('' not in row[:my_len]):
                    a = np.vstack((a,np.array(row[:my_len]).astype(np.float)))
    my_file.close()
    np.save(datapath[:-4] + '.npy',a)

#once you imported the file to npy it is much quicker to just load the npy rather than reading the whole csv again:
if loadnpy:
    a = np.load(datapath[:-4] + '.npy')

# Make plot

fig = plt.figure(figsize = (16,9))

ax = fig.add_subplot(111)

plt.title(my_title)
ax.set_xlabel('Scan/s')
ax.set_ylabel('Oscilloscope trace/V')

#ax.plot(a[:,0], a[:,3], 'b-', label = 'Doppler-broadened absorption')
#ax.plot(a[:,0], a[:,4], 'r-', label = 'Doppler-free absorption')
#ax.plot(a[:,0], a[:,1], 'y-', label = 'Intensity signal dl pro/V')
ax.plot(a[:,0], a[:,1], 'y-', label = 'AOM driver output')

ax.legend(loc = 6)


ax_twin = ax.twinx()

#ax_twin.plot(a[:,0], a[:,2], 'g-', label = 'Intensity signal CoSy/V')
ax_twin.plot(a[:,0], a[:,2], 'g-', label = 'AOM driver monitor')
ax_twin.set_ylabel('Oscilloscope trace/V')

ax_twin.legend(loc = 7)

#ax_twin.set_ylim(ymin = 2.4, ymax = 2.5)

#plt.ylim(ymin = 40, ymax = 50)
plt.xlim(xmin = a[0,0], xmax = a[-1,0])


plt.savefig(datapath[:-4] + '.pdf', format = 'pdf')
plt.savefig(datapath[:-4] + '.png', format = 'png')

plt.show()
