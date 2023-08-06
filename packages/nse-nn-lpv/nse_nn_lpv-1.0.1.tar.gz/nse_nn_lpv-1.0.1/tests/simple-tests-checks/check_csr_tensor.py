import numpy as np

import torch

import nse_nn_lpv.nse_fem_utils as nfu
import multidim_galerkin_pod.gen_pod_utils as gpu

import nse_nn_lpv.nse_data_helpers as ndh

strtodata = '../simulations-training-data/train-data/0-1_100_47x63_cntrd.json'
(nsedatal, vvecl), femdata = ndh.\
    get_nse_img_data(strtodata, return_fem_info=True, return_vvecs=True)
pathcorr = '../simulations-training-data/'
kpod = 30

mmat, convfun, getconvmat, invinds = nfu.\
    get_fem_utils(meshfile=pathcorr+femdata['meshfile'],
                  geodata=pathcorr+femdata['geodata'],
                  physregs=pathcorr+femdata['physregs'],
                  scheme=femdata['femscheme'])

meanv = 0
velstrs = femdata['velstrs']
podsnapshotl = []

for ckey in velstrs.keys():
    if ckey == 'mean':
        pass
    else:
        cv = np.load(pathcorr+velstrs[ckey]+'.npy')[invinds, :]
        podsnapshotl.append(cv - meanv)

podsnpshtmat = np.hstack(podsnapshotl)
podvecs, prjvecs = gpu.get_podbas_wrtmass(podsnpshtmat, My=mmat, npodvecs=kpod)
myfac = gpu.SparseFactorMassmat(mmat)

myf = myfac.F

ttcolidx = torch.from_numpy(myf.indices)
ttcrowidx = torch.from_numpy(myf.indptr)
ttdata = torch.from_numpy(myf.data)
ttmf = torch._sparse_csr_tensor(ttcrowidx, ttcolidx, ttdata,
                                size=myf.shape, dtype=torch.double)
