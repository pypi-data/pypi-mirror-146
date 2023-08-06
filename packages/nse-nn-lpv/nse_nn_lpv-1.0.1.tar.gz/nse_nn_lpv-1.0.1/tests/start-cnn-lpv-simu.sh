MSHDIR='../simulations-training-data/mesh/'
MSHNAM='karman2D-outlets'
MSHPRFX=${MSHDIR}${MSHNAM}
MSHLVL=1  # level of the FEM mesh 

RE=40  # Reynolds number of the problem
NTS=1200  # Number of time steps for the simulation

# RE=60  # Reynolds number of the problem
# NTS=1800  # Number of time steps for the simulation

TE=1  # End time (we start with 0 by default)
SCLTST=50  # scale the test setup (e.g., for a quick test) -- scales both $TE and $NTS
PRVFRM=200  # how many frames for paraview 

DTTE=8  # End time (we start with 0 by default)
DTPTS=2000  # how many data points to record (for the NN later)
XYDIM='63x127'  # the dimension of the rectangular grid

# LDLPV='FOM'
# LDLPV='FOM'
# LDLPV='POD'
LDLPV='CNN'
ALPHA=.5

TTTRGT='state'  # 'state' for state
TTTRGT='cnvctn'  # 'state' for state
TTTRGT='both'  # 'state' for state

CS=3  # code size to check
CHNLSL='2-4-8-10-12'  # list of channel sizes for CNN
KPOD=15  # number of pod modes for the model output /= code size

python3 CNN_LPV_simulation.py \
    --meshprefix ${MSHPRFX} --meshlevel ${MSHLVL} \
    --Re ${RE} --Nts ${NTS} --tE ${TE} --scaletest ${SCLTST} \
    --alpha ${ALPHA} \
    --paraviewframes ${PRVFRM} \
    --dataendtime ${DTTE} --codesize ${CS} \
    --datapoints ${DTPTS} --xydim ${XYDIM} \
    --channelsizes ${CHNLSL} --kpod ${KPOD} \
    --traintarget ${TTTRGT} --ldlpv ${LDLPV}
