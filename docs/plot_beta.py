
import os
import numpy as np
from scipy.stats import linregress
import matplotlib.pyplot as plt
from matplotlib import cm
import cmasher as cmr
from astropy.io import ascii

from utils import read_templates

import flare.plt as fplt



def plot_beta(template_sets):

    n = len(template_sets.keys())

    left  = 0.15
    bottom = 0.15
    width = 0.8
    height = 0.1
    # height = 0.8/n


    fig = plt.figure(figsize = (3.5, 3.5))

    for i, (template_set_name, templates) in enumerate(template_sets.items()):


        ax = fig.add_axes((left, bottom + i*height, width, height))

        colors = cmr.take_cmap_colors('cmr.tropical', len(templates.keys())) #, cmap_range=(0.15, 0.85)

        for t, c in zip(templates.values(), colors):


            wv = [1300., 2500.]

            s = (t.lam>wv[0])&(t.lam<wv[1])

            slope, intercept, r, p, se = linregress(t.log10lam[s], np.log10(t.fnu[s]))

            beta = slope - 2.0

            ax.axvline(beta, color = 'k')

        ax.set_xlim([-3.49, 6.99])
        ax.set_yticks([])

        if i == 0:
            ax.set_xlabel(r'$\rm \beta$')
        else:
            ax.set_xticks([])

    fig.savefig(f'figs/beta.pdf')
    fig.savefig(f'figs/beta.png')





if __name__ == '__main__':


    # --- Generate plots of the template sets in this module

    template_sets = {}

    path_to_templates = '../' # --- templates contained in this module

    for sps_grid in ['bpass-v2.2.1_chab100-bin']:

        template_set_prameter_file = f'Wilkins22_{sps_grid}.spectra.param'

        template_sets[template_set_prameter_file] = read_templates(template_set_prameter_file, path_to_templates)


    # --- Generate plots of other template set

    path_to_templates = os.getenv('EAZY') # --- templates contained in this module

    for template_set_prameter_file in ['Larson22.spectra.param','tweak_fsps_QSF_12_v3.spectra.param']:
        template_sets[template_set_prameter_file] = read_templates(template_set_prameter_file, path_to_templates)



    print(template_sets)

    plot_beta(template_sets)
