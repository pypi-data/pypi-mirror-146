import numpy as np

import dolfin

import dolfin_navier_scipy.dolfin_to_sparrays as dts
import dolfin_navier_scipy.problem_setups as dnsps

__all__ = ['get_fem_utils',
           'vvec_to_datachannels',
           ]


def get_fem_utils(meshfile=None, physregs=None, geodata=None,
                  scheme=None, Re=1., vtdc_dict=None):
    femp, stokesmatsc, rhsd = \
        dnsps.get_sysmats(problem='gen_bccont', Re=Re, bccontrol=False,
                          scheme=scheme, mergerhs=True,
                          meshparams=dict(strtomeshfile=meshfile,
                                          strtophysicalregions=physregs,
                                          strtobcsobs=geodata))
    mmat = stokesmatsc['M']

    def convfun(vvecone, vvectwo=None, dirizero=False):
        dbcvals = [0]*len(femp['dbcinds']) if dirizero else femp['dbcvals']
        if vvectwo is None:
            nvv = dts.get_convvec(u0_vec=vvecone, V=femp['V'],  # femp=femp,
                                  invinds=femp['invinds'],
                                  dbcinds=femp['dbcinds'], dbcvals=dbcvals)
            return nvv
        else:
            nuv = dts.get_convvec(u0_vec=vvecone, V=femp['V'],
                                  uone_utwo_same=False, utwo_vec=vvectwo,
                                  invinds=femp['invinds'],
                                  dbcinds=femp['dbcinds'], dbcvals=dbcvals)
            return nuv

    def getconvmat(vvec, dirizero=False):
        ''' get the convection matrix N(vvec) and the part that comes from

        the reduction of the Direchlet conditions so that
        `N(v)v = N(v)vi + N(v)vg`, where `vi` is the inner vector and `vg` are
        the boundary values --- note the sign
        '''

        dbcvals = [0]*len(femp['dbcinds']) if dirizero else femp['dbcvals']
        cvm, _, _ = dts.\
            get_convmats(u0_vec=vvec, V=femp['V'], invinds=femp['invinds'],
                         dbcinds=femp['dbcinds'], dbcvals=dbcvals)
        cvmc, bcscomp = dts.\
            condense_velmatsbybcs(cvm, invinds=femp['invinds'],
                                  dbcinds=femp['dbcinds'],
                                  dbcvals=femp['dbcvals'])
        return cvmc, -bcscomp

    if vtdc_dict is not None:
        xlims = [vtdc_dict['xmin'], vtdc_dict['xmax']]
        ylims = [vtdc_dict['ymin'], vtdc_dict['ymax']]

        # TODO: boundary conditions

        def vtdc(vvec):
            return vvec_to_datachannels(vvec, xlims=xlims, ylims=ylims,
                                        xmshpoints=vtdc_dict['xmshpoints'],
                                        ymshpoints=vtdc_dict['ymshpoints'],
                                        V=femp['V'])
    else:
        vtdc = None

    return mmat, convfun, getconvmat, vtdc, femp['invinds']


def vvec_to_datachannels(vvec, xlims=[-1, 1], ylims=[-1, 1],
                         xmshpoints=None, ymshpoints=None, V=None,
                         ret_minmax=False):

    '''interpolating a dolfin function to a regular grid on a rectangle

    Parameters
    ----------
    vvec: numpy array
        vector of the FEM approximation
    V: fenics V-space
        space of the FEM approximation
    xmshpoints, ymshpoints: int
        number of points in the regular grid (per dimension)
    xlims, ylims: iterable of two floats
        containing the spatial extensions of the rectangle
    ret_minmax: boolean, optional
        whether to return the extremal values (can be used to scale the data)
        optional, defaults to `False`

    Notes
    -----
    Coordinates that are included in the rectangle but not in the domain on
    which V is defined are set to zero.
    '''

    # Expand the vector into a (FEniCS) FEM function
    curvfun = dts.expand_vp_dolfunc(V=V, vc=vvec)[0]

    # set up the grid on the rectangle
    xmsh = np.linspace(xlims[0], xlims[1], num=xmshpoints)
    ymsh = np.linspace(ylims[0], ylims[1], num=ymshpoints)

    # lists for the data values
    # note that the function value v(x,y) has two components
    xdatlist = []
    ydatlist = []
    for cxp in xmsh:
        xcdl = []
        ycdl = []
        for cyp in ymsh:
            cpp = dolfin.Point(cxp, cyp)
            try:
                cvval = curvfun(cpp)
            except RuntimeError:
                cvval = [0, 0]
            xcdl.append(cvval[0])
            ycdl.append(cvval[1])
        xdatlist.append(xcdl)
        ydatlist.append(ycdl)
    # turning the list of lists into a numpy array
    xdata = np.array(xdatlist).T
    ydata = np.array(ydatlist).T
    # Transpose to have the first dimension as lateral dimension

    if ret_minmax:
        (xfun, yfun) = curvfun.split(deepcopy=True)
        xfv = xfun.vector().get_local()
        yfv = yfun.vector().get_local()
        vmmdct = dict(vxmin=xfv.min(), vxmax=xfv.max(),
                      vymin=yfv.min(), vymax=yfv.max())

        return xdata, ydata, vmmdct

    else:
        return xdata, ydata
