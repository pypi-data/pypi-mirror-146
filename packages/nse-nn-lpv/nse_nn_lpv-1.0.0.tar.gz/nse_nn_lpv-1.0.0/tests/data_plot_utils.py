import json

import numpy as np
import matplotlib.pyplot as plt


def plot_ld(ldd=None, cd=1., cl=1., fstr=None, chunks=40,   # cmappara=.5,
            bcprms=[.2, .5, .8],
            labelstr=None, fignum=101, fltrd=10, showplease=False):

    if fstr is not None:
        with open(fstr) as jsf:
            ldd = json.load(jsf)
    else:
        pass

    trange = np.array([np.float(ct) for ct in ldd.keys()])
    drgs = cd*np.array([np.float(cld[1]) for cld in ldd.values()])
    lfts = cl*np.array([np.float(cld[0]) for cld in ldd.values()])
    N = drgs.size
    chnkl = np.int(np.floor(N/chunks))
    # nchnks = chunks - 2*np.int(chunks/10)

    lccmplst, dlcmplst = [], []
    for cbc in bcprms:
        dlcmplst.extend([cbc-.05, cbc+.05])
        lccmplst.extend([cbc]*(chunks+1))

    plt.figure(fignum, figsize=((9, 3)))
    plt.rcParams["axes.prop_cycle"] = \
        plt.cycler("color", plt.cm.plasma(lccmplst))
    for cchnkid in range(chunks):
        line, = plt.plot(drgs[cchnkid*chnkl:(cchnkid+1)*chnkl:fltrd],
                         lfts[cchnkid*chnkl:(cchnkid+1)*chnkl:fltrd],
                         alpha=0.2)
    line, = plt.plot(drgs[cchnkid*chnkl:cchnkid*chnkl+1],
                     lfts[cchnkid*chnkl:cchnkid*chnkl+1],
                     alpha=0.7)
    line.set_label(labelstr)
    plt.xlim(-0.2, -0.12)
    plt.ylim(-0.1, 0.1)
    plt.xlabel('drag')
    plt.ylabel('lift')
    plt.title('Phase portrait of drag and lift')
    plt.legend()
    plt.tight_layout()
    plt.rcParams["axes.prop_cycle"] = \
        plt.cycler("color", plt.cm.plasma(dlcmplst))
    plt.figure(fignum+1, figsize=((9, 3)))
    plt.plot(trange[::fltrd], lfts[::fltrd], alpha=0.3, label=labelstr)
    plt.plot(trange[::fltrd], drgs[::fltrd], alpha=0.3)
    plt.xlabel('time $t$')
    plt.ylabel('drag and lift')
    plt.title('Drag and lift over time')
    plt.tight_layout()
    plt.legend()
    if showplease:
        plt.show()


def dae_model_illustration(CAE_model, chkX):
    from torchviz import make_dot
    _encode_, cpred = CAE_model(chkX)
    # DAE_model structure illustration
    targetfolder = "/content/drive/MyDrive/MPI Internship summer 2021/" +\
        "NetworkStructure"
    encode_63x127_cl248_cs3 = make_dot(_encode_)
    cpred_63x127_cl248_cs3 = make_dot(cpred)
    encode_63x127_cl248_cs3.view('encode_63x127_cl248_cs3', targetfolder)
    cpred_63x127_cl248_cs3.view('cpred_63x127_cl248_cs3', targetfolder)


if __name__ == '__main__':
    rsfldr = 'results/drag-lift-curves/'
    podrs = rsfldr + '_t0.0-30.0_Nts36000_ldlpvPOD_a0.5_k3.json'
    plot_ld(fstr=podrs)
    fomrs = rsfldr + '_t0.0-20.0_Nts24000_FOM.json'
    plot_ld(fstr=fomrs)
    cnnrs = 'results/drag-lift-curves/_cl2-4-8-10-12_cs3_ks5_strd2_pdg1' +\
        '_kpod15_trgt-both_t0.0-12.0_Nts14400_ldlpvCNN_a0.5.json'
    plot_ld(fstr=cnnrs)
    plt.show()
