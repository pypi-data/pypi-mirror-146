import os
import json
import logging
from rich.logging import RichHandler

import numpy as np

import torch
import torch.optim as optim
from torch.utils.data import DataLoader

import nse_nn_lpv.CNN_utils as cnnh
import nse_nn_lpv.nse_data_helpers as ndh

import nse_nn_lpv.nse_fem_utils as nfu

import multidim_galerkin_pod.gen_pod_utils as gpu

from train_cnnnse_models import train_cnnnse  # , check_CNN_POD
from check_pod_parts import checkall, check_single_vec
import data_handling_utils as dhu

debug = True
debug = False


# ######################################
# ## CHAP: Set Parameters
# ######################################

showfeaturemaps = False

# pathcorr = '../simulations-training-data/'
kpod = 15
kconvpod = 45
scaledata = True
scaledata = False

torch.manual_seed(0)

# Hyperparameters for the CNN
# code_size = 15
batch_size = 25
tst_batch_size = 100
num_epochs = 35
upd_epochs = 10

lr = 0.0075  # 0.01 in Lee/Carlberg
optimizer_cls = optim.Adam

# channellist = [2, 6, 10, 15]  # , 12, 24]  # defines the number of C-Layers
kernelsize = 5
stride = 2
padding = 1

logging.basicConfig(level=logging.INFO, handlers=[RichHandler()],
                    format='%(message)s',
                    datefmt="[%X]",
                    )


# ######################################
# ## CHAP: Load the FEM Data
# ######################################


