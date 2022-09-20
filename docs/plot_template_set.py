
import os
import warnings
warnings.filterwarnings("ignore")

import numpy as np

import matplotlib.pyplot as plt
from matplotlib import cm
import cmasher as cmr
from astropy.io import ascii

from utils import read_templates

plt.style.use('http://stephenwilkins.co.uk/matplotlibrc.txt')


from synthesizer.grid import parse_grid_id

def plot_template_set_all(template_set_prameter_file, path_to_templates):

    templates = read_templates(template_set_prameter_file, path_to_templates)

    colors = cmr.take_cmap_colors('cmr.tropical', len(templates.keys())) #, cmap_range=(0.15, 0.85)

    left  = 0.15
    bottom = 0.15
    width = 0.8
    height = 0.8

    lam_range = [3, 4]

    fig = plt.figure(figsize = (3.5, 5))
    ax = fig.add_axes((left, bottom, width, height))

    for t, c in zip(templates.values(), colors):
        s = (t.log10lam>lam_range[0])&(t.log10lam<lam_range[1])
        ax.plot(t.log10lam[s], np.log10(t.fnu[s]), lw=1, label = rf'$\rm {t.number}$', color = c)


    ax.legend(fontsize = 6, labelspacing = 0.1)
    template_set_id = '.'.join(template_set_prameter_file.split('.')[:-2])

    ax.set_xlabel(r'$\rm log_{10}(\lambda/\AA)$')
    ax.set_ylabel(r'$\rm log_{10}(L_{\nu}/erg\ s^{-1}\ Hz^{-1} M_{\odot}^{-1})$')

    fig.savefig(f'figs/{template_set_id}_all.pdf')
    fig.savefig(f'figs/{template_set_id}_all.png')


def plot_template_comparison(default_template_set_prameter_file, template_set_prameter_file, path_to_templates):

    default_templates = read_templates(default_template_set_prameter_file, path_to_templates)
    templates = read_templates(template_set_prameter_file, path_to_templates)

    colors = cmr.take_cmap_colors('cmr.tropical', len(templates.keys())) #, cmap_range=(0.15, 0.85)

    left  = 0.15
    bottom = 0.15
    width = 0.8
    height = 0.8

    lam_range = [3, 4]

    fig = plt.figure(figsize = (3.5, 5))
    ax = fig.add_axes((left, bottom, width, height))

    for dt, t, c in zip(default_templates.values(), templates.values(), colors):

        s = (t.log10lam>lam_range[0])&(t.log10lam<lam_range[1])
        ax.plot(t.log10lam[s], np.log10(t.fnu[s]/dt.fnu[s]), lw=1, label = rf'$\rm {t.number}$', color = c, alpha = 0.5)


    ax.legend(fontsize = 6, labelspacing = 0.1)
    template_set_id = '.'.join(template_set_prameter_file.split('.')[:-2])

    ax.axhline(0.0, c='k',alpha=0.1, lw=3)
    ax.set_ylim([-1.49, 1.49])
    ax.set_xlabel(r'$\rm log_{10}(\lambda/\AA)$')
    ax.set_ylabel(r'$\rm log_{10}(L_{\nu}/L_{\nu}^{default})$')

    fig.savefig(f'figs/{template_set_id}_comparison.pdf')
    fig.savefig(f'figs/{template_set_id}_comparison.png')




