import os
import json
import logging

from rich.logging import RichHandler
import numpy as np
import matplotlib.pyplot as plt

# import dolfin

# import dolfin_navier_scipy.dolfin_to_sparrays as dts
import dolfin_navier_scipy.problem_setups as dnsps
import dolfin_navier_scipy.stokes_navier_utils as snu


from nse_nn_lpv import nse_fem_utils as nfu

debug = True
debug = False

logging.basicConfig(level=logging.INFO, handlers=[RichHandler()],
                    format='%(message)s',
                    datefmt="[%X]",
                    )

def directory_generator(dirName):
    try:
        os.mkdir(dirName)
        print("Directory ", dirName,  "Created") 
    except FileExistsError:
        print("Directory ", dirName,  "Already exists")

def testit(meshprfx='mesh/karman2D-outlets', meshlevel=1, proutdir='results/',
           outputfile='notspecified.json', xydims='47x63',
           ddir='simu-data/',
           pname='cw', N=None, nu=1e-2, Re=None,
           t0=0.0, tE=2.0, Nts=4e2+1, plotplease=True,
           pngplease=True,
           ParaviewOutput=False, prvoutpnts=200,
           dataoutpnts=200,
           scheme='TH'):

    (xdim, ydim) = xydims.split(sep='x')
    xmshpoints, ymshpoints = int(xdim), int(ydim)

    if not (np.mod(xmshpoints, 16) == 15 and np.mod(ymshpoints, 16) == 15):
        dx = 15 - np.mod(xmshpoints, 16)
        dy = 15 - np.mod(ymshpoints, 16)
        raise UserWarning('the dimensions must be compatible for the CNN: \n' +
                          'need dim = k*16 + 15 \n' +
                          'please add -- x+={0}, y+={1}'.format(dx, dy))

    meshfile = meshprfx + '_lvl{0}.xml.gz'.format(meshlevel)
    physregs = meshprfx + '_lvl{0}_facet_region.xml.gz'.format(meshlevel)
    geodata = meshprfx + '_geo_cntrlbc.json'

    femp, stokesmatsc, rhsd = \
        dnsps.get_sysmats(problem='gen_bccont', Re=Re, bccontrol=False,
                          scheme=scheme, mergerhs=True,
                          meshparams=dict(strtomeshfile=meshfile,
                                          strtophysicalregions=physregs,
                                          strtobcsobs=geodata))
    data_prfx = '{4}_N{0}_Re{1}_Nts{2}_tE{3}_ndtpts_{5}'.\
        format(N, femp['Re'], Nts, tE, scheme, dataoutpnts)

    # setting some parameters
    if Re is not None:
        nu = femp['charlen']/Re

    # tips = dict(t0=t0, tE=tE, Nts=Nts)
    trange = np.linspace(t0, tE, Nts+1)
    # cnts = trange.size  # TODO: trange may be a list...
    # filtert = np.arange(0, cnts, np.int(np.floor(cnts/dataoutpnts)))
    # datatrange = trange[filtert]

    try:
        os.chdir(ddir.split(sep='/')[0])
        os.chdir('..')
    except OSError:
        raise Warning('need "' + ddir.split(sep='/')[0] +
                      '" subdir for storing the data')

    # plttrange = np.linspace(t0, tE, 101)
    # plttrange = None

    try:
        with open(ddir+data_prfx+'velstrs.json', 'r') as f:
            velstrs = json.load(f)
        if debug:
            raise FileNotFoundError()
        logging.info('loaded FEM velocity data')
    except FileNotFoundError as e:
        logging.debug(e, exc_info=True)
        logging.info('computing FEM velocity data')
        soldict = stokesmatsc  # containing A, J, JT
        soldict.update(femp)  # adding V, Q, invinds, diribcs
        soldict.update(trange=trange, dataoutpnts=dataoutpnts)
        # , datatrange=datatrange)
        # adding time integration params
        soldict.update(fv=rhsd['fv'], fp=rhsd['fp'],
                       N=N, nu=nu,
                       start_ssstokes=True,
                       get_datastring=None,
                       treat_nonl_explicit=True,
                       dbcinds=femp['dbcinds'], dbcvals=femp['dbcvals'],
                       data_prfx=ddir+data_prfx,
                       # paraviewoutput=ParaviewOutput,
                       # plttrange=plttrange, prvoutpnts=prvoutpnts,
                       vfileprfx=proutdir+'vel_',
                       pfileprfx=proutdir+'p_')

        velstrs = snu.solve_nse(return_dictofvelstrs=True,
                                **soldict)
        with open(ddir+data_prfx+'velstrs.json', 'w') as f:
            json.dump(velstrs, f)

    datadict = {}
    logging.info('interpolating and saving the data')
    cfignum = 0
    with open(geodata) as f:
        domaindata = json.load(f)
    bbdict = domaindata['bounding box']  # bounding box of the domain
    xlims = [bbdict['xone'][0], bbdict['xtwo'][0]]
    ylims = [bbdict['xone'][1], bbdict['xfour'][1]]

    vxmins, vxmaxs, vymins, vymaxs = [], [], [], []

    for itn, ckey in enumerate(velstrs.keys()):
        # curvvec = np.load(tstvstr)
        cvvec = np.load(velstrs[ckey]+'.npy')

        # xmshpoints = 15 + 20*16  # this should k*16+15 for some k
        # ymshpoints = 15 + 8*16  # this should k*16+15 for some k

        xdata, ydata, vmmdct = nfu.\
            vvec_to_datachannels(cvvec, V=femp['V'], xlims=xlims, ylims=ylims,
                                 xmshpoints=xmshpoints, ymshpoints=ymshpoints,
                                 ret_minmax=True)
        vxmins.append(vmmdct['vxmin'])
        vymins.append(vmmdct['vymin'])
        vymaxs.append(vmmdct['vymax'])
        vxmaxs.append(vmmdct['vxmax'])

        if np.mod(itn+1, int(dataoutpnts/10)) == 0 or ckey == 'mean':
            logging.info('done with {0}/{1}'.format(itn+1, dataoutpnts))
            if plotplease or pngplease:
                plt.figure(cfignum, figsize=(4, 2))
                cfignum += 1
                plt.imshow(xdata, extent=[xlims[0], xlims[1],
                                          ylims[0], ylims[1]],
                           # vmin=vmin, vmax=vmax,
                           cmap=plt.get_cmap('gist_earth'))
                plt.title('$t={0}$'.format(ckey))
                if pngplease:
                    plt.savefig('plots/{0}.png'.format(cfignum))
        datadict.update({ckey: dict(vvec=cvvec.tolist(),
                                    vmatx=xdata.tolist(),
                                    vmaty=ydata.tolist())})

    vxmin = np.min(np.array(vxmins))
    vymin = np.min(np.array(vymins))

    vxmax = np.max(np.array(vxmaxs))
    vymax = np.max(np.array(vymaxs))

    datadict.update({'geometry': dict(xmin=0, xmax=5, ymin=0, ymax=1,
                                      xmshpoints=xmshpoints,
                                      ymshpoints=ymshpoints)})
    datadict.update({'velstrs': velstrs})
    datadict.update({'meshfile': os.path.abspath(meshfile),
                     'physregs': os.path.abspath(physregs),
                     'geodata': os.path.abspath(geodata),
                     'femscheme': scheme})
    # The Maxima/Minima of the field
    datadict.update({'velmaxima': dict(vxmin=vxmin, vxmax=vxmax,
                                       vymax=vymax, vymin=vymin)})
    with open(outputfile, 'w') as outfile:
        json.dump(datadict, outfile)
        logging.info('saved data and fem info to: ' + outputfile)
    if plotplease:
        plt.show()

    # print('for plots check \nparaview ' + proutdir + 'vel___timestep.pvd')
    # print('or \nparaview ' + proutdir + 'p___timestep.pvd')


