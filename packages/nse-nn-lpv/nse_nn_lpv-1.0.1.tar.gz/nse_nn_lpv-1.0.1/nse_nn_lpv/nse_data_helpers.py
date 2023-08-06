import numpy as np
import matplotlib.pyplot as plt
import json
import logging

import torch
from torch.utils.data import Dataset

__all__ = ['NSEDataSet',
           'NSEDataSetPlain',
           'NSEDataSetPODConv',
           'get_check_podprjerror',
           'get_nse_img_data',
           ]


class NSEDataSet(Dataset):
    def __init__(self, dtchnnll, vvecl, velmaxima={}, scaledata=False):
        # invinds=None,  # bcinds=None, bcvals=None,
        # mscalevelvecs=False, mmatfac=None,
        # shiftvec=None, shiftvelvecs=False,
        # getfvdata=False, fvfun=None,
        # podbasis=None,
        ''' super class for providing the NSE simulation data as torch Dataset

        Parameters
        ----------
        dtchnnll: list
            list of the (interpolated to a tensor grid) data as tuple of two
            arrays `(vx, vy)`
        vvecl: list
            list of the corresponding data as numpy vector
        velmaxima: dict, optional
            A dictionary with keys
             * `vxmin` -- minimal value of x-component of the velocity
             * `vxmax` -- maximal value of x-component of the velocity
             * `vymin` -- minimal value of y-component of the velocity
             * `vymax` -- maximal value of y-component of the velocity
            used to scale the input data onto [-1, 1]
        scaledata: boolean, optional
            whether to scale the data with the numbers of `velmaxima`
            defaults to `False`
        mscalevelvecs: boolean, optional
            whether to scale the velocity vectors (see also `mmatfac`),
            defaults to `False`
        mmatfac: (n, n) scipy.csr matrix, optional
            A factor of the massmatrix. If provided, the loaded velocity
            vectors are premultiplied by it in order to realize `|v|_M` as
            `|mmatfac*v|_2`. Defaults to `None`
        shiftvec: (n, 1) np.array, optional
            a vector that shifts the velocity vectors, defaults to `None`
        shiftvelvecs: boolean, optional
            whether to shift the velocity vectors, defaults to `False`
        podbasis: (n, k) np.array, optional
            a matrix `V` that contains a basis of reduced coordinates to, e.g.,
            realize a convection as `N(v)v ~= N(V*r)v`, defaults to `None`
        getfvdata: boolean, optional
            whether to include the data of `fvfun` see below,
            defaults to `False`
        fvfun: f(v), callable
            a function that returns the convection `f(v)`, defaults to `None`
        invinds, bcinds, bcvals: lists, optional
            lists that contain the coordinates of the inner nodes and
            the boundary nodes and the boundary values for the FEM function
            represented by vvec, default to `None`
            TODO: so far, the bcinds, bcvals are encoded in convfun. Maybe make
            it explicit?
        '''
        self.dtchnnll = dtchnnll
        self.vvecl = vvecl
        # self.invinds = invinds
        # self.bcinds = bcinds
        # self.bcvals = bcvals
        self.scaledata = scaledata
        self.velmaxima = velmaxima
        # self.shiftvec = shiftvec
        # self.shiftvelvecs = shiftvelvecs
        # self.mscalevelvecs = mscalevelvecs
        # self.fvfun = fvfun
        # self.getfvdata = getfvdata
        # self.podbasis = podbasis

        # if self.mscalevelvecs:
        #     ttcolidx = torch.from_numpy(mmatfac.indices)
        #     ttcrowidx = torch.from_numpy(mmatfac.indptr)
        #     ttdata = torch.from_numpy(mmatfac.data)
        #     ttmf = torch.\
        #         _sparse_csr_tensor(ttcrowidx, ttcolidx, ttdata,
        #                            size=mmatfac.shape, dtype=torch.float)
        #     self.torchmmatfac = ttmf
        #     self.mmatfac = mmatfac
        # else:
        #     self.mmatfac = None

    def __len__(self):
        try:
            return len(self.vvecl)
        except TypeError:
            return len(self.dtchnnll)

    def _get_vvec(self, idx):
        return torch.from_numpy(self.vvecl[idx]).float()

    def _get_tnsr(self, idx):
        vimgdt = \
            convert_torchtens(self.dtchnnll[idx],
                              scaledata=self.scaledata, **self.velmaxima)
        return vimgdt


class NSEDataSetPlain(NSEDataSet):
    def __init__(self, dtchnnll, vvecl, velmaxima={}, scaledata=False):
        ''' Class that provides the NSE data as vectors and tensors

        '''
        super().__init__(dtchnnll, vvecl,
                         velmaxima=velmaxima, scaledata=scaledata)

    def __getitem__(self, idx):
        return self._get_tnsr(idx), self._get_vvec(idx)


