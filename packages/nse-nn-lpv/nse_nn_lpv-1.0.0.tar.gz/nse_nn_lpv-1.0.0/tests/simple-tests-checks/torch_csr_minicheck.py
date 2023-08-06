import numpy as np
import scipy.sparse as sps

import torch

k = 4
m = 3

row = np.array([0, 1, 2, 0])
col = np.array([0, 1, 1, 0])
data = np.array([1., 2., 4., 8.])
spscsr = sps.csr_matrix((data, (row, col)), shape=(m, k))

spsindptr = torch.from_numpy(spscsr.indptr)
col_indices = torch.from_numpy(spscsr.indices)
values = torch.from_numpy(spscsr.data).float()
ttcsr = torch._sparse_csr_tensor(spsindptr, col_indices, values,
                                 dtype=torch.float, size=(m, k))

print(ttcsr.to_dense())
print(spscsr.toarray())

N = 2

xbnp = np.arange(N*k).reshape((N, k, 1))
xbatches = torch.from_numpy(xbnp).float()

print(xbatches)
# print(xbatches.view((N, k)))
# print(xbatches.view((N, k)).T)

xbatchmat = xbatches.view((N, k)).T
print('the right hand side:\n', xbatchmat)
print('the torch sparse tensor:\n', ttcsr.to_dense())
# print(spscsr.toarray())

# ttcxb = ttcsr.to_dense() @ xbatchmat
print('A*x:\n', ttcsr.matmul(xbatchmat))

# print(ttcxb)
# print(ttcxb.view((N, m, 1)))
# print(ttcxb.T.view((N, m, 1)))
# print(ttcsr @ xbatchmat)
# print(torch.sparse.mm(ttcsr, xbatchmat))
# print(spscsr @ xbatchmat.numpy())
