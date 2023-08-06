RE=40  # Reynolds number
TE=1  # End time (we start with 0 by default)
TE=8  # End time (we start with 0 by default)
DTPTS=200  # how many data points to record (for the NN later)
DTPTS=2000  # how many data points to record (for the NN later)
XYDIM='47x63'  # the dimension of the rectangular grid
XYDIM='63x127'  # the dimension of the rectangular grid
TTTRGT='bs'  # 'ss' for state/state and all combis
CSL='3-5-8'  # list of code sizes to check
CHNLSL='2-4-8-10-12'  # list of channel sizes for CNN
FID=1
FIDPRMS='15-10'  # how much and often data is added for focus on ini phase

python3 CNN_pod_check.py \
    --Re ${RE} \
    --dataendtime ${TE} --codesizes=${CSL} \
    --datapoints ${DTPTS} --xydim=${XYDIM} \
    --channelsizes ${CHNLSL} \
    --fid ${FID} --fidparams ${FIDPRMS} \
    --traintesttarget ${TTTRGT}
