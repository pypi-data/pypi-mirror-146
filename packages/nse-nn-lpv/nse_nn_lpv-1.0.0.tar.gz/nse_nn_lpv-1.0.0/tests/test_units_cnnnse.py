import unittest

import numpy as np

import torch

import nse_nn_lpv.CNN_utils as cnnh


class CNNNseHelpers(unittest.TestCase):

    def setUp(self):
        self.k = 20
        self.n = 100
        self.podvecs = np.random.randn(self.n, self.k)
        self.vone = np.random.randn(1, self.k)
        self.tvone = torch.from_numpy(self.vone)
        self.vtwo = np.random.randn(1, self.k)
        self.tvtwo = torch.from_numpy(self.vtwo)
        self.vonetrgt = torch.from_numpy(self.podvecs @ self.vone.T)
        self.myloss = cnnh.get_podbas_mmat_mseloss(self.podvecs)

    def test_single_losses(self):
        # vonetrgt = torch.from_numpy(self.podvecs @ self.vone.T)
        vott = self.vonetrgt.view((1, -1, 1))
        vovoloss = self.myloss(self.tvone.float(), vott)
        print('vone-vone: ', vovoloss.item())
        self.assertAlmostEqual(vovoloss.item(), 0.)
        vtvoloss = self.myloss(self.tvtwo.float(), vott)
        print('vtwo-vone: ', vtvoloss.item())
        self.assertNotAlmostEqual(vovoloss.item(), vtvoloss.item())

    def test_batch_losses(self):
        bvtwo = np.stack([self.vtwo.flatten(), self.vtwo.flatten()])
        tbvtwo = torch.from_numpy(bvtwo)

        bvonetrgt = torch.stack([self.vonetrgt, self.vonetrgt])
        bvtvoloss = self.myloss(tbvtwo.float(), bvonetrgt)
        vtvoloss = self.myloss(self.tvtwo.float(),
                               self.vonetrgt.view((1, -1, 1)))
        print('vtwo-vone: ', vtvoloss.item())
        print('(bvtwo-bvone)/2: ', bvtvoloss.item()/2)
        self.assertAlmostEqual(bvtvoloss.item()/(2*vtvoloss.item()), 1.)


if __name__ == "__main__":
    unittest.main()
