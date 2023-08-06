import json

import scipy.io
import numpy as np

mats = scipy.io.loadmat('problem-setups/drivencavity__mats_NV3042_Re1.mat')

dtfile = 'data/snapshots_drivencavity_Re500_' +\
    'NV3042_tE3_Nts512_nsnaps512_vels.json'

with open(dtfile) as jsfile:
    velsnapshotdict = json.load(jsfile)

hmat = mats['H']


def fullconv(vone, vtwo):
    return hmat @ np.kron(vone, vtwo)


vinit = velsnapshotdict['0.0']  # initial v comes as list
NV = len(vinit)

vinit = np.array(vinit).reshape((NV, 1))  # initial v as array

print(np.linalg.norm(vinit-fullconv(vinit, vinit)))