class NSEDataSetPODConv(NSEDataSet):
    def __init__(self, dtchnnll, vvecl, velmaxima={}, scaledata=False,
                 vvecl_not_shifted=None,
                 cvvl=None,  # vsconv=None,
                 podvconvl=None):
        ''' Class that provides the NSE data as vectors, tensors, and

        the convections parametrized by POD coordinates `rhok`
        in order to estimate
        ```
        N(v)v - sum(rhok*N(tvk)v) - N(vs)v
        ```
        in a loss function

        Parameters
        ----------
        cvvl: list
            of the convection vectors `N(v)v`
        vsconv: sparse array
            the convection matrix of the shiftvector `N(vs)`
        podvconvl: list
            of the convection matrices of the (shifted) POD modes
            `[N(tvk) for tvk in podmodes]`
        vvecl_not_shifted: list
            velocity vectors that where not shifted

        Returns
        -------
         - vdatachannel
         - vvec -- as above
         - vvec_ns -- vvec not shifted
         - convvvec -- `(N(v-vs))*v`
         - podconvvecs -- array of [(N(tvk))*v]

        '''
        super().__init__(dtchnnll, vvecl,
                         velmaxima=velmaxima, scaledata=scaledata)
        self.cvvl = cvvl
        self.vvecl_ns = vvecl_not_shifted
        # self.vsconv = vsconv
        self.podvconvl = podvconvl

    def _get_convvveci(self, idx):
        # return torch.from_numpy(self.cvvl[idx] -
        #                         self.vsconv @ self.vvecl_ns[idx]).float()
        return torch.from_numpy(self.cvvl[idx]).float()

    def _get_podconvvecis(self, idx):
        vveci_ns = self.vvecl_ns[idx]
        # print('in data set vveci:', vveci_ns)
        podcnvvecsl = np.hstack([pdcnv @ vveci_ns for pdcnv in self.podvconvl])
        # print('in data set podconvi[0]:', podcnvvecsl[:, 0])
        return torch.from_numpy(podcnvvecsl).float()

    def _get_vvec_ns(self, idx):
        return torch.from_numpy(self.vvecl_ns[idx]).float()

    def __getitem__(self, idx):
        return self._get_tnsr(idx), \
            (self._get_convvveci(idx), self._get_podconvvecis(idx),
             self._get_vvec(idx), self._get_vvec_ns(idx))


def get_check_podprjerror(mmat=None, myfac=None, prjvecs=None, podvecs=None):
    # podshiftvec=None):
    def check_pod_prjerror(tstvec, poddim=None, ret_rho=False):
        tstvecnp = myfac.solve_Ft(tstvec.view((-1, 1)).numpy())
        # the tstvecs have been multiplied by Ft in the NSEDataSet
        # if podshiftvec is None:
        crho = prjvecs[:, :poddim].T @ tstvecnp
        prjlftv = podvecs[:, :poddim] @ crho
        pdiff = tstvecnp - prjlftv
        # else:
        #     crho = prjvecs[:, :poddim].T @ (tstvecnp - podshiftvec)
        #     prjlftv = podvecs[:, :poddim] @ crho
        #     pdiff = tstvecnp - prjlftv - podshiftvec
        perr = (pdiff.T @ mmat @ pdiff).flatten()[0]
        if ret_rho:
            return perr, crho
        return perr

    return check_pod_prjerror


def batch_avrg_poderr(xbatch, poddim=None, cpe_fn=None):
    accupe = 0
    for x in xbatch:
        accupe += cpe_fn(x, poddim=poddim)
    return accupe/xbatch.shape[0]


def convert_torchtens(nsedatapt, scaledata=False,
                      vxmin=None, vxmax=None, vymin=None, vymax=None):
    velptx = nsedatapt[0]
    velpty = nsedatapt[1]
    if scaledata:
        vxshift = -.5*(vxmax + vxmin)
        velptx = 2./(vxmax-vxmin) * (velptx + vxshift)
        vyshift = -.5*(vymax + vymin)
        velpty = 2./(vymax-vymin) * (velpty + vyshift)
        pass
    else:
        pass
    velptxy = np.stack([velptx, velpty])
    tstset = (torch.from_numpy(velptxy)).float()
    return tstset


def get_nse_img_data(strtodata, plotplease=False, return_vvecs=True):
    ''' extract the simulation data from the json file

    and return as lists

    Parameters
    ---

    strtodata: string
        full path of the json data
    '''

    with open(strtodata) as jsf:
        datadict = json.load(jsf)

    gddct = datadict['geometry']
    xmin, xmax = gddct['xmin'], gddct['xmax'],
    ymin, ymax = gddct['ymin'], gddct['ymax']

    datal = []
    vvcsl = []
    figidx = 0
    for ckey in datadict.keys():
        try:
            # the solution has two components: x and y
            cxdatamat = np.array(datadict[ckey]['vmatx'])
            cydatamat = np.array(datadict[ckey]['vmaty'])
            datal.append((cxdatamat, cydatamat, '{0}'.format(ckey)))
            # the solution as *the real* data vector
            # vvec = np.array(datadict[ckey]['vvec'])
            if plotplease:
                plt.figure(100+figidx)
                plt.imshow(cxdatamat,
                           extent=[xmin, xmax, ymin, ymax],
                           cmap=plt.get_cmap('gist_earth'))
                plt.figure(200+figidx)
                plt.imshow(cydatamat,
                           extent=[xmin, xmax, ymin, ymax],
                           cmap=plt.get_cmap('gist_earth'))
                figidx += 1
            if return_vvecs:
                vvcsl.append(np.array(datadict[ckey]['vvec']).reshape((-1, 1)))
        except (TypeError, KeyError) as e:
            # logging.exception('')
            logging.debug(e)
            logging.debug('Nondata key:' + f'{ckey}')
            pass
        plt.show()

    rttpl = (datal, vvcsl) if return_vvecs else datal

    velfielddata = dict(velstrs=datadict['velstrs'])
    try:
        velfielddata.update(dict(velmaxima=datadict['velmaxima']))
    except KeyError:
        pass

    femdata = dict(meshfile=datadict['meshfile'],
                   physregs=datadict['physregs'],
                   geodata=datadict['geodata'],
                   femscheme=datadict['femscheme'],
                   geometry=gddct)
    return rttpl, femdata, velfielddata


if __name__ == '__main__':
    strtodata = '../simulations-training-data/train-data/firsttry.json'
    get_nse_img_data(strtodata, plotplease=False, single_save=True)
