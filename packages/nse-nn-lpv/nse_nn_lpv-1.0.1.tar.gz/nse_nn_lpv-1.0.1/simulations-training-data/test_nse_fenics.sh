# SCLTST=500
# PRVFRM=700
# MSHPRFX='mesh/2D-double-rotcyl'

MSHDIR='mesh/'
MSHNAM='karman2D-outlets'
MSHPRFX=${MSHDIR}${MSHNAM}
MSHLVL=1
RE=40

NTS=1200
TE=1
SCLTST=.5
SCLDTE=${SCLTST}
PRVFRM=20
DTPTS=100
XYDIM='63x127'

# OUTPUTFILE='train-data/0-'${SCLDTE}'_'${DTPTS}'_'${XYDIM}'_cntrd.json'
OUTPUTFILE='train-data/0-'${SCLDTE}'_'${DTPTS}'_'${XYDIM}'.json'

python3 time_dep_nse_generic.py \
    --meshprefix ${MSHPRFX} --meshlevel ${MSHLVL} \
    --Re ${RE} --Nts ${NTS} --tE ${TE} --scaletest ${SCLTST} \
    --datapoints ${DTPTS} --outputdata ${OUTPUTFILE} --xydim=${XYDIM} \
    --paraviewframes ${PRVFRM}
# --centered
