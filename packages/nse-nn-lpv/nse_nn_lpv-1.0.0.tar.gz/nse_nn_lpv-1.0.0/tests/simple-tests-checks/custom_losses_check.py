import numpy as np
import scipy.sparse as sps

import torch
import torch.nn as nn
import torch.nn.functional as tnf

# import nse_nn_lpv.CNN_utils as cnu


class LocFEMLoss(nn.Module):
    def __init__(self, mmat=None, tmmat=None, podbas=None):
        '''
        mmat ... (n, n) scipy.sparse mass matrix in COO format
        podbas ... (n, k) np.array
        '''
        super(LocFEMLoss, self).__init__()
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
            self.podbas = podbas
        else:
            self.podbas = torch.from_numpy(podbas).float()

    def forward(self, vvecone, vvectwo):
        ''' FEM norm over a full batch as

        1. `[[v11], [v12]]` to a matrix `V = [v1 v2]`
        2. multiply by `M`: `MV = [Mv1 Mv2]`
        3. compute pointwise product `V.*M = [v1.*Mv1 v2.*Mv2]`
        4. sum over elements = sum of the inner products `v1Mv1+v2Mv2`
        5. divide 0.5 and by number of batches -- average over batch
        '''

        Nbatch = vvecone.shape[0]

        if self.podbas is None:
            vvecdiff = (vvecone - vvectwo).view([Nbatch, -1]).T
        else:
            liftedv = self.podbas.matmul(vvecone.view([Nbatch, -1]).T)
            vvecdiff = liftedv - vvectwo.view([Nbatch, -1]).T

        mvvd = self.ttmmat.matmul(vvecdiff)
        return (1./(2*Nbatch)*torch.mul(vvecdiff, mvvd)).sum()


class MiniNN(nn.Module):
    def __init__(self, code_in, code_out=None):
        super().__init__()  # similar for Python 3
        code_out = code_in if code_out is None else code_out
        self.layerone = nn.Linear(code_in, code_out)

    def forward(self, x):
        x = tnf.elu(self.layerone(x.view([1, -1])))
        return x


N = 4
Nbatch = 2
mmat = 3*sps.eye(N) - \
    sps.diags(np.ones((N-1, )), -1) - sps.diags(np.ones((N-1, )), 1)
mmat = mmat.tocoo()

mmtdns = mmat.toarray()
tmmat = torch.from_numpy(mmtdns).float().to_sparse()


# xone = torch.randn(N, requires_grad=True)
xone = torch.ones((Nbatch, N, 1), requires_grad=True)
xtwo = torch.randn((Nbatch, N, 1), requires_grad=True)
# y = x.sum()
# y.backward()

# femloss = LocFEMLoss(tmmat=tmmat)
femloss = LocFEMLoss(mmat=mmat, podbas=np.eye(N))
# lossx = femloss(xone, 0*xtwo)
lossx = femloss(xone, xtwo)
# lossx = xone.sum()
# lossx = torch.norm(xone)
lossx.backward()

print(xone.grad)
print(xone)
print(1/Nbatch * tmmat @ (xone-xtwo).view([Nbatch, -1]).T)

raise UserWarning()

# k = 20
N = 100
# snapshots = np.random.randn(self.n, self.k)
mmat = 3*sps.eye(N, format='csr') - \
    sps.diags(np.ones((N-1, )), -1) - sps.diags(np.ones((N-1, )), 1)
vveco = np.linspace(0, 1, N).reshape((N, 1))
vvect = np.linspace(1, 0, N).reshape((N, 1))
vvecone = torch.from_numpy(vveco).float()
vvectwo = torch.from_numpy(vvect).float()

femloss = LocFEMLoss(mmat=mmat)

lossoo = femloss(vvecone, vvecone)
lossot = femloss(vvecone, vvectwo)

mnmodel = MiniNN(N)

optimizer = torch.optim.Adam(mnmodel.parameters())

pred = mnmodel.forward(vvecone)
loss = femloss(pred, vvecone.view([1, -1]))

# Backpropagation
optimizer.zero_grad()
loss.backward()
optimizer.step()
