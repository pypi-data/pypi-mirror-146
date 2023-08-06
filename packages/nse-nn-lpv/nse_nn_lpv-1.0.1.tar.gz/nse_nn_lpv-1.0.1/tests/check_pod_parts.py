import logging

import numpy as np

import torch
from torch.utils.data import DataLoader

import nse_nn_lpv.CNN_utils as cnnh
import nse_nn_lpv.nse_data_helpers as ndh


def pod_convpod_approx(velvec_ns=None, shiftvec=None,
                       podvecs=None, prjvecs=None,
                       nvsmvmatv=None,
                       myfac=None, minvpodvecs=None,
                       podconvvecs=None,
                       getconvmat=None):

    print('******************')
    print(f'POD dim: {podvecs.shape[1]}')
    print(f'M-1-POD dim: {minvpodvecs.shape[1]}')
    print('******************')

    velvec = velvec_ns + shiftvec

    # print('shift alright: ', np.allclose(npcvcns, vvecl[-1]))
    check_nvsmvmatv = getconvmat(velvec_ns, dirizero=True)[0] @ (velvec)
    print('N(v-vs)*v check: ', np.allclose(check_nvsmvmatv, nvsmvmatv))

    pptnpcvc = podvecs @ (prjvecs.T @ velvec_ns)
    print('|(I-P)[v-vs]|/|vs|={0:.4e}'.
          format(np.linalg.norm(velvec_ns-pptnpcvc)/np.linalg.norm(velvec_ns)))

    npptvmatv = getconvmat(pptnpcvc, dirizero=True)[0] @ (velvec)

    # npcpodconvvecs = cpodconvvecs.numpy().reshape((-1, code_size))
    nppodcoeffs = prjvecs.T @ velvec_ns
    Nppt = podconvvecs @ nppodcoeffs

    difnppts = Nppt - npptvmatv

    nrmdifnppts = np.linalg.norm(difnppts)
    nrmlyindifnppts = np.linalg.norm(myfac.solve_F(difnppts))
    nrmwndifnppts = np.linalg.norm(minvpodvecs.T@(difnppts))

    print('|N(v-vs)v - N(P(v-vs))v| = {0:.4e}'.format(nrmdifnppts))
    print('|N(P(v-vs))v - rk*N(vk)v|_M-1 = {0:.4e}'.format(nrmlyindifnppts))
    print('|N(P(v-vs))v - rk*N(vk)v|_W = {0:.4e}'.format(nrmwndifnppts))
    print('.5*|N(P(v-vs))v - rk*N(vk)v|_W^2 = ' +
          '{0:.4e}'.format(.5*nrmwndifnppts*nrmwndifnppts))

    print('|rk*N(vk)v|_M-1 = {0:.4e}'.
          format(np.linalg.norm(myfac.solve_F(Nppt))))
    print('|rk*N(vk)v|_W = {0:.4e}'.
          format(np.linalg.norm(minvpodvecs.T@(Nppt))))
    print('|N(P(v-vs))v|_M-1 = {0:.4e}'.
          format(np.linalg.norm(myfac.solve_F(npptvmatv))))
    print('|N(P(v-vs))v|_W = {0:.4e}'.
          format(np.linalg.norm(minvpodvecs.T@(npptvmatv))))
    print('NoDIFFERENCePLEASE: |N(P(v-vs))v - rk*N(vk)v| = {0:.4e}'.
          format(np.linalg.norm(npptvmatv-Nppt)))
    # print('NoDIFFERENCePLEASE: N(P(v-vs))v - rk*N(vk)v = {0:.4e}'.
    #       format((npptvmatv-Nppt).sum()))

    podconvres = nvsmvmatv - Nppt
    lyipodconvres = myfac.solve_F(podconvres)
    credpodconvres = minvpodvecs.T @ podconvres

    redpodresnorm = np.linalg.norm(credpodconvres)
    fulpodresnorm = np.linalg.norm(lyipodconvres)

    print('|N(v-vs)v - rk*N(Vk)v| = {0:.4e}'.
          format(np.linalg.norm(podconvres)))
    print('|N(v-vs)v - rk*N(Vk)v|_M-1 = {0:.4e}'.
          format(fulpodresnorm))
    print('|N(v-vs)v - rk*N(Vk)v|_W = {0:.4e}'.
          format(redpodresnorm))
    print('(|podres|_M-1 - |podres|_W)/|podres|_M-1 = {0:.4e}'.
          format((fulpodresnorm-redpodresnorm)/redpodresnorm))
    print('**** THE LOSS ****')
    print('.5*|N(v-vs)v - rk*N(Vk)v|_W^2 = {0:.4e}'.
          format(redpodresnorm*redpodresnorm*0.5))


