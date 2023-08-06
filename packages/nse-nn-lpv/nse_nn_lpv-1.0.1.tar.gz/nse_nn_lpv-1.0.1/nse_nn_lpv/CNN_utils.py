import numpy as np

import torch

import torch.nn as nn
import torch.nn.functional as tnf


__all__ = ['comptheshapes',
           'DynamicConvAutoencoder',
           'CNNllPODLoss',
           'FEMLoss',
           'PODConvLoss',
           'get_podbas_mmat_mseloss',
           ]


def comptheshapes(inputdatashape, channellist,
                  stride=2, padding=0, dilation=1, kernelsize=5):
    """Compute the shapes of the data in the CNN a priori

    as with the formulas provided in the pytorch docs [1]_

    Parameters
    ----------
    x: tuple
        shape of the initial data point, i.e. (N_batch, C_in, H, W)

    References
    ----------

    ..[1] pytorch.org/docs/1.8.1/generated/torch.nn.Conv2d.html#torch.nn.Conv2d
    """

    layerss = [inputdatashape]
    Nbatch = inputdatashape[0]
    Hin = inputdatashape[2]
    Win = inputdatashape[3]
    for lcn in channellist[1:]:
        flhout = (Hin + 2*padding - dilation*(kernelsize-1) - 1)/stride + 1
        Hout = np.int(np.floor(flhout))
        flwout = (Win + 2*padding - dilation*(kernelsize-1) - 1)/stride + 1
        Wout = np.int(np.floor(flwout))
        layerss.append((Nbatch, lcn, Hout, Wout))
        Hin, Win = Hout, Wout

    return layerss


class DynamicConvAutoencoder(nn.Module):
    """ CNN encoder/decoder of variable sizes/channels

    Parameters:
    -----------

    sngl_lnr_lyr_dec : bool, optional
        whether the decoding is a single linear layer (without activation)
        defaults to `False`
    sll_code_size : int, optional
        size of the output layer in the `sngl_lnr_lyr_dec` case

    Notes:
    ------

    A fully dynamic implementation (nested) makes the structure of the network
    less accessible to, e.g., `pytorch`'s `save` routines. That's why a few
    common cases like 1, 2, 3, or 4 convolutional layers are coded explicitly.
    """

    def __init__(self, code_size, channellist=None, stride=None,
                 kernelsize=None, padding=None, cnnaeoutshape=None,
                 sngl_lnr_lyr_dec=False, sll_decode_size=None):
        # super(ConvAutoencoder, self).__init__()
        super().__init__()  # similar for Python 3
        self.code_size = code_size
        self.stride = stride
        self.ks = kernelsize
        self.channellist = channellist
        self.cnnparams = dict(kernel_size=self.ks, stride=self.stride,
                              padding=padding)
        nncnnaeout = cnnaeoutshape[1]*cnnaeoutshape[2]*cnnaeoutshape[3]
        self.cnnaeoutnn = nncnnaeout
        self.cnnaeoutheight = cnnaeoutshape[2]
        self.cnnaeoutwidth = cnnaeoutshape[3]

        # Encoder
        if len(channellist) >= 2:
            self.encconv1 = nn.Conv2d(channellist[0], channellist[1],
                                      **self.cnnparams)
        if len(channellist) >= 3:
            self.encconv2 = nn.Conv2d(channellist[1], channellist[2],
                                      **self.cnnparams)
        if len(channellist) >= 4:
            self.encconv3 = nn.Conv2d(channellist[2], channellist[3],
                                      **self.cnnparams)
        if len(channellist) >= 5:
            self.encconv4 = nn.Conv2d(channellist[3], channellist[4],
                                      **self.cnnparams)
        if len(channellist) >= 6:
            self.cvenclayers = []
            for layerid in range(len(channellist)-1):
                self.cvenclayers.append(nn.Conv2d(channellist[layerid],
                                                  channellist[layerid+1],
                                                  **self.cnnparams))
        self.fcenc = nn.Linear(self.cnnaeoutnn, self.code_size)

        # Decoder
        self.sngl_lnr_lyr_dec = sngl_lnr_lyr_dec
        if sngl_lnr_lyr_dec:
            self.sll_decode_size = sll_decode_size
            # a single linear layer for decoding
            self.decll = nn.Linear(self.code_size, self.sll_decode_size)
        else:
            self.fcdec = nn.Linear(self.code_size, self.cnnaeoutnn)
            self.cvdeclayers = []
            for layerid in reversed(range(len(channellist)-1)):
                self.cvdeclayers.\
                    append(nn.ConvTranspose2d(channellist[layerid+1],
                                              channellist[layerid],
                                              **self.cnnparams))

    def encode(self, x):
        # FeatureMaps = []
        Nbatch = x.size(0)
        if len(self.channellist) == 2:
            x = tnf.elu(self.encconv1(x))
        elif len(self.channellist) == 3:
            x = tnf.elu(self.encconv1(x))
            x = tnf.elu(self.encconv2(x))
        elif len(self.channellist) == 4:
            x = tnf.elu(self.encconv1(x))
            x = tnf.elu(self.encconv2(x))
            x = tnf.elu(self.encconv3(x))
        elif len(self.channellist) == 5:
            x = tnf.elu(self.encconv1(x))
            x = tnf.elu(self.encconv2(x))
            x = tnf.elu(self.encconv3(x))
            x = tnf.elu(self.encconv4(x))
        else:
            for cvenclayer in self.cvenclayers:
                # print('enc-in: shape x:', x.shape)
                x = tnf.elu(cvenclayer(x))
                # print('enc-out: shape x:', x.shape)
                # FeatureMaps.append(x)
        x = x.view([Nbatch, 1, -1])  # vectorize per batch (=x.size(0))
        # write to last dimension so that the linear layer picks it up
        x = tnf.elu(self.fcenc(x))
        return x  # , FeatureMaps

    def decode(self, x):
        if self.sngl_lnr_lyr_dec:
            return self.decll(x)
        else:
            Nbatch = x.size(0)
            x = tnf.elu(self.fcdec(x))
            x = x.view([Nbatch, self.channellist[-1],
                        self.cnnaeoutheight, self.cnnaeoutwidth])
            # reshape to tensor (as it came out of the CNN part of the encoder)
            for cvdeclayer in self.cvdeclayers:
                x = tnf.elu(cvdeclayer(x))
            return x

    def forward(self, x):
        # gofx, FeatureMaps = self.encode(x)
        gofx = self.encode(x)
        invgofx = self.decode(gofx)
        return gofx, invgofx  # , FeatureMaps


