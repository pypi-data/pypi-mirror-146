from CNN_pod_check import train_test_PODCNN
from data_handling_utils import get_traindata_str

# te = 8  # End time (we start with 0 by default)
# dtpts = 2000  # how many data points to record (for the NN later)
# xydim = '63x127'  # the dimension of the rectangular grid

te = 8  # End time (we start with 0 by default)
dtpts = 2000  # how many data points to record (for the NN later)
xydim = '47x63'  # the dimension of the rectangular grid
xydim = '63x127'  # the dimension of the rectangular grid
Re = 40  # Reynolds number

trainfor = 'state'
trainfor = 'cnvctn'
trainfor = 'both'
testfor = 'state'
testfor = 'cnvctn'

focus_init_data = True
fid_params = [15, 10]

datastrg = get_traindata_str(te=te, num_dtpts=dtpts, xydim=xydim, Re=Re)
strtodata = '../simulations-training-data/train-data/' + datastrg + '.json'
strtopodbas = './cached-data/pod-bases/' + datastrg
strtocvvecs = './cached-data/conv-vecs/' + datastrg
modelpath = './cached-data/pytorch-models/' + datastrg

csl = [3, 5, 8]  # list of code sizes to check
chnlsl = [2, 4, 8, 10, 12]  # list of channel sizes for CNN

cnnel, podel = \
    train_test_PODCNN(code_size_l=csl,
                      modelpath=modelpath, podmatstr=strtopodbas,
                      cvvecsjsonstr=strtocvvecs, strtodata=strtodata,
                      trainfor=trainfor, testfor=testfor,
                      datadims=xydim, channellist=chnlsl,
                      focus_init_data=focus_init_data, fid_params=fid_params,
                      dataendtime=te, datapoints=dtpts)
