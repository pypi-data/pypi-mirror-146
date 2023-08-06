from data_plot_utils import plot_ld
import matplotlib.pyplot as plt
from tikzplotlib import save, clean_figure

CNNplease = False
CNNplease = True
PODplease = False
PODplease = True

dtdct = dict(fltrd=20, fignum=111, bcprms=[.2, .4, .6, .8])

if CNNplease:
    alpha = .33
    fomrs = 'results/drag-lift-curves/RE60_t0.0-50.0_Nts90000_FOM.json'
    plot_ld(fstr=fomrs, labelstr='FOM', **dtdct)

    cs = 3
    fomrs = 'results/drag-lift-curves/' + \
        f'_cl2-4-8-10-12_cs{cs}_ks5_strd2_pdg1_kpod15_trgt-bothRE60' +\
        f'_t0.0-50.0_Nts90000_ldlpvCNN_a{alpha}.json'
    plot_ld(fstr=fomrs, labelstr=f'CNN-{cs}', **dtdct)

    cs = 5
    fomrs = 'results/drag-lift-curves/' + \
        f'_cl2-4-8-10-12_cs{cs}_ks5_strd2_pdg1_kpod15_trgt-bothRE60' +\
        f'_t0.0-50.0_Nts90000_ldlpvCNN_a{alpha}.json'
    plot_ld(fstr=fomrs, labelstr=f'CNN-{cs}', **dtdct)

    cs = 8
    fomrs = 'results/drag-lift-curves/' + \
        f'_cl2-4-8-10-12_cs{cs}_ks5_strd2_pdg1_kpod15_trgt-bothRE60' +\
        f'_t0.0-50.0_Nts90000_ldlpvCNN_a{alpha}.json'
    try:
        plot_ld(fstr=fomrs, labelstr=f'CNN-{cs}', **dtdct)
    except FileNotFoundError:
        pass
    fig = plt.figure(dtdct['fignum'])
    # clean_figure()
    save(f'tikzplots/re60-fomcnn-alpha{alpha}-dlppt.tex')
    fig = plt.figure(dtdct['fignum']+1)
    clean_figure()
    save(f'tikzplots/re60-fomcnn-dlppt-alpha{alpha}-dlvst.tex')
    fig.savefig(f'tikzplots/re60-fomcnn-dlppt-alpha{alpha}-dlvst.png')
    fig.savefig(f'tikzplots/re60-fomcnn-dlppt-alpha{alpha}-dlvst.svg')


if PODplease:
    alpha = .5
    dtdct.update(dict(fignum=222))

    fomrs = 'results/drag-lift-curves/RE60_t0.0-50.0_Nts90000_FOM.json'
    plot_ld(fstr=fomrs, labelstr='FOM', **dtdct)

    cs = 3
    fomrs = 'results/drag-lift-curves/' + \
        f'RE60_t0.0-50.0_Nts90000_ldlpvPOD_a{alpha}_k{cs}.json'
    plot_ld(fstr=fomrs, labelstr=f'POD-{cs}', **dtdct)

    cs = 5
    fomrs = 'results/drag-lift-curves/' + \
        f'RE60_t0.0-50.0_Nts90000_ldlpvPOD_a{alpha}_k{cs}.json'
    plot_ld(fstr=fomrs, labelstr=f'POD-{cs}', **dtdct)

    cs = 8
    fomrs = 'results/drag-lift-curves/' + \
        f'RE60_t0.0-50.0_Nts90000_ldlpvPOD_a{alpha}_k{cs}.json'
    plot_ld(fstr=fomrs, labelstr=f'POD-{cs}', **dtdct)

    fig = plt.figure(dtdct['fignum'])
    # clean_figure()
    save(f'tikzplots/re60-fompod-alpha{alpha}-dlppt.tex')
    fig = plt.figure(dtdct['fignum']+1)
    clean_figure()
    save(f'tikzplots/re60-fompod-dlppt-alpha{alpha}-dlvst.tex')
    fig.savefig(f'tikzplots/re60-fompod-dlppt-alpha{alpha}-dlvst.png')
    fig.savefig(f'tikzplots/re60-fompod-dlppt-alpha{alpha}-dlvst.svg')

    # cs = 12
    # fomrs = 'results/drag-lift-curves/' + \
    #     f'RE60_t0.0-50.0_Nts90000_ldlpvPOD_a{alpha}_k{cs}.json'
    # plot_ld(fstr=fomrs, labelstr=f'POD-{cs} a{alpha}', **dtdct)

# fomrs = 'results/drag-lift-curves/' + \
#     'RE60_t0.0-50.0_Nts90000_ldlpvPOD_a0.5_k5.json'
# plot_ld(fstr=fomrs, labelstr='POD-5 a-.5', fignum=111, fltrd=20)

plt.show()