def train_test_PODCNN(code_size_l=None, channellist=None,
                      modelpath=None,
                      cvvecspath='./cached-data/conv-vecs/',
                      strtodata=None, podmatstr=None,
                      cvvecsjsonstr=None,
                      focus_init_data=False, fid_params=[20, 10],
                      testfor=None, trainfor=None, return_error_lists=True,
                      datadims=None, datapoints=None, dataendtime=None):

    modelstr = '_cl' + '-'.join(str(chnl) for chnl in channellist)
    modelstr = modelstr + f'_ks{kernelsize}_strd{stride}_pdg{padding}'
    modelstr = modelstr + f'_kpod{kpod}'

    logging.info('***********************************')
    logging.info('train for ' + trainfor + ' -- test for ' + testfor)
    logging.info('***********************************')
    logging.info('loading the velocity field data')
    logging.debug('from ' + strtodata)
    (nsedatal, vvecl), femdata, vlctflddata = ndh.get_nse_img_data(strtodata)
    logging.info('done loading the velocity field data')

    # ######################################
    # ## CHAP: Get the FEM coefficients
    # ######################################
    mmat, convfun, getconvmat, vvec_to_datachannels, invinds = nfu.\
        get_fem_utils(meshfile=femdata['meshfile'],
                      geodata=femdata['geodata'],
                      physregs=femdata['physregs'],
                      scheme=femdata['femscheme'],
                      vtdc_dict=femdata['geometry'])

    # vvecchk = vvec_to_datachannels(vvecl[-1])
    # import ipdb
    # ipdb.set_trace()
    vvecl = [vvec[invinds, :] for vvec in vvecl]  # reduce to inner indices
    # if shiftdata:
    shiftvec = vvecl[0]  # [invinds, :]
    vvecl_shftd = [vvec - shiftvec for vvec in vvecl]
    podsnapshotl = vvecl_shftd
    # else:
    #     shiftvec = None
    #     vvecl_shftd = None
    #     podsnapshotl = vvecl

    mmatcoo = mmat.tocoo()
    myfac = gpu.SparseFactorMassmat(mmat)

    # ######################################
    # ## CHAP: Compute the POD Modes
    # ######################################

    # ## Compute the POD modes for the velocity vectors
    try:
        podvecs = np.load(podmatstr+'.npy')
        prjvecs = np.load(podmatstr+'_prj'+'.npy')
        poddatasv = np.load(podmatstr+'_shiftvec.npy')
        if not np.allclose(poddatasv, shiftvec):
            raise RuntimeError('shifts do not coincide')
        if podvecs.shape[1] < kpod:
            raise FileNotFoundError('need more podvecs - comp more podvecs')
        else:
            prjvecs = prjvecs[:, :kpod]
            podvecs = podvecs[:, :kpod]
        logging.info('loaded POD-vecs')
        logging.debug('from: ' + podmatstr)
    except FileNotFoundError as e:
        logging.debug(e, exc_info=True)
        logging.info('computing POD-vecs')
        podsnpshtmat = np.hstack(podsnapshotl)
        podvecs, prjvecs = gpu.\
            get_podbas_wrtmass(podsnpshtmat, My=mmat, npodvecs=kpod)
        # cspodvecs, csprjvecs = gpu.get_podbas_wrtmass(podsnpshtmat, My=mmat,
        #                                               npodvecs=code_size)
        np.save(podmatstr, podvecs)
        np.save(podmatstr+'_prj', prjvecs)
        np.save(podmatstr+'_shiftvec', shiftvec)
        logging.info('saved POD-vecs')
        logging.debug('saved to:\n'+podmatstr)

    # ## Compute the convection vectors and the POD modes for them
    try:
        if debug:
            raise FileNotFoundError()
        with open(cvvecsjsonstr) as jsf:
            podconvvvl = json.load(jsf)
        cnv = len(podconvvvl[0])
        podconvvvl = [np.array(cpcvl).reshape((cnv, 1))
                      for cpcvl in podconvvvl]
        logging.info('loaded convection vectors')
    except FileNotFoundError as e:
        logging.info('computing/saving convection vectors')
        logging.debug(e, exc_info=True)
        podconvvvl = []
        for vvec in vvecl_shftd:
            ccnvmat, ccnvadd = getconvmat(vvec, dirizero=True)
            podconvvvl.append(ccnvmat@(vvec+shiftvec))
        jspodconvvvl = [cpcvl.flatten().tolist() for cpcvl in podconvvvl]
        with open(cvvecsjsonstr, 'w') as jsf:
            json.dump(jspodconvvvl, jsf)

    cnvpodmatstr = podmatstr + f'_convkp{kconvpod}'
    try:
        lytinvcpv = np.load(cnvpodmatstr+'.npy')
        logging.info('loaded convPOD-vecs')
        logging.debug('from: '+cnvpodmatstr)
        if debug:
            raise FileNotFoundError('debugging -- gonna compute it anyways')
        else:
            pass
        if lytinvcpv.shape[1] < kpod:
            raise FileNotFoundError('need more podvecs - comp more podvecs')
        else:
            lytinvcpv = lytinvcpv[:, :kpod]
    except FileNotFoundError as e:
        logging.debug(e, exc_info=True)
        lyiconvvecl = [myfac.solve_F(cvc) for cvc in podconvvvl]
        cnvpodsnapshots = np.hstack(lyiconvvecl)
        cnvpodvecs, _ = gpu.get_podbases(cnvpodsnapshots, nlsvecs=kconvpod)
        lytinvcpv = myfac.solve_Ft(cnvpodvecs)
        np.save(cnvpodmatstr, lytinvcpv)
        logging.info('saved convPOD-vecs')
        logging.debug('to:\n'+cnvpodmatstr)

    podvecconvl = [getconvmat(podmode.flatten(), dirizero=True)[0]
                   for podmode in podvecs.T]

    # myloss = cnnh.get_podbas_mmat_mseloss(myfac.Ft @ podvecs)
    # myloss = cnnh.FEMLoss(mmat=mmatcoo, podbas=podvecs)
    # femloss = cnnh.FEMLoss(mmat=mmat)

    # ######################################
    # ## CHAP: NSE Data as Dataset
    # ######################################
    # vvecl_ds = vvecl_shftd if shiftdata else vvecl
    trn_nse_data_plain = ndh.\
        NSEDataSetPlain(nsedatal, vvecl_shftd, scaledata=scaledata,
                        velmaxima=vlctflddata['velmaxima'])

    if focus_init_data:
        for extprcntg in fid_params:
            for datalist in [nsedatal, vvecl_shftd, vvecl, podconvvvl]:
                fltridx = dhu.exp_subset_indcs(datalist, extprcntg)
                extdata = [datalist[idx] for idx in fltridx]
                datalist.extend(extdata)
            logging.info(f'doubled the data by {extprcntg} percent ' +
                         'with exp focus on the beginning')

    trn_nse_data_conv = ndh.\
        NSEDataSetPODConv(nsedatal, vvecl_shftd, scaledata=scaledata,
                          velmaxima=vlctflddata['velmaxima'],
                          vvecl_not_shifted=vvecl,
                          cvvl=podconvvvl,  # vsconv=convsmat,
                          podvconvl=podvecconvl)

    # ######################################
    # ## CHAP: Instatiate the CNN Model
    # ######################################

    stst_dataloader = DataLoader(trn_nse_data_plain, batch_size=tst_batch_size,
                                 shuffle=True)

    (testimages, testvecs) = next(iter(stst_dataloader))

    datashapes = cnnh.comptheshapes(testimages.shape, channellist=channellist,
                                    stride=stride,
                                    kernelsize=kernelsize, padding=padding)

    cnnaeout = datashapes[-1]
    outdof = cnnaeout[3]*cnnaeout[2]*cnnaeout[1]
    indofl = datadims.split('x')
    indof = int(indofl[0]) * int(indofl[1])
    logging.info('*** CNN-AE sizes ***')
    logging.info(f'in: {datadims} -- DOF-in: {indof}')
    logging.info(f'*** out {cnnaeout} -- DOF per batch {outdof}')
    if trainfor == 'state':
        trn_dataloader = DataLoader(trn_nse_data_plain, batch_size=batch_size,
                                    shuffle=True)
        trn_loss = cnnh.FEMLoss(mmat=mmatcoo, podbas=podvecs)
    elif trainfor == 'cnvctn':
        trn_dataloader = DataLoader(trn_nse_data_conv, batch_size=batch_size,
                                    shuffle=True)
        trn_loss = cnnh.PODConvLoss(lytinvcpv.T)
        if debug:
            checkall(trn_nse_data_conv, shiftvec=shiftvec,
                     podvecs=podvecs, prjvecs=prjvecs,
                     myfac=myfac, minvpodvecs=lytinvcpv, getconvmat=getconvmat)
    elif trainfor == 'both':
        trn_dataloader = DataLoader(trn_nse_data_conv, batch_size=batch_size,
                                    shuffle=True)
        trn_loss_stt = cnnh.FEMLoss(mmat=mmatcoo, podbas=podvecs)
        trn_loss_cnv = cnnh.PODConvLoss(lytinvcpv.T)

        def trn_loss(cpred, chky):
            return .5*(trn_loss_stt(cpred, chky[2])+trn_loss_cnv(cpred, chky))

    else:
        raise NotImplementedError()

    if testfor == 'state':
        chk_dataloader = DataLoader(trn_nse_data_plain, batch_size=batch_size,
                                    shuffle=True)
        full_chk_dataloader = DataLoader(trn_nse_data_plain,
                                         batch_size=len(vvecl), shuffle=False)
        tst_loss = cnnh.FEMLoss(mmat=mmatcoo, podbas=podvecs)
    elif testfor == 'cnvctn':
        chk_dataloader = DataLoader(trn_nse_data_conv, batch_size=batch_size,
                                    shuffle=True)
        full_chk_dataloader = DataLoader(trn_nse_data_conv,
                                         batch_size=len(vvecl), shuffle=False)
        tst_loss = cnnh.PODConvLoss(lytinvcpv.T)
    else:
        raise NotImplementedError()

    # ######################################
    # ## CHAP: Train and Test for different model parameters
    # ######################################

    cnnel = []  # lists to collect the errors
    podel = []
    for code_size in code_size_l:
        # string to save/load the model
        csmodelstr = dhu.\
            get_nnmodel_str(channellist=channellist, num_pod_vecs=kpod,
                            stride=stride, kernelsize=kernelsize,
                            padding=padding, code_size=code_size,
                            target=trainfor)

        # ## Define the model
        modelparams = dict(channellist=channellist, stride=stride,
                           padding=padding, kernelsize=kernelsize,
                           sngl_lnr_lyr_dec=True,
                           sll_decode_size=kpod, cnnaeoutshape=cnnaeout)
        DAE_model = cnnh.\
            DynamicConvAutoencoder(code_size, **modelparams)

        # ## Train the model
        try:
            if debug:
                raise IOError()
            mdd = torch.load(modelpath+csmodelstr)
            logging.debug('loaded model parameters:')
            for param_tensor in DAE_model.state_dict():
                logging.debug(param_tensor)
                logging.debug(DAE_model.state_dict()[param_tensor].size())
            DAE_model.load_state_dict(
                mdd['model_states'], strict=True)
            logging.info('loaded CNN model')
            logging.debug('from: '+modelpath+csmodelstr)
            if not dhu.check_fid(mdd['fid_dict'], fid_params, focus_init_data):
                logging.info('not the same focus on initial data')
                logging.info('gonna do some more training')
                raise KeyError('little hack')
            else:
                pass
            save_model_please = False
            # save_model_please = True  # need the pod paths

        except IOError as e:
            logging.debug(e, exc_info=True)
            train_cnnnse(DAE_model, optimizer_cls=optimizer_cls,
                         lr=lr, loss_fun=trn_loss, num_epochs=num_epochs,
                         trn_dataloader=trn_dataloader)
            save_model_please = True
        except KeyError as e:
            logging.debug(e, exc_info=True)
            logging.info('hack or error in the model dict keys -- retrain')
            train_cnnnse(DAE_model, optimizer_cls=optimizer_cls,
                         lr=lr, loss_fun=trn_loss, num_epochs=upd_epochs,
                         trn_dataloader=trn_dataloader)
            save_model_please = True

        if save_model_please:
            torch.save({'model_states': DAE_model.state_dict(),
                        'path_to_data': os.path.abspath(strtodata),
                        'path_to_podvecs': os.path.abspath(podmatstr),
                        'model_parameters': modelparams,
                        'fid_dict': dict(focus_init_data=focus_init_data,
                                         fid_params=fid_params)},
                       modelpath+csmodelstr)
            logging.info('model and link to data saved to:\n' +
                         modelpath+csmodelstr)
            logging.debug('model and link to data saved to:\n' +
                          os.path.abspath(modelpath+csmodelstr))
        else:
            pass

        chkX, chky = next(iter(chk_dataloader))

        illustration = True
        illustration = False
        if illustration:
            from data_plot_utils import dae_model_illustration
            dae_model_illustration(DAE_model, chkX)

        # CNN Error
        _encode_, cpred = DAE_model(chkX)

        ccnnerr = tst_loss(cpred, chky)

        # POD Error -- with podbasis of size `code_size`
        tprjvecs = torch.from_numpy(prjvecs).float()
        if testfor == 'cnvctn':
            cspodcoeffs = tprjvecs.T.matmul(chky[2])
        elif testfor == 'state':
            cspodcoeffs = tprjvecs.T.matmul(chky)
        else:
            raise NotImplementedError()
        cspodcoeffs[:, code_size:, :] = 0  # set coeffs `0` up to `code_size`
        cscpl = tst_loss(cspodcoeffs, chky)
        cnnel.append(ccnnerr.item())
        podel.append(cscpl.item())

    test_sngl_vecs = True
    if test_sngl_vecs:
        fchkX, fchky = next(iter(full_chk_dataloader))
        for cdtp in range(2):  # len(vvecl)):
            if testfor == 'state':
                chkX = fchkX[cdtp:cdtp+1, :, :, :]
                chky = fchky[cdtp:cdtp+1, :, :]
            elif testfor == 'cnvctn':
                chkX = fchkX[cdtp:cdtp+1, :, :, :]
                chky = (fchky[0][cdtp:cdtp+1, :, :],
                        fchky[1][cdtp:cdtp+1, :, :],
                        fchky[2][cdtp:cdtp+1, :, :],
                        fchky[3][cdtp:cdtp+1, :, :])

            # CNN Error
            _, cpred = DAE_model(chkX)
            logging.debug(f'cnn pred {cpred}')
            ccnnerr = tst_loss(cpred, chky)
            logging.info(f'sngl cnn err {ccnnerr.item()}')

            # POD Error -- with podbasis of size `code_size`
            tprjvecs = torch.from_numpy(prjvecs).float()
            if testfor == 'cnvctn':
                cspodcoeffs = tprjvecs.T.matmul(chky[2])
            elif testfor == 'state':
                cspodcoeffs = tprjvecs.T.matmul(chky)
            else:
                raise NotImplementedError()
            cspodcoeffs[:, code_size:, :] = 0
            cscpl = tst_loss(cspodcoeffs, chky)
            logging.info(f'sngl pod err {cscpl.item()}')

    logging.info('***************************************')
    logging.info('trained for ' + trainfor + ' -- tested for ' + testfor)
    logging.info('***************************************')
    print('code sizes: ', code_size_l)
    print('cnn errors: ', cnnel)
    print('pod errors: ', podel)

    if showfeaturemaps:
        from feature_maps_utils import plot_feature_maps
        plot_feature_maps(DAE_model, chkX[0, :, :, :])

    check_single_vec(CAE_model=DAE_model, podbas=podvecs, invinds=invinds,
                     mmat=mmat, shiftvec=shiftvec, prjbas=prjvecs,
                     strtodata=strtodata, podmatstr=podmatstr,
                     vvec_to_datachannel=vvec_to_datachannels)
    if return_error_lists:
        return cnnel, podel


