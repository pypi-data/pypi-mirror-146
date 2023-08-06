import numpy as np


def get_traindata_str(t0=0, te=None, num_dtpts=None, xydim=None, Re=None):
    te = np.int(te) if np.round(te) == te else te
    # make te an integer if it is an integer
    return f'sc_{Re}_{t0}-{te}_{num_dtpts}_' + xydim


def get_nnmodel_str(channellist=None, num_pod_vecs=None,
                    stride=None, kernelsize=None, padding=None,
                    code_size=None, target=None):
    modelstr = '_cl' + '-'.join(str(chnl) for chnl in channellist) + \
        f'_cs{code_size}_ks{kernelsize}_strd{stride}_pdg{padding}' + \
        f'_kpod{num_pod_vecs}' + '_trgt-' + target
    return modelstr


def get_lpvsimu_str(t0=0., te=None, Nts=None, Re=None, alpha=None,
                    ldlpv=None, poddim=None, cnnmodstr=None):
    if ldlpv == 'CNN':
        return cnnmodstr + f'RE{Re}_t{t0}-{te}_Nts{Nts}_ldlpv{ldlpv}_a{alpha}'
    elif ldlpv == 'POD':
        return f'RE{Re}_t{t0}-{te}_Nts{Nts}_ldlpv{ldlpv}_a{alpha}_k{poddim}'
    elif ldlpv == 'FOM':
        return f'RE{Re}_t{t0}-{te}_Nts{Nts}_FOM'
    else:
        raise UserWarning("set ldlpv to 'FOM' if no approx is wanted")


def exp_subset_indcs(indices, prcntg=20):
    try:
        fullsz = indices.size
    except AttributeError:
        # seems to be a list
        fullsz = len(indices)
    rdsize = np.int(np.floor(fullsz*prcntg/100))
    lgrng = np.round(np.geomspace(1, fullsz, rdsize))
    # lgrng = np.log(np.arange(fullsz) + 1)
    # rdidx = fullsz - np.ceil(lgrng[:rdsize]/lgrng[rdsize]*fullsz) - 1
    # return # (rdidx[::-1]).astype('int')
    return lgrng.astype('int') - 1


def check_fid(mfid, fid_params, focus_init_data):
    ''' checks if the training had the same focus on the initial data

    '''
    if mfid['focus_init_data'] is focus_init_data:
        if mfid['fid_params'] == fid_params:
            # if ((mfid['fid_params'] == fid_params).sum() == len(fid_params)):
            return True
        else:
            return False
    else:
        return False
