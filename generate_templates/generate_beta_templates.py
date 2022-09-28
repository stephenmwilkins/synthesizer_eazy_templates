

import numpy as np


from astropy.table import Table

from unyt import yr, Myr
from pathlib import Path

from synthesizer.grid import SpectralGrid
from synthesizer.binned import SFH, ZH, generate_sfzh, generate_instant_sfzh, SEDGenerator
from synthesizer.sed import convert_fnu_to_flam
from unyt import yr, Myr

param_file = []


class TemplateGenerator:

    def __init__(self, sps_grid, cloudy_grid, out_dir = '../templates', template_set_name = 'beta'):

        self.out_dir = out_dir
        self.sps_grid = sps_grid
        self.template_set_name = template_set_name
        self.grid = SpectralGrid(f'{sps_grid}_{cloudy_grid}')
        self.i = 1 # running index of template



        # --- info list

        self.info_list = []

        # --- create info table
        # self.info_table = Table()





    def write_template(self, galaxy, log10age):

        lam = galaxy.spectra['total'].lam

        llam = convert_fnu_to_flam(lam, galaxy.spectra['total'].lnu)

        np.savetxt(f'{self.out_dir}/{self.template_set_name}/{self.sps_grid}/{self.i}.dat', np.array([lam, llam]).T)

        self.param_file.append(f'{self.i} templates/{self.template_set_name}/{self.sps_grid}/{self.i}.dat 1.0 {10**(log10age-9):.2f} 1.0')

        self.i += 1

        # beta = galaxy.spectra['total'].measure_beta()




    def write_parameter_file(self):

        """ write parameter file """








if __name__ == '__main__':

    out_dir = '../templates'
    template_set_name = 'beta'



    # --- create output path
    Path(f'{out_dir}/{template_set_name}').mkdir(parents=True, exist_ok=True)

    # --- create parameter file
    param_file = []


    betas = np.arange(-4., 4., 0.5)

    print(len(betas))

    lam = np.arange(1, 50000) # 1 -> 50,000\AA (0.1 - 5000nm) [0.001-5um]



    for i, beta in enumerate(betas):

        llam = (lam/5500)**beta
        llam[lam<912] = 0.0

        np.savetxt(f'{out_dir}/{template_set_name}/{i}.dat', np.array([lam, llam]).T)

        param_file.append(f'{i} templates/{template_set_name}/{i}.dat 1.0 0.0 1.0')

    # --- save parameter file
    with open(f'{out_dir}/{template_set_name}.spectra.param', 'w') as f:
        for line in param_file:
            f.write(f'{line}\n')