if __name__ == '__main__':
    import argparse
    datanums = 200

    # modelstr = modelstr + '_shftd' if shiftdata else modelstr
    parser = argparse.ArgumentParser()
    parser.add_argument("--Re", type=int,
                        help="Reynolds number", default=40)
    parser.add_argument("--dataendtime", type=float,
                        help="final time of the data range", default=1.)
    parser.add_argument("--datapoints", type=int,
                        help="number of data points", default=datanums)
    parser.add_argument("--xydims", type=str,
                        help="dimensions of the input 2D images for the CNN",
                        default='47x63')
    parser.add_argument("--codesizes", type=str,
                        help="dimensions of the input 2D images for the CNN",
                        default='3-5-8')
    parser.add_argument("--channelsizes", type=str,
                        help="dimensions of the input 2D images for the CNN",
                        default='2-4-8-10-12')
    parser.add_argument("--traintesttarget", type=str,
                        help="what to train and what to test for",
                        default='cc')
    parser.add_argument("--fid", type=bool,
                        help="whether to put extra focus on the initial data",
                        default=False)
    parser.add_argument("--fidparams", type=str,
                        help="percentages of focii on the ini data",
                        default='15-10')

    args = parser.parse_args()
    logging.info(args)
    code_size_l = [int(ccs) for ccs in args.codesizes.split('-')]
    chnl_size_l = [int(ccs) for ccs in args.channelsizes.split('-')]

    fid_params = [int(ccs) for ccs in args.fidparams.split('-')]

    dtendtm = np.int(args.dataendtime) \
        if np.round(args.dataendtime) == args.dataendtime else args.dataendtime
    trntstdct = dict(c='cnvctn', s='state', b='both')
    trainfor = trntstdct[args.traintesttarget[0]]
    testfor = trntstdct[args.traintesttarget[1]]

    datastrg = dhu.\
        get_traindata_str(te=args.dataendtime,
                          num_dtpts=args.datapoints, xydim=args.xydims, Re=args.Re)

    strtodata = '../simulations-training-data/train-data/' + datastrg + '.json'
    strtopodbas = './cached-data/pod-bases/' + datastrg
    strtocvvecs = './cached-data/conv-vecs/' + datastrg
    modelpath = './cached-data/pytorch-models/' + datastrg

    cnnel, podel = \
        train_test_PODCNN(code_size_l=code_size_l,
                          trainfor=trainfor, testfor=testfor,
                          datadims=args.xydims, channellist=chnl_size_l,
                          strtodata=strtodata, modelpath=modelpath,
                          podmatstr=strtopodbas,
                          cvvecsjsonstr=strtocvvecs,
                          focus_init_data=args.fid, fid_params=fid_params,
                          dataendtime=dtendtm, datapoints=args.datapoints)
