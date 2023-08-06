import json
import logging
import argparse

import dolfin

from rich.logging import RichHandler
import numpy as np
# import matplotlib.pyplot as plt

import torch
# import dolfin

import dolfin_navier_scipy.dolfin_to_sparrays as dts
import dolfin_navier_scipy.problem_setups as dnsps
import dolfin_navier_scipy.stokes_navier_utils as snu

from nse_nn_lpv import nse_fem_utils as nfu
import nse_nn_lpv.nse_data_helpers as ndh
import nse_nn_lpv.CNN_utils as cnu

from data_handling_utils import get_nnmodel_str, get_traindata_str
import data_handling_utils as dhu
from data_plot_utils import plot_ld
from check_pod_parts import check_single_vec

debug = True
debug = False

logging.basicConfig(level=logging.INFO, handlers=[RichHandler()],
                    format='%(message)s',
                    datefmt="[%X]",
                    )

# logging.getLogger('matplotlib').setLevel(logging.WARNING)


def simuit(meshprfx='mesh/karman2D-outlets', meshlevel=1, xydims='47x63',
           ddir='simu-data/',
           pname='cw', N=None, nu=1e-2, Re=None,
           t0=0.0, tE=2.0, Nts=4e2+1, plotplease=True,
           pngplease=True,
           dataoutpnts=200,
           cae_model_parameters={},
           test_the_model=False,
           ldlpv='FOM', alpha=.5,
           proutdir='prv-plots/', ParaviewOutput=True, prvoutpnts=200,
           scheme='TH'):
    '''
    Parameters
    ---
    cae_model_parameters: dictionary
        with the parameters that defines the surrogate CNN/POD model
         * `dataendtime`
         * `datapoints`
         * `kpod` -- number of POD modes
         * `modeldatapath` -- path to the (learned) parameters of the model
    '''

    # ## FEM Problem Definition

    meshfile = meshprfx + '_lvl{0}.xml.gz'.format(meshlevel)
    physregs = meshprfx + '_lvl{0}_facet_region.xml.gz'.format(meshlevel)
    geodata = meshprfx + '_geo_cntrlbc.json'

    femp, stokesmatsc, rhsd = \
        dnsps.get_sysmats(problem='gen_bccont', Re=Re, bccontrol=False,
                          scheme=scheme, mergerhs=True,
                          meshparams=dict(strtomeshfile=meshfile,
                                          strtophysicalregions=physregs,
                                          strtobcsobs=geodata))

    V, invinds = femp['V'], femp['invinds']
    bcinds, bcvals = femp['dbcinds'], femp['dbcvals']

    data_prfx = '{4}_N{0}_Re{1}_Nts{2}_tE{3}_ndtpts_{5}'.\
        format(N, femp['Re'], Nts, tE, scheme, dataoutpnts)

    # for the lift drag computation

    cylbcinds = dnsps.get_bcinds(mesh=femp['mesh'], V=femp['V'],
                                 prfile=physregs, pelist=[5, 6, 7])

    phionevec = np.zeros((femp['V'].dim(), 1))
    phionevec[cylbcinds, :] = 1.
    phione = dolfin.Function(femp['V'])
    phione.vector().set_local(phionevec)
    ldsf = dnsps.LiftDragSurfForce(V=femp['V'], nu=femp['nu'],
                                   gradvsymmtrc=False, phione=phione)

    def comp_ld(vvec, pvec, time=None):
        vfun, pfun = dts.\
            expand_vp_dolfunc(V=femp['V'], Q=femp['Q'], vc=vvec, pc=pvec,
                              invinds=invinds, bcinds=bcinds, bcvals=bcvals)
        return ldsf.evaliftdragforce(u=vfun, p=pfun)

    # pickx = dolfin.as_matrix([[1., 0.], [0., 0.]])
    # pox = pickx*phione
    # picky = dolfin.as_matrix([[0., 0.], [0., 1.]])
    # poy = picky*phione
    # plt.figure(101)
    # dolfin.plot(pox)
    # plt.figure(102)
    # dolfin.plot(poy)
    # plt.show()
    # import ipdb
    # ipdb.set_trace()

    # setting some parameters
    if Re is not None:
        nu = femp['charlen']/Re

    # tips = dict(t0=t0, tE=tE, Nts=Nts)
    trange = np.linspace(t0, tE, Nts+1)
    # cnts = trange.size  # TODO: trange may be a list...
    # filtert = np.arange(0, cnts, np.int(np.floor(cnts/dataoutpnts)))
    # datatrange = trange[filtert]
    if ldlpv == 'POD' or ldlpv == 'CNN':
        modeldatadict = torch.load(cae_model_parameters['modeldatapath'])
        kpod = cae_model_parameters['kpod']
    else:
        pass

    if ldlpv == 'CNN':
        (xdim, ydim) = xydims.split(sep='x')
        xmshpoints, ymshpoints = np.int(xdim), np.int(ydim)

        with open(geodata) as f:
            domaindata = json.load(f)
        bbdict = domaindata['bounding box']  # bounding box of the domain
        xlims = [bbdict['xone'][0], bbdict['xtwo'][0]]
        ylims = [bbdict['xone'][1], bbdict['xfour'][1]]

        nnmp = cae_model_parameters  # short cut

        datashapes = cnu.\
            comptheshapes((1, 2, xmshpoints, ymshpoints),
                          channellist=nnmp['channellist'],
                          stride=nnmp['stride'],
                          kernelsize=nnmp['kernelsize'],
                          padding=nnmp['padding'])

        cnnaeout = datashapes[-1]

        modelparams = dict(channellist=nnmp['channellist'],
                           stride=nnmp['stride'],
                           padding=nnmp['padding'],
                           kernelsize=nnmp['kernelsize'],
                           sngl_lnr_lyr_dec=True,
                           sll_decode_size=kpod, cnnaeoutshape=cnnaeout)
        CAE_model = cnu.DynamicConvAutoencoder(
            nnmp['code_size'], **modelparams)
        modeldatadict = torch.load(nnmp['modeldatapath'])
        logging.debug('loaded model parameters:')
        CAE_model.load_state_dict(
            modeldatadict['model_states'], strict=True)
        logging.info('loaded CNN model')
        logging.debug('from: '+nnmp['modeldatapath'])

        def vvectdc(vvec):
            return nfu.\
                vvec_to_datachannels(vvec, V=femp['V'], xlims=xlims,
                                     ylims=ylims, xmshpoints=xmshpoints,
                                     ymshpoints=ymshpoints)
    else:
        pass

    # podmatstr = podbaspath + datastrg
    if ldlpv == 'CNN' or ldlpv == 'POD':
        podmatstr = modeldatadict['path_to_podvecs']
        logging.info(podmatstr)
        podbas = np.load(podmatstr+'.npy')[:, :kpod]
        prjvecs = np.load(podmatstr+'_prj'+'.npy')[:, :kpod]
        podshiftvec = np.load(podmatstr+'_shiftvec'+'.npy')
        logging.debug('POD vectors loaded from ' + podmatstr)

        podshiftvec_wbcs = np.full((V.dim(), 1), np.nan)
        podshiftvec_wbcs[invinds, :] = podshiftvec
        podshiftvec_wbcs[bcinds, 0] = bcvals

        # shiftvec = vvecl[0][invinds, :]
        shiftvec = podshiftvec
        mmat = stokesmatsc['M']
        code_size = cae_model_parameters['code_size']
        prjbas = prjvecs
    else:
        code_size = None
        alpha = None
        pass

    if test_the_model and ldlpv == 'CNN':
        strtodata = modeldatadict['path_to_data']
        check_single_vec(CAE_model=CAE_model, invinds=invinds,
                         mmat=mmat, shiftvec=shiftvec, prjbas=prjvecs,
                         strtodata=strtodata, podmatstr=podmatstr,
                         vvec_to_datachannel=vvectdc)
    else:
        pass

    # for vvec in vvecl[:5]:
    #     (_, vvecl), _, _ = ndh.get_nse_img_data(strtodata)

    #     vveci = vvec[invinds, :]
    #     xdata, ydata = nfu.\
    #         vvec_to_datachannels(vvec, V=femp['V'],
    #                              xlims=xlims, ylims=ylims,
    #                              xmshpoints=xmshpoints,
    #                              ymshpoints=ymshpoints)
    #     vvecdatatensor = ndh.convert_torchtens((xdata, ydata),
    #                                            scaledata=False)
    #     vvecdatatensor = vvecdatatensor[None, :, :, :]  # add the batch dim
    #     _, crho = CAE_model(vvecdatatensor)
    #     # nvvsqrd = vveci.T @ (mmat @ vveci)
    #     tvvec = podbas @ crho.detach().numpy().reshape((-1, 1)) + shiftvec
    #     diffv = vveci - tvvec
    #     ndvsqrd = diffv.T @ (mmat @ diffv)
    #     prjv = prjbas.T @ (vveci-shiftvec)
    #     prjv[code_size:, :] = 0
    #     ppdv = podbas @ prjv - vveci + shiftvec
    #     nppdvsqrd = ppdv.T @ (mmat @ ppdv)
    #     logging.info(f'CNN error sqrd: {ndvsqrd}')
    #     logging.info(f'POD error sqrd: {nppdvsqrd}')

    uselpv = ldlpv
    # if not uselpv == 'FOM':

    def CAE_LPV_convection(vvec):
        vveci = vvec[invinds, :]
        if uselpv == 'CNN' or logging.DEBUG >= logging.root.level:
            xdata, ydata = nfu.\
                vvec_to_datachannels(vvec, V=femp['V'], xlims=xlims,
                                     ylims=ylims, xmshpoints=xmshpoints,
                                     ymshpoints=ymshpoints)
            vvecdatatensor = ndh.\
                convert_torchtens((xdata, ydata), scaledata=False)
            vvecdatatensor = vvecdatatensor[None, :, :, :]  # add the batch dim
            _, crho = CAE_model(vvecdatatensor)
            cnnvvec = podbas@crho.detach().numpy().reshape((-1, 1)) + shiftvec
        else:
            pass

        if uselpv == 'POD' or logging.DEBUG >= logging.root.level:
            prjv = prjbas.T @ (vveci-shiftvec)
            prjv[code_size-1:, :] = 0
            podvvec = podbas @ prjv + shiftvec
        else:
            pass

        if logging.DEBUG >= logging.root.level:
            diffv = vveci - cnnvvec
            ndvsqrd = diffv.T @ (mmat @ diffv)
            poddiffvec = podvvec - vveci
            nppdvsqrd = poddiffvec.T @ (mmat @ poddiffvec)
            logging.debug(f'CNN error: {ndvsqrd}')
            logging.debug(f'POD error: {nppdvsqrd}')

        if uselpv == 'CNN':
            convvecvec = cnnvvec
        elif uselpv == 'POD':
            convvecvec = podvvec
        else:
            raise RuntimeError('no LPV approximation defined')

        bdnuv = dts.get_convvec(u0_vec=convvecvec, V=femp['V'],
                                uone_utwo_same=False, utwo_vec=vvec,
                                invinds=femp['invinds'],
                                dbcinds=femp['dbcinds'], dbcvals=bcvals)
        gdnuv = dts.get_convvec(u0_vec=vvec, V=femp['V'],
                                uone_utwo_same=False, utwo_vec=convvecvec,
                                invinds=femp['invinds'],
                                dbcinds=femp['dbcinds'], dbcvals=bcvals)
        nuv = (1-alpha)*gdnuv + alpha*bdnuv
        return -nuv

    logging.info('computing FEM simulation')
    soldict = stokesmatsc  # containing A, J, JT
    soldict.update(femp)  # adding V, Q, invinds, diribcs
    soldict.update(trange=trange, dataoutpnts=dataoutpnts)
    # adding time integration params
    soldict.update(fv=rhsd['fv'], fp=rhsd['fp'],
                   N=N, nu=nu,
                   start_ssstokes=True,
                   get_datastring=None,
                   treat_nonl_explicit=True,
                   dbcinds=femp['dbcinds'], dbcvals=femp['dbcvals'],
                   data_prfx=ddir+data_prfx,
                   paraviewoutput=ParaviewOutput,
                   # plttrange=plttrange,
                   prvoutpnts=prvoutpnts,
                   vfileprfx=proutdir+'vel_',
                   pfileprfx=proutdir+'p_')
    if not uselpv == 'FOM':
        logging.info('Convection with ' + uselpv + ' LPV approximation')
        soldict.update(use_custom_nonlinearity=True,
                       custom_nonlinear_vel_function=CAE_LPV_convection)

    vpod = {}
    snu.solve_nse(return_as_list=False,
                  vp_output=True, vp_out_fun=comp_ld, vp_output_dict=vpod,
                  check_ff=True, check_ff_maxv=1e3,
                  **soldict)

    resultstr = dhu.\
        get_lpvsimu_str(t0=t0, te=tE, Nts=Nts, alpha=alpha, ldlpv=ldlpv,
                        poddim=code_size, cnnmodstr=csmodelstr, Re=Re)
    lddatapath = 'results/drag-lift-curves/'
    ldjsstr = lddatapath + resultstr + '.json'
    with open(ldjsstr, 'w') as f:
        json.dump(vpod, f)
        logging.info('lift/drag data saved to \n' + ldjsstr)
    plot_ld(vpod, showplease=True)

    # import ipdb
    # ipdb.set_trace()
    # print(vellist)


