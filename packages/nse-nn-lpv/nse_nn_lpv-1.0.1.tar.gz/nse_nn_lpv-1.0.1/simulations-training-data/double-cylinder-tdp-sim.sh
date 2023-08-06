MSHDIR='mesh/double-cylinder/'
MSHNAM='2D-double-rotcyl'
MSHPRFX=${MSHDIR}${MSHNAM}
MSHLVL=2  # level of the FEM mesh 
RE=60

NTS=3072  # 12*2**8
TE=1  # End time (we start with 0 by default)
SCLTST=10  # scale the test setup (e.g., for a quick test) -- scales both $TE and $NTS
SCLDTE=$((${SCLTST}*${TE}))  # the scaled end time
PRVFRM=20  # how many frames for paraview 
DTPTS=200  # how many data points to record (for the NN later)
# XYDIM='47x63'
XYDIM='175x303'  # the dimension of the rectangular grid

OUTPUTFILE='train-data/dbc-'${SCLDTE}'_'${DTPTS}'_'${XYDIM}'.json'
DATAPRFX='cached-data/dbc-'

python3 time_dep_nse_generic.py \
    --meshprefix ${MSHPRFX} --meshlevel ${MSHLVL} \
    --Re ${RE} --Nts ${NTS} --tE ${TE} --scaletest ${SCLTST} \
    --datapoints ${DTPTS} --outputdata ${OUTPUTFILE} --xydim=${XYDIM} \
    --dataprefix ${DATAPRFX} \
    --paraviewframes ${PRVFRM}
# --centered
