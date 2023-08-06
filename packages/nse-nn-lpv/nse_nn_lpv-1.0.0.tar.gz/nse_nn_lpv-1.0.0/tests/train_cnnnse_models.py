# import torch
import logging
import numpy as np

import nse_nn_lpv.nse_data_helpers as ndh

__all__ = ['check_CNN_POD',
           'train_cnnnse',
           'test_cnnnse']


def check_CNN_POD(testimages=None, testvecs=None, DAE_model=None,
                  myloss=None, code_size=None, check_ppe=None):
    '''
    '''
    # ### CNN Error
    testloss, _ = test_cnnnse(DAE_model, testimages=testimages,
                              testvecs=testvecs, myloss=myloss)
    batch_size = testimages.shape[0]
    # ### POD Error
    avperr = ndh.batch_avrg_poderr(testvecs, poddim=code_size,
                                   cpe_fn=check_ppe)

    return testloss.item()/batch_size, avperr


def test_cnnnse(DAE_model, testimages=None, testvecs=None,
                verbose=True, myloss=None):
    ''' testing the CNN NSE reduction
    '''
    testrho, testtv = DAE_model.forward(testimages)
    testloss = myloss(testtv, testvecs)
    batch_size = testimages.shape[0]
    logging.info(f'Input shape: {testimages.shape}')
    logging.info(f'Output shape: {testtv.shape}')
    logging.info(f'Encoded shape: {testrho.shape}')
    logging.info(f'mymseloss (avrg): {testloss/batch_size}')
    return testloss, testrho


def train_cnnnse(DAE_model, trn_dataloader=None, loss_fun=None, verbose=True,
                 trn_nse_data=None,
                 tst_dataloader=None,
                 num_epochs=None, optimizer_cls=None, lr=None):

    optimizer = optimizer_cls(DAE_model.parameters(), lr=lr)

    size = len(trn_dataloader.dataset)
    nbatches = len(trn_dataloader)
    avrgbatchsize = np.int(np.floor(size/nbatches))
    szw = np.int(np.log10(size) + 1)  # how many digits are needed for logging
    sew = np.int(np.log10(num_epochs) + 1)  # how many digits are needed ...

    for epoch in range(num_epochs):  # loop over the dataset multiple times
        for batch, (X, y) in enumerate(trn_dataloader):

            # Compute prediction and loss
            _, pred = DAE_model.forward(X)
            loss = loss_fun(pred, y)

            # Backpropagation
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

            if np.mod(batch, np.int(nbatches/2)) == 0:
                loss, crnt = loss.item(), batch * avrgbatchsize
                logging.info(f"loss:{loss:.2e} [{crnt:{szw}}/{size}]" +
                             f" -- epoch:{epoch+1:{sew}}/{num_epochs}")

        if tst_dataloader is not None:
            (tstimgd, tstvec) = next(iter(tst_dataloader))
            _, trndcoutput = DAE_model.forward(tstimgd)
            trndloss = loss_fun(trndcoutput, tstvec)
            batch_size = tstimgd.shape[0]
            logging.info(f'trained: mymseloss (avrg): {trndloss/batch_size}')
    logging.info('Finished Training')