def checkall(tds, shiftvec=None, podvecs=None, prjvecs=None,
             myfac=None, minvpodvecs=None, getconvmat=None,
             batchsizechecklist=[1, 2, 10]):

    cnvchk_dataloader = DataLoader(tds, batch_size=1, shuffle=True)

    kpod = podvecs.shape[1]

    X, y = next(iter(cnvchk_dataloader))
    cpodconvvecs = y[1]
    cvvc = y[2]
    # cvvc_ns = testone[2]
    nvsmvmatv = y[0]

    pod_convpod_approx(velvec_ns=cvvc.numpy().reshape((-1, 1)),
                       shiftvec=shiftvec,
                       podvecs=podvecs, prjvecs=prjvecs,
                       myfac=myfac, minvpodvecs=minvpodvecs,
                       nvsmvmatv=nvsmvmatv.numpy().reshape((-1, 1)),
                       podconvvecs=cpodconvvecs.numpy().reshape((-1, kpod)),
                       getconvmat=getconvmat)

    print('******************')
    print('Conv POD Loss Function Check')
    print('******************')

    ttprjvecs = torch.from_numpy(prjvecs).float()
    pcl = cnnh.PODConvLoss(lytinvmat=minvpodvecs.T)
    ttpodcoeffs = ttprjvecs.T.matmul(y[2])
    cpcll = pcl(ttpodcoeffs, (y[0], y[1]))
    print(f'Nbatch: {y[0].shape[0]}, Loss: {cpcll.item():.2e}')

    for bsc in batchsizechecklist:
        cnvchk_dataloader = DataLoader(tds, batch_size=bsc, shuffle=True)
        X, y = next(iter(cnvchk_dataloader))
        ttpodcoeffs = ttprjvecs.T.matmul(y[2])
        cpcll = pcl(ttpodcoeffs, (y[0], y[1]))
        print(f'Nbatch: {y[0].shape[0]}, Loss: {cpcll.item():.2e}')

    return


def check_single_vec(CAE_model=None, vvec=None, shiftvec=None,
                     invinds=None, lossfun=None, code_size=5,
                     podbas=None, prjbas=None, plotplease=False,
                     strtodata=None, podmatstr=None,
                     vvec_to_datachannel=None, mmat=None):

    # strtodata = '../simulations-training-data/train-data/' +\
    #     'sc_0-2_200_47x63.json'
    # podmatstr = './cached-data/pod-bases/sc_0-2_200_47x63_kp20'
    podbas = np.load(podmatstr+'.npy')
    (nsedatal, vvecl), femdata, vlctflddata = ndh.get_nse_img_data(strtodata)
    vvec = vvecl[0]
    for vvec in vvecl[:2]:
        vveci = vvec[invinds, :]
        xdata, ydata = vvec_to_datachannel(vvec)
        # xdata, ydata = xdata.T, ydata.T
        # import ipdb
        # ipdb.set_trace()
        vvecdatatensor = ndh.convert_torchtens((xdata, ydata), scaledata=False)
        vvecdatatensor = vvecdatatensor[None, :, :, :]  # add the batch dim
        _, crho = CAE_model(vvecdatatensor)
        logging.debug(f'cnn pred {crho}')
        kpod = crho.shape[-1]
        # nvvsqrd = vveci.T @ (mmat @ vveci)
        tvvec = podbas[:, :kpod] @ crho.detach().numpy().reshape((-1, 1)) \
            + shiftvec
        diffv = vveci - tvvec
        ndvsqrd = .5 * diffv.T @ (mmat @ diffv)
        prjv = prjbas[:, :kpod].T @ (vveci-shiftvec)
        prjv[code_size:, :] = 0
        ppdv = podbas[:, :kpod] @ prjv - vveci + shiftvec
        nppdvsqrd = .5 * ppdv.T @ (mmat @ ppdv)

        logging.info(f'state: CNN error sqrd/2: {ndvsqrd}')
        logging.info(f'state: POD error sqrd/2: {nppdvsqrd}')
    pass