class CNNllPODLoss(nn.Module):
    def __init__(self, mmatfac=None, podbas=None):
        '''
        NOT MAINTAINED CURRENTLY -- see `get_podbas_mmat_mseloss` below
        mmatfac ... mass matrix (factor)
        TODO
        '''
        raise NotImplementedError('not functional at the moment')
        super(CNNllPODLoss, self).__init__()
        # turn numpy sparse array into a torch object
        ttcolidx = torch.from_numpy(mmatfac.indices)
        ttcrowidx = torch.from_numpy(mmatfac.indptr)
        ttdata = torch.from_numpy(mmatfac.data)
        ttmf = torch._sparse_csr_tensor(ttcrowidx, ttcolidx, ttdata,
                                        size=mmatfac.shape, dtype=torch.double)
        self.mmatfac = ttmf
        self.podbas = podbas

    def forward(self, podcoeffs, cvvec):
        pcfs = podcoeffs.detach().numpy().reshape((-1, 1))
        lftpoddif = self.podbas @ pcfs - cvvec
        return (lftpoddif.T @ self.mmat @ lftpoddif).flatten()[0]


class FEMLoss(nn.Module):
    def __init__(self, mmat=None, tmmat=None, podbas=None, prjbas=None):
        '''
        mmat ... (n, n) scipy.sparse mass matrix in COO format
        podbas ... (n, k) np.array
        '''
        super(FEMLoss, self).__init__()
        if tmmat is not None:
            self.ttmmat = tmmat
        elif mmat is not None:
            # turn numpy sparse array into a torch object
            values = mmat.data
            indices = np.vstack((mmat.row, mmat.col))

            i = torch.LongTensor(indices)
            v = torch.FloatTensor(values)
            shape = mmat.shape

            ttmf = torch.sparse.FloatTensor(i, v, torch.Size(shape))
            self.ttmmat = ttmf
        else:
            pass
        if podbas is None:
            self.podbas = None
        else:
            self.podbas = torch.from_numpy(podbas).float()
        if prjbas is None:
            self.prjbas = None
        else:
            self.prjbas = torch.from_numpy(prjbas.T).float()

    def forward(self, vvecone, vvectwo):
        ''' FEM norm over a full batch as

        1. `[[v11], [v12]]` to a matrix `V = [v1 v2]`
        2. multiply by `M`: `MV = [Mv1 Mv2]`
        3. compute pointwise product `V.*M = [v1.*Mv1 v2.*Mv2]`
        4. sum over elements = sum of the inner products `v1Mv1+v2Mv2`
        5. divide by 2 and by number of batches -- average over batch
        '''

        Nbatch = vvecone.shape[0]

        if self.podbas is None:
            vvecdiff = (vvecone - vvectwo).view([Nbatch, -1]).T
        else:
            if self.prjbas is None:
                liftedv = self.podbas.matmul(vvecone.view([Nbatch, -1]).T)
            else:
                prjctdv = self.prjbas.matmul(vvecone.view([Nbatch, -1]).T)
                liftedv = self.podbas.matmul(prjctdv)

            vvecdiff = liftedv - vvectwo.view([Nbatch, -1]).T

        # vvecdiff = vvecdiff.float()
        mvvd = self.ttmmat.matmul(vvecdiff)
        return (1./(2*Nbatch)*torch.mul(vvecdiff, mvvd)).sum()


