#!/usr/bin/env python

import os, sys

try:
    import tables
except ImportError:
    print "Failed to import the 'tables' python module"
    print "This is required to load the hdf format files that MSMBuilder uses to store the cluster centers"
    print "Please install PyTables before proceeding:"
    print "http://www.pytables.org/moin"
    sys.exit(1)

import numpy as np

def usage():
    print 'USAGE'
    print '    %s <hdf_path> <output_path>' % sys.argv[0]
    print
    print 'DESCRIPTION'
    print "    Convert the cluster definitions from MSMBuilder's HDF storage format to one"
    print "    compatiable with AWE. Please be aware that only MSMBuilder's 'hybrid' clustering"
    print "    algorithm is supported."
    sys.exit(1)


PRECISION = 1000.

parms = sys.argv[1:]
if len(parms) == 0 or '-h' in parms or '--help' in parms or '-?' in parms:
    usage()

try:
    hdfile  = parms[0]
    txtfile = parms[1]
except IndexError:
    usage()


F = tables.openFile(hdfile)
data = F.getNode('/XYZList').read()

### convert from the lossy integer scheme
data = data.astype('float32') / PRECISION

ncells, ncoords, dim = data.shape

with open(txtfile, 'w') as fd:
    fd.write('ncells: '  + str(ncells) + '\n')
    fd.write('ncoords: ' + str(ncoords) + '\n')
    fd.write('ndims: '   + str(dim)    + '\n')
    fd.write('\n')

    np.savetxt(fd, data.flatten(), fmt='%f')

F.close()
