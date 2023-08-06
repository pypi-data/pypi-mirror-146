MSHDIR='mesh/'
MSHNAM='karman2D-outlets'
MSHPRFX=${MSHDIR}${MSHNAM}
MSHLVL=1  # level of the FEM mesh 

RE=40  # Reynolds number of the problem
NTS=1200  # Number of time steps for the simulation

# RE=60  # Reynolds number of the problem
# NTS=1800  # Number of time steps for the simulation

TE=1  # End time (we start with 0 by default)
SCLTST=8  # scale the test setup (e.g., for a quick test) -- scales both $TE and $NTS
SCLDTE=$((${SCLTST}*${TE}))  # the scaled end time
PRVFRM=20  # how many frames for paraview 
DTPTS=2000  # how many data points to record (for the NN later)
XYDIM='63x127'  # the dimension of the rectangular grid
DATAPRFX='cached-data/cw-'

OUTPUTFILE='train-data/sc_'${RE}'_0-'${SCLDTE}'_'${DTPTS}'_'${XYDIM}'.json'

python3 time_dep_nse_generic.py \
    --meshprefix ${MSHPRFX} --meshlevel ${MSHLVL} \
    --Re ${RE} --Nts ${NTS} --tE ${TE} --scaletest ${SCLTST} \
    --datapoints ${DTPTS} --outputdata ${OUTPUTFILE} --xydim=${XYDIM} \
    --dataprefix ${DATAPRFX} \
    --paraviewframes ${PRVFRM}
