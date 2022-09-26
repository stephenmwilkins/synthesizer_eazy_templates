
import os
import numpy as np
from scipy.stats import linregress
import matplotlib.pyplot as plt
from matplotlib import cm
import cmasher as cmr
from astropy.io import ascii

from utils import read_templates

import flare.plt as fplt
from synthesizer.grid import parse_grid_id


def plot_beta(template_sets):

    n = len(template_sets.keys())

    fig, axes = plt.subplots(n, 1, figsize = (3.5,6), sharex = True)
    plt.subplots_adjust(left=0.3, top=0.975, bottom=0.075, right=0.95, wspace=0.0, hspace=0.0)


    for ax, (template_set_name, templates) in zip(axes, template_sets.items()):

        colors = cmr.take_cmap_colors('cmr.tropical', len(templates.keys())) #, cmap_range=(0.15, 0.85)

        # nm, model, imf = template_set_name.split('_')

        tn = '.'.join(template_set_name.split('.')[:-2])
        tn = '_'.join(tn.split('_')[1:])

        grid_id_k = parse_grid_id(tn)

        ax.text(-0.05, 0.6, f'{grid_id_k["sps_model"].upper()}-{grid_id_k["sps_model_version"]}', fontsize = 7, ha = 'right', transform = ax.transAxes)
        ax.text(-0.05, 0.3, f'{grid_id_k["imf"]}', fontsize = 5, ha = 'right', transform = ax.transAxes)

        for t, c in zip(templates.values(), colors):


            wv = [1300., 2500.]

            s = (t.lam>wv[0])&(t.lam<wv[1])

            slope, intercept, r, p, se = linregress(t.log10lam[s], np.log10(t.fnu[s]))

            beta = slope - 2.0

            ax.axvline(beta, color = c, alpha = 0.7)

        ax.set_xlim([-3.49, 6.99])
        ax.set_yticks([])


    axes[-1].set_xlabel(r'$\rm \beta$')

    fig.savefig(f'figs/beta.pdf')
    fig.savefig(f'figs/beta.png')





if __name__ == '__main__':


    # --- Generate plots of the template sets in this module

    template_sets = {}

    path_to_templates = '../' # --- templates contained in this module

    grid_ids = [
    'bpass-v2.2.1-bin_100-100',
    'bpass-v2.2.1-bin_100-300',
    'bpass-v2.2.1-bin_135-100',
    'bpass-v2.2.1-bin_135-300',
    'bpass-v2.2.1-bin_135all-100',
    'bpass-v2.2.1-bin_170-100',
    'bpass-v2.2.1-bin_170-300',
    'bpass-v2.2.1-bin_chab-100',
    'bpass-v2.2.1-bin_chab-300',
    'fsps-v3.2_Chabrier03',
    'maraston-rhb_kroupa',
    'maraston-rhb_salpeter',
    'bc03_chabrier03',
    'bc03-2016-Stelib_chabrier03',
    'bc03-2016-BaSeL_chabrier03',
    'bc03-2016-Miles_chabrier03',
    ]


    for grid_id in grid_ids:

        template_set_prameter_file = f'Wilkins22_{grid_id}.spectra.param'

        template_sets[template_set_prameter_file] = read_templates(template_set_prameter_file, path_to_templates)


    # --- Generate plots of other template set

    # path_to_templates = os.getenv('EAZY') # --- templates contained in this module
    #
    # for template_set_prameter_file in ['Larson22.spectra.param','tweak_fsps_QSF_12_v3.spectra.param']:
    #     template_sets[template_set_prameter_file] = read_templates(template_set_prameter_file, path_to_templates)


    plot_beta(template_sets)
