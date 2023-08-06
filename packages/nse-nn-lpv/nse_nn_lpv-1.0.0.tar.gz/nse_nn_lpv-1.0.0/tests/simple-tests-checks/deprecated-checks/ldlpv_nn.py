import json

import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim

import numpy as np

# tensorboard writer
# from torch.utils.tensorboard import SummaryWriter
# Normalising data
# from torchvision import transforms

# mats = scipy.io.loadmat('problem-setups/drivencavity__mats_NV3042_Re1.mat')
dtfile = 'data/snapshots_drivencavity_Re500_' +\
    'NV3042_tE3_Nts512_nsnaps512_vels.json'

with open(dtfile) as jsfile:
    velsnapshotdict = json.load(jsfile)

# print(velsnapshotdict.keys())
# sz = len(velsnapshotdict)

# putting the data into one matrix
trngelst = [float(tk) for tk in velsnapshotdict.keys()]
vvelslst = [np.array(vk).flatten() for vk in velsnapshotdict.values()]
vvelsarr = np.array(vvelslst).T
NV = vvelsarr.shape[0]
poddim = 15

nndimlist = [NV, int(NV/4), 2*poddim, poddim, NV]


class dynNet(nn.Module):
    ''' NN with variable numbers of layers and numbers of neurons

    '''

    def __init__(self, nndimlist=None):
        super(dynNet, self).__init__()
        self.nndimlist = nndimlist
        mdlist = nn.ModuleList()
        for i in range(len(nndimlist)-1):
            mdlist.append(nn.Linear(nndimlist[i], nndimlist[i+1]))
        self.mdlist = mdlist

    def forward(self, x):
        for layer in self.mdlist:
            x = F.relu(layer(x))
        return x


dnet = dynNet(nndimlist=nndimlist)
print(dnet)

tstvc = torch.tensor(vvelsarr[:, -1].tolist())
# need the `tolist` to avoid TypeError (why?) when evaluating

msecriterion = nn.MSELoss()
# msecriterion = nn.CrossEntropyLoss()
print('w/o train: loss: ', msecriterion(dnet(tstvc), tstvc))

optimizer = optim.SGD(dnet.parameters(), lr=0.001, momentum=0.9)
traindata = vvelsarr[:, :int(10/9*NV)]  # the first 90% of the time steps
trndtlst = (traindata.T).tolist()
ndata = len(trndtlst)

# crecriterion = nn.CrossEntropyLoss()
# didn't work, why?

for epoch in range(4):
    running_loss = 0
    for i, ctdata in enumerate(trndtlst):
        # zero the parameter gradients (WHY?)
        optimizer.zero_grad()

        # forward + backward + optimize
        ctdtnsr = torch.tensor(ctdata)
        outputs = dnet(ctdtnsr)
        loss = msecriterion(outputs, ctdtnsr)
        loss.backward()
        optimizer.step()

        # print statistics
        running_loss += loss.item()
        if i % int(ndata/10) == int(ndata/10)-1:  # print every 10-th batch
            print('[%d, %5d] loss: %.3f' %
                  (epoch + 1, i + 1, running_loss / int(ndata/10)))
            running_loss = 0.0

print('w/ train: CREloss: ', msecriterion(dnet(tstvc), tstvc))

# test loss
