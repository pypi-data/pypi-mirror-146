import unittest

import numpy as np
import scipy.sparse as sps

import multidim_galerkin_pod.gen_pod_utils as gpu

import torch

import nse_nn_lpv.nse_data_helpers as ndh
# import nse_nn_lpv.CNN_utils as cnnh


class MMatShiftPOD(unittest.TestCase):

    def setUp(self):
        self.k = 20
        self.n = 100
        self.snapshots = np.random.randn(self.n, self.k)
        self.mmat = 3*sps.eye(self.n, format='csr') - \
            sps.diags(np.ones((self.n-1, )), -1) - \
            sps.diags(np.ones((self.n-1, )), 1)

    def test_mmat_pod(self):
        ''' check the handling of mass matrices and how it is optimal

        '''
        khalf = np.int(self.k/2)

        mpodvecs, mprjvecs = gpu.get_podbas_wrtmass(self.snapshots,
                                                    My=self.mmat,
                                                    npodvecs=self.k)
        myfac = gpu.SparseFactorMassmat(self.mmat)

        mockmmat = sps.eye(self.n, format='csr')
        podvecs, prjvecs = gpu.get_podbas_wrtmass(self.snapshots,
                                                  My=mockmmat,
                                                  npodvecs=self.k)

        mockmyfac = gpu.SparseFactorMassmat(mockmmat)

        mmat_check_ppe = ndh.get_check_podprjerror(mmat=self.mmat, myfac=myfac,
                                                   prjvecs=mprjvecs,
                                                   podvecs=mpodvecs)

        mock_check_ppe = ndh.get_check_podprjerror(mmat=mockmmat,
                                                   myfac=mockmyfac,
                                                   prjvecs=prjvecs,
                                                   podvecs=podvecs)
        mxd_mock_check_ppe = ndh.get_check_podprjerror(mmat=self.mmat,
                                                       myfac=mockmyfac,
                                                       prjvecs=prjvecs,
                                                       podvecs=podvecs)
        mpoderr, mockpoderr, mxdpoderr = 0, 0, 0
        for ccol in range(self.k):
            mcvec = torch.from_numpy(myfac.Ft@self.snapshots[:, ccol]).float()
            # ### the `check_ppe` scales with `Ft.inv` first
            mpoderr += mmat_check_ppe(mcvec)
            cvec = torch.from_numpy(self.snapshots[:, ccol]).float()
            mockpoderr += mock_check_ppe(cvec)
            mxdpoderr += mxd_mock_check_ppe(cvec)

        self.assertAlmostEqual(mpoderr, 0.)
        self.assertAlmostEqual(mockpoderr, 0)
        self.assertAlmostEqual(mxdpoderr, 0)

        # ## Check the approximation
        # pod vecs for M=M, error measured in M-norm
        mm_check_ppe = ndh.\
            get_check_podprjerror(mmat=self.mmat, myfac=mockmyfac,
                                  prjvecs=mprjvecs[:, :khalf],
                                  podvecs=mpodvecs[:, :khalf])

        # pod vecs for M=id, error measured in M-norm
        idm_check_ppe = ndh.\
            get_check_podprjerror(mmat=self.mmat,
                                  myfac=mockmyfac,
                                  prjvecs=prjvecs[:, :khalf],
                                  podvecs=podvecs[:, :khalf])

        mpodaerr, mockpodaerr = 0, 0
        for ccol in range(self.k):
            mcvec = torch.from_numpy(myfac.Ft@self.snapshots[:, ccol]).float()
            # ### the `check_ppe` scales with `Ft.inv` first
            mpodaerr += mm_check_ppe(mcvec)
            cvec = torch.from_numpy(self.snapshots[:, ccol]).float()
            mockpodaerr += idm_check_ppe(cvec)
        self.assertNotAlmostEqual(mpodaerr, 0.)
        self.assertNotAlmostEqual(mockpodaerr, 0)
        # the approximation with the M-Pod vectors should be better in the M
        self.assertGreater(mockpodaerr, mockpoderr)


if __name__ == "__main__":
    unittest.main()