if __name__ == '__main__':
    kernelsize = 5
    stride = 2
    padding = 1
    dataendtime = 2
    datapoints = 200
    kpod = 20
    podbaspath = './cached-data/pod-bases/'
    mshprfx = '../simulations-training-data/mesh/karman2D-outlets'
    scheme = 'TH'
    alpha = .5

    parser = argparse.ArgumentParser()

    # ## SIMULATION parameters
    parser.add_argument("--meshprefix", type=str,
                        help="prefix for the mesh files",
                        default=mshprfx)
    parser.add_argument("--alpha", type=float,
                        help="parameter blending the LPV", default=alpha)
    parser.add_argument("--meshlevel", type=int,
                        help="mesh level", default=1)
    parser.add_argument("--Re", type=int,
                        help="Reynoldsnumber", default=40)
    parser.add_argument("--tE", type=float,
                        help="final time of the simulation", default=1.)
    parser.add_argument("--Nts", type=float,
                        help="number of time steps", default=1200)
    parser.add_argument("--scaletest", type=float,
                        help="scale the test size", default=1.)
    parser.add_argument("--paraviewframes", type=int,
                        help="number of outputs for paraview", default=100)

    # ## LPV Model parameters
    parser.add_argument("--codesize", type=int,
                        help="code size of the model",
                        default='5')
    parser.add_argument("--datapoints", type=int,
                        help="number of data output points",
                        default=datapoints)
    parser.add_argument("--dataendtime", type=float,
                        help="final time of the data range",
                        default=dataendtime)
    parser.add_argument("--ldlpv", type=str, choices=['CNN', 'POD', 'FOM'],
                        help="which LPV approximation to choose",
                        default='CNN')
    parser.add_argument("--xydims", type=str,
                        help="dimensions of the input 2D images for the model",
                        default='47x63')
    parser.add_argument("--channelsizes", type=str,
                        help="channel sizes of the model",
                        default='2-4-8-10-12')
    parser.add_argument("--traintarget", type=str,
                        help="what the model was trained for",
                        default='cnvctn')
    parser.add_argument("--kpod", type=int,
                        help="number of POD modes used for the model output",
                        default=kpod)
    args = parser.parse_args()
    logging.info(args)

    chnll = [int(ccs) for ccs in args.channelsizes.split('-')]

    datastrg = get_traindata_str(te=args.dataendtime, Re=args.Re,
                                 num_dtpts=args.datapoints, xydim=args.xydims)

    csmodelstr = \
        get_nnmodel_str(channellist=chnll, num_pod_vecs=args.kpod,
                        stride=stride, kernelsize=kernelsize,
                        padding=padding, code_size=args.codesize,
                        target=args.traintarget)

    modelpath = './cached-data/pytorch-models/' + datastrg
    modeldatapath = modelpath + csmodelstr

    cae_model_parameters = \
        dict(kpod=args.kpod, dataendtime=args.dataendtime,
             datapoints=args.datapoints, channellist=chnll,
             code_size=args.codesize, modeldatapath=modeldatapath,
             stride=stride, padding=padding, kernelsize=kernelsize)

    simuit(Re=args.Re,
           meshprfx=args.meshprefix, meshlevel=args.meshlevel,
           t0=0., tE=args.scaletest*args.tE,
           Nts=np.int(args.scaletest*args.Nts),
           dataoutpnts=args.datapoints,
           ldlpv=args.ldlpv, alpha=args.alpha,
           # ddir=args.dataprefix,
           xydims=args.xydims, cae_model_parameters=cae_model_parameters,
           scheme=scheme, ParaviewOutput=True, prvoutpnts=args.paraviewframes)
