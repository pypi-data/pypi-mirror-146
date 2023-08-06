import json

import scipy.io
import scipy.linalg as spla
import numpy as np

import matplotlib.pyplot as plt

import nse_quadratic_mats.conv_tensor_utils as ctu

mats = scipy.io.loadmat('problem-setups/drivencavity__mats_NV3042_Re1.mat')

dtfile = 'data/snapshots_drivencavity_Re500_' +\
    'NV3042_tE3_Nts512_nsnaps512_vels.json'

with open(dtfile) as jsfile:
    velsnapshotdict = json.load(jsfile)

hmat = mats['H']
pdim = 15


def fullconv(vone, vtwo):
    return hmat @ np.kron(vone, vtwo)


trngelst = [float(tk) for tk in velsnapshotdict.keys()]

# putting the data into one matrix
vvelslst = [np.array(vk).flatten() for vk in velsnapshotdict.values()]
vvelsarr = np.array(vvelslst).T

# SVD to extract POD modes
U, S, Vh = spla.svd(vvelsarr, full_matrices=False)
plt.semilogy(S, 'o')
plt.show(block=False)

# POD projection matrix
Uk = U[:, :pdim]

vinit = velsnapshotdict['0.0']  # initial v comes as list
NV = len(vinit)

vinit = np.array(vinit).reshape((NV, 1))  # initial v as array
print('POD projection error on initial values: ',
      np.linalg.norm(vinit-Uk @ Uk.T @ vinit))

try:
    Lone = ctu.linearzd_quadterm(hmat, vinit, retparts=True, lone_only=True)
except TypeError:
    raise UserWarning('I have updated the `nse_quadratic_mats` module \n' +
                      'please update to `0.0.2` \n' +
                      '`pip install --upgrade nse_quadratic_mats` should do')

tNlist = []
for kkk in range(pdim):
    ccolumn = Uk[:, kkk:kkk+1]
    ctN = ctu.linearzd_quadterm(hmat, ccolumn, retparts=True, lone_only=True)
    tNlist.append(ctN)

vinitk = Uk.T @ vinit  # projected v
tvinit = Uk @ vinitk  # inflated projected v

tNtv = ctu.linearzd_quadterm(hmat, tvinit, retparts=True, lone_only=True)

ttNtv = vinitk[0, 0]*tNlist[0]
for kkk in range(1, pdim):
    ttNtv = ttNtv + vinitk[kkk, 0]*tNlist[kkk]

# sanity check -- should be 0 more or less -- no approximation here
eap = ttNtv @ vinit - tNtv @ vinit
print('Affine representation OK?: ', np.linalg.norm(eap))

morerror = ttNtv @ vinit - hmat @ np.kron(vinit, vinit)
print('Full convection vs. reduced-parameter affine LPV: ',
      np.linalg.norm(morerror))
