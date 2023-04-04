# Author: Vatsal Sanjay
# vatsalsanjay@gmail.com
# Physics of Fluids
# Last Update: Dec 30 2020

import numpy as np
import os
import subprocess as sp
import matplotlib.pyplot as plt
from matplotlib import rc
import matplotlib
from matplotlib.ticker import StrMethodFormatter
from matplotlib.ticker import FormatStrFormatter
from matplotlib.collections import LineCollection
import sys

matplotlib.rcParams['text.usetex'] = True
matplotlib.rcParams['font.family'] = 'serif'

def gettingFacets(filename, Tracer):
    if Tracer == 1:
        exe = ["./getFacet1", filename]
    else:
        exe = ["./getFacet2", filename]
    p = sp.Popen(exe, stdout=sp.PIPE, stderr=sp.PIPE)
    stdout, stderr = p.communicate()
    temp1 = stderr.decode("utf-8")
    temp2 = temp1.split("\n")
    segs = []
    skip = False
    if (len(temp2) > 1e2):
        for n1 in range(len(temp2)):
            temp3 = temp2[n1].split(" ")
            if temp3 == ['']:
                skip = False
                pass
            else:
                if not skip:
                    temp4 = temp2[n1+1].split(" ")
                    r1, z1 = np.array([float(temp3[1]), float(temp3[0])])
                    r2, z2 = np.array([float(temp4[1]), float(temp4[0])])
                    segs.append(((r1, z1),(r2,z2)))
                    segs.append(((-r1, z1),(-r2,z2)))
                    skip = True
    return segs

def gettingTriplePoint(filename, name1, DistCutoff):
    exe = ["./getX0Y0V0", filename, name1, str(DistCutoff)]
    p = sp.Popen(exe, stdout=sp.PIPE, stderr=sp.PIPE)
    stdout, stderr = p.communicate()
    temp1 = stderr.decode("utf-8")
    temp2 = temp1.split("\n")
    temp3 = temp2[0].split(" ")
    return float(temp3[0]), float(temp3[1]), float(temp3[2]), float(temp3[3])

# ----------------------------------------------------------------------------------------------------------------------


nGFS = 10000
ci = int(sys.argv[1])
Ldomain = float(sys.argv[2])
hf = float(sys.argv[3])

DistCutoff, BoxSize = 1e-4, 0.1

rmin, rmax, zmin, zmax = [-Ldomain/2., Ldomain/2., -hf*1.001, Ldomain-hf]

name1 = "%4.4d_X0Y0V0.dat" % ci

if os.path.exists(name1):
    print("File %s found! New data will be appended to the file" % name1)

folder = 'TrackingTP' # output folder
if not os.path.isdir(folder):
    os.makedirs(folder)

for ti in range(nGFS):
    t = (5e-4)*ti
    place = "intermediate/snapshot-%5.4f" % t
    ImageName = "%s/%9.9d.png" %(folder, int(100000*ti))
    if not os.path.exists(place):
        print("%s File not found!" % place)
    else:
        if os.path.exists(ImageName):
            print("%s Image present!" % ImageName)
        else:
            facets1 = gettingFacets(place, 1)
            facets2 = gettingFacets(place, 2)
            if (len(facets1) == 0 or len(facets2) == 0):
                print("Problem in the available file %s" % place)
            else:
                tp, zTP, rTP, vTP  = gettingTriplePoint(place, name1, DistCutoff)
                print("t %5.4f zTP %4.3f rTP %4.3f vTP %4.3e" % (tp, zTP, rTP, vTP))

                ## Part to plot
                AxesLabel, TickLabel = [30, 25]
                fig, (ax, ax2) = plt.subplots(1,2)
                fig.set_size_inches(19.20, 10.80)
                rc('axes', linewidth=2)
                ## Drawing Facets
                line_segments1 = LineCollection(facets1, linewidths=2, colors='#fc8d59', linestyle='solid')
                ax.add_collection(line_segments1)
                line_segments2 = LineCollection(facets2, linewidths=2, colors='#1a9850', linestyle='solid')
                ax.add_collection(line_segments2)
                ax.plot([rTP], [zTP], 'bo')
                ax.plot([-rTP], [zTP], 'bo')
                ax.plot([0, 0], [zmin, zmax],'--', color='grey')
                box = plt.Rectangle((rmin, zmin), rmax-rmin, zmax-zmin, fill=False, transform=ax.transData, color='k')
                ax.add_patch(box)
                
                box = plt.Rectangle((rTP-BoxSize/2., zTP-BoxSize/2.), BoxSize, BoxSize, fill=False, transform=ax.transData, color='gray')
                ax.add_patch(box)

                ax.set_xlabel(r'$\mathcal{R}$', fontsize=AxesLabel)
                ax.set_ylabel(r'$\mathcal{Z}$', fontsize=AxesLabel)
                ax.set_aspect('equal')
                ax.set_xlim(rmin, rmax)
                ax.set_ylim(zmin, zmax)
                ax.set_title('$t = %5.4f$' % t, fontsize=AxesLabel)

                ax.axis('off')

                # ax2 same as ax but zoomed in on the triple point: window size is BoxSize
                ## Drawing Facets
                line_segments12 = LineCollection(facets1, linewidths=2, colors='#fc8d59', linestyle='solid')
                ax2.add_collection(line_segments12)
                line_segments22 = LineCollection(facets2, linewidths=2, colors='#1a9850', linestyle='solid')
                ax2.add_collection(line_segments22)
                ax2.plot([rTP], [zTP], 'bo')
                ax2.plot([-rTP], [zTP], 'bo')
                ax2.plot([0, 0], [zmin, zmax],'--', color='grey')
                box = plt.Rectangle((rTP-BoxSize/2., zTP-BoxSize/2.), BoxSize, BoxSize, fill=False, transform=ax2.transData, color='gray')
                ax2.add_patch(box)

                ax2.set_xlabel(r'$\mathcal{R}$', fontsize=AxesLabel)
                ax2.set_ylabel(r'$\mathcal{Z}$', fontsize=AxesLabel)
                ax2.set_aspect('equal')
                ax2.set_xlim(rTP-BoxSize/2., rTP+BoxSize/2.)
                ax2.set_ylim(zTP-BoxSize/2., zTP+BoxSize/2.)
                ax2.axis('off')

                # plt.show()
                plt.savefig(ImageName,bbox_inches='tight')
                plt.close()
    print(("Done %d of %d" % (ti+1, nGFS)))
