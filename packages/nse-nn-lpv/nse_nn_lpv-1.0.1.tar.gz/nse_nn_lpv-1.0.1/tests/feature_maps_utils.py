import logging

import matplotlib.pyplot as plt
import numpy as np

import torch

# disable all debug info from matplotlib
logging.getLogger('matplotlib').setLevel(logging.WARNING)


def plot_feature_maps(DAE_model, tstinput):
    # conv_layer_weights = []
    conv_layers = []
    model_children_list = list(DAE_model.children())

    for modelchild in model_children_list:
        if type(modelchild) == torch.nn.Conv2d:
            conv_layers.append(modelchild)
            # model_weights.append(modelchild.weight)

    # fmps_dataloader = DataLoader(trn_nse_data_plain,
    #                              batch_size=1, shuffle=True)
    # (fmpimage, fmptestvec) = next(iter(fmps_dataloader))

    # pass the image through all the layers
    cnnresults = [conv_layers[0](tstinput)]
    for i in range(1, len(conv_layers)):
        # pass the result from the last layer to the next layer
        cnnresults.append(conv_layers[i](cnnresults[-1]))

    aspctr = 9./16
    cnnfmfignum = 401
    plt.figure(cnnfmfignum, figsize=(5, 2))
    plt.subplot(2, 1, 1)
    plt.imshow(tstinput[0, 0, :, :], aspect=aspctr)
    plt.subplot(2, 1, 2)
    plt.imshow(tstinput[0, 1, :, :], aspect=aspctr)
    ncols = 2
    for cnnlayer in cnnresults:
        cnnfmfignum += 1
        nchannels = cnnlayer.shape[1]
        nrows = np.int(np.ceil(nchannels/ncols))
        fig = plt.figure(cnnfmfignum, figsize=(9, 3))
        axs = fig.subplots(nrows, ncols)
        axs = axs.flatten()

        for kkk in range(nchannels):
            # plt.subplot(nrows, ncols, kkk+1)
            axs[kkk].imshow((cnnlayer[0, kkk, :, :]).detach())
            # , aspect=aspctr)
            axs[kkk].set_aspect(.3)
        ncols = ncols*2

    plt.show()
    return
