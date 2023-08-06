import numpy as np
import scipy.io

import torch
from torch import nn

# torch.set_default_tensor_type(torch.FloatTensor)

# With square kernels and equal stride
m = nn.Conv2d(2, 8, 5, stride=2)
# non-square kernels and unequal stride and with padding
# m = nn.Conv2d(16, 33, (3, 5), stride=(2, 1), padding=(4, 2))
# # non-square kernels and unequal stride and with padding and dilation
# m = nn.Conv2d(16, 33, (3, 5), stride=(2, 1), padding=(4, 2), dilation=(3, 1))
# input = torch.randn(20, 16, 50, 100)
# output = m(input)


velptx = scipy.io.loadmat('./data/veldata.mat')['vxmat']
velpty = scipy.io.loadmat('./data/veldata.mat')['vymat']
velptxy = np.stack([velptx, velpty])
tstset = (torch.from_numpy(velptxy)).float()
tstshp = tstset.shape
ttstset = tstset.reshape((1, tstshp[0], tstshp[1], tstshp[2]))
output = m(ttstset)