def plot_template_set_individual(template_set_prameter_file, path_to_eazy):

    lam_range = [3, 4]

    templates = read_templates(template_set_prameter_file, path_to_eazy)

    colors = cmr.take_cmap_colors('cmr.tropical', len(templates.keys())) #, cmap_range=(0.15, 0.85)

    fig, axes = plt.subplots(3,4, figsize = (7,5), sharex = True, sharey = True)

    left  = 0.125  # the left side of the subplots of the figure
    right = 0.9    # the right side of the subplots of the figure
    bottom = 0.1   # the bottom of the subplots of the figure
    top = 0.9      # the top of the subplots of the figure
    wspace = 0.0   # the amount of width reserved for blank space between subplots
    hspace = 0.0   # the amount of height reserved for white space between subplots

    fig.subplots_adjust(left=left, bottom=bottom, right=right, top=top, wspace=wspace, hspace=hspace)

    for ax, t, c in zip(axes.flatten(), templates.values(), colors):
        s = (t.log10lam>lam_range[0])&(t.log10lam<lam_range[1])
        ax.plot(t.log10lam[s], np.log10(t.fnu[s]), lw=1, label = rf'$\rm {t.number}$', color = c)

        ax.set_ylim([16.01, 22.99])

    template_set_id = '.'.join(template_set_prameter_file.split('.')[:-2])



    # ax.set_xlabel(r'$\rm log_{10}(\lambda/\AA)$')
    # ax.set_ylabel(r'$\rm log_{10}(L_{\nu}/erg\ s^{-1}\ Hz^{-1} M_{\odot}^{-1})$')

    fig.savefig(f'figs/{template_set_id}_individual.pdf')
    fig.savefig(f'figs/{template_set_id}_individual.png')


def create_page(grid_id):

    grid_id_k = parse_grid_id(grid_id)

    page = f"""
## | {grid_id_k["sps_model"].upper()} | {grid_id_k["sps_model_version"]} | {grid_id_k["imf"]} | {grid_id_k["imf_hmc"]} |
### {grid_id}
![](../figs/Wilkins22_{grid_id}_all.png)
![](../figs/Wilkins22_{grid_id}_individual.png)
![](../figs/Wilkins22_{grid_id}_comparison.png)
    """

    with open(f'pages/Wilkins22_{grid_id}.md','w+') as f:
        f.writelines(page)


    print(f'| {grid_id_k["sps_model"].upper()} | {grid_id_k["sps_model_version"]} | {grid_id_k["imf"]} | {grid_id_k["imf_hmc"]} | [Page](docs/pages/Wilkins22_{grid_id}.md)')



if __name__ == '__main__':


    grid_ids = [
    'bc03_chabrier03',
    'bpass-v2.2.1-bin_100-100',
    'bpass-v2.2.1-bin_100-300',
    'bpass-v2.2.1-bin_135-100',
    'bpass-v2.2.1-bin_135-300',
    'bpass-v2.2.1-bin_135all-100',
    'bpass-v2.2.1-bin_170-100',
    'bpass-v2.2.1-bin_170-300',
    'fsps-v3.2_Chabrier03',
    'bpass-v2.2.1-bin_chab-100',
    'bpass-v2.2.1-bin_chab-300',
    'maraston-rhb_kroupa',
    'maraston-rhb_salpeter',
    'bc03-2016-Stelib_chabrier03',
    # 'bc03-2016-BaSeL_chabrier03',
    # 'bc03-2016-Miles_chabrier03',
    ]


    # --- Generate plots of the template sets in this module

    path_to_templates = '../' # --- templates contained in this module

    default_grid_id = 'fsps-v3.2_Chabrier03'
    # default_grid_id = 'bpass-v2.2.1-bin_chab-100'
    default_template_set_prameter_file = f'Wilkins22_{default_grid_id}.spectra.param'

    for grid_id in grid_ids:

        template_set_prameter_file = f'Wilkins22_{grid_id}.spectra.param'

        plot_template_set_all(template_set_prameter_file, path_to_templates)
        plot_template_set_individual(template_set_prameter_file, path_to_templates)
        plot_template_comparison(default_template_set_prameter_file, template_set_prameter_file, path_to_templates)
        create_page(grid_id)

    # --- Generate plots of other template set


    path_to_templates = os.getenv('EAZY') # --- templates contained in this module

    for template_set_prameter_file in ['Larson22.spectra.param','tweak_fsps_QSF_12_v3.spectra.param']:

        plot_template_set_all(template_set_prameter_file, path_to_templates)
        plot_template_set_individual(template_set_prameter_file, path_to_templates)
        