if __name__ == '__main__':
    directory_generator("cached-data") 
    directory_generator("train-data")
    scaletest = 8.
    mshprfx = ('mesh/karman2D-outlets')
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--meshprefix", type=str,
                        help="prefix for the mesh files",
                        default=mshprfx)
    parser.add_argument("--meshlevel", type=int,
                        help="mesh level", default=1)
    parser.add_argument("--Re", type=int,
                        help="Reynoldsnumber", default=40)
    parser.add_argument("--tE", type=float,
                        help="final time of the simulation", default=1.)
    parser.add_argument("--Nts", type=float,
                        help="number of time steps", default=1200)
    parser.add_argument("--scaletest", type=float,
                        help="scale the test size", default=scaletest)
    parser.add_argument("--paraviewframes", type=int,
                        help="number of outputs for paraview", default=100)
    parser.add_argument("--datapoints", type=int,
                        help="number of data output points", default=1000)
    parser.add_argument("--outputdata", type=str,
                        help="file name of the output",
                        default='train-data/firsttry.json')
    parser.add_argument("--xydims", type=str,
                        help="dimensions of the input 2D image for the CNN",
                        default='47x63')
    parser.add_argument("--dataprefix", type=str,
                        help=("directory and prefix for " +
                              "the cached simulation data"),
                        default='cached-data/nn-')
    args = parser.parse_args()
    logging.info(args)
    scheme = 'TH'
    # disable all debug info from matplotlib
    # logging.getLogger('matplotlib').setLevel(logging.WARNING)

    testit(Re=args.Re,
           meshprfx=args.meshprefix, meshlevel=args.meshlevel,
           outputfile=args.outputdata,
           t0=0., tE=args.scaletest*args.tE,
           Nts=int(args.scaletest*args.Nts),
           dataoutpnts=args.datapoints,
           ddir=args.dataprefix,
           xydims=args.xydims,
           scheme=scheme, ParaviewOutput=True, prvoutpnts=args.paraviewframes)
