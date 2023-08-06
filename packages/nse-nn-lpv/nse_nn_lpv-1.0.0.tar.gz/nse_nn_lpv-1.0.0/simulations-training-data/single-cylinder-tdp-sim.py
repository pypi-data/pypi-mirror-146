from time_dep_nse_generic import testit
import numpy as np

mshprfx = 'mesh/karman2D-outlets'
mshlvl = 1  # level of the FEM mesh
re = 40  # Reynolds number of the problem
nts = 1200  # Number of time steps for the simulation
te = 1  # End time (we start with 0 by default)
# scale the test setup (e.g., for a quick test) -- scales both `te` and `nts`
scltst = 2
scldte = scltst*te
scldnts = np.int(np.ceil(scltst*nts))
prvfrm = 20  # how many frames for paraview
dtpts = 200  # how many data points to record (for the NN later)
xydim = '63x127'  # the dimension of the rectangular grid
xydim = '47x63'  # the dimension of the rectangular grid
dataprfx = 'cached-data/cw-'
outputfile = f'train-data/sc_0-{scldte}_{dtpts}_' + xydim + '.json'

testit(Re=re,
       meshprfx=mshprfx, meshlevel=mshlvl,
       t0=0., tE=scldte, Nts=scldnts,
       dataoutpnts=dtpts, xydims=xydim,
       outputfile=outputfile,
       ddir=dataprfx, pngplease=False,
       scheme='TH', ParaviewOutput=False, prvoutpnts=prvfrm)
