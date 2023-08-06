from data_plot_utils import plot_ld
import matplotlib.pyplot as plt

from tikzplotlib import save, clean_figure

rsfldr = 'results/drag-lift-curves/'
fomrs = rsfldr + '_t0.0-50.0_Nts60000_FOM.json'
for cs in [3, 5, 8]:
    fignum = 111+cs
    plot_ld(fstr=fomrs, labelstr='FOM', fignum=fignum, fltrd=20)
    podrs = rsfldr + f'_t0.0-50.0_Nts60000_ldlpvPOD_a0.5_k{cs}.json'
    plot_ld(fstr=podrs, labelstr=f'POD-{cs}', fignum=fignum)
    cnnrs = rsfldr + f'_cl2-4-8-10-12_cs{cs}_ks5_strd2_pdg1_kpod15_' +\
        'trgt-both_t0.0-50.0_Nts60000_ldlpvCNN_a0.5.json'
    plot_ld(fstr=cnnrs, labelstr=f'CNN-{cs}', fignum=fignum, fltrd=20)

for cs in [3, 5, 8]:
    fig = plt.figure(111+cs)
    # clean_figure()
    save(f'tikzplots/dlppt-cs{cs}.tex')
    fig.savefig(f'tikzplots/dlppt-cs{cs}.svg')
    fig.savefig(f'tikzplots/dlppt-cs{cs}.png')
    fig = plt.figure(111+cs+1)
    clean_figure()
    save(f'tikzplots/dlvst-cs{cs}.tex')
    fig.savefig(f'tikzplots/dlvst-cs{cs}.png')
    fig.savefig(f'tikzplots/dlvst-cs{cs}.svg')

plt.show()