class PODConvLoss(nn.Module):
    def __init__(self, lytinvmat=None):
        '''
        Parameters
        ---
        lyinvmat, (k, n) np.array
            matrix that realizes the M-1 inner product
        '''
        super(PODConvLoss, self).__init__()
        self.lytinvmat = torch.from_numpy(lytinvmat).float()

    def forward(self, podcoeffs, podconvtargets):
        ''' M-1 norm (with a POD base W) over a full batch as

        1. `[[f1], [f2]]` to a matrix `f = [f1 f2]`
        2. multiply by `W`: `Wf = [Wf1 Wf2]`
        3. compute pointwise square `Wf.^2`
        4. sum over elements = sum of the inner products `f1W.TWf1+f2W.TWf2`
        5. divide by 2 and by number of batches -- average over batch
        '''

        Nbatch = podcoeffs.shape[0]
        nvsmvmatv = podconvtargets[0]
        podconvvecs = podconvtargets[1]

        podconvres = nvsmvmatv - \
            podconvvecs.matmul(podcoeffs.view([Nbatch, -1, 1]))
        lytinvpcr = self.lytinvmat.matmul(podconvres)
        return (1./(2*Nbatch)*torch.mul(lytinvpcr, lytinvpcr)).sum()


def get_podbas_mmat_mseloss(podbas, mmat=None, mmatf=None):
    ''' get a loss function that measures

    `|vk - V*rk|_M`

    where `V` is a (POD) basis for the state, `rk` is the encoded variable,
    and `M` is the mass matrix of the FEM discretization.
    '''

    if mmatf is not None or mmat is not None:
        raise NotImplementedError('pytorch CSR multiplication' +
                                  'not working like I thought')
        # ttcolidx = torch.from_numpy(mmatf.indices)
        # ttcrowidx = torch.from_numpy(mmatf.indptr)
        # ttdata = torch.from_numpy(mmatf.data)
        # ttmf = torch._sparse_csr_tensor(ttcrowidx, ttcolidx, ttdata,
        #                                 size=mmatf.shape, dtype=torch.float)
        # ttpodbas = torch.from_numpy(podbas)
        # ttpodbas = ttpodbas.float()
        # mfttpb = ttmf.matmul(ttpodbas)

    ttpb = torch.from_numpy(podbas).float()
    xdim = podbas.shape[0]

    mselossfn = nn.MSELoss(reduction='sum')

    def podbas_mmat_mseloss(nnoutput, target):
        (bs, cs) = nnoutput.shape
        stackvecasmat = nnoutput.view((bs, cs)).T
        ttpbsvm = ttpb @ stackvecasmat
        return mselossfn(ttpbsvm.T.view((bs, xdim, 1)), target)

    return podbas_mmat_mseloss


# def get_POD_conv_loss(scalemat):
#     def POD_conv_loss(convvec, podconvvecs, podcoeffs):
#         convdiff = convvec - podconvvecs.matmul(podcoeffs)
#         scldcd = scalemat.matmul(convdiff)
#         return torch.norm(scldcd)
#     return POD_conv_loss
