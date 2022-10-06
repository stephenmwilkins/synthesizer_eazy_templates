

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

    def __init__(self, sps_grid, cloudy_grid, out_dir = '../templates', template_set_name = 'Wilkins22'):

        self.out_dir = out_dir
        self.sps_grid = sps_grid
        self.template_set_name = template_set_name


        self.grid = SpectralGrid(f'{sps_grid}_{cloudy_grid}')

        # --- create output path
        Path(f'{self.out_dir}/{self.template_set_name}').mkdir(parents=True, exist_ok=True)

        # --- create parameter file
        self.param_file = []

        for i in range(12):
            self.param_file.append(f'{i+1} templates/{self.template_set_name}/fsps_QSF_12_v3_{i+1:03d}.dat 1.0 0.0 1.0')
        self.i = i + 2




    def write_template(self, galaxy, log10age):

        lam = galaxy.spectra['total'].lam

        llam = convert_fnu_to_flam(lam, galaxy.spectra['total'].lnu) * 1E-35

        np.savetxt(f'{self.out_dir}/{self.template_set_name}/{self.i}.dat', np.array([lam, llam]).T)

        self.param_file.append(f'{self.i} templates/{self.template_set_name}/{self.i}.dat 1.0 {10**(log10age-9):.2f} 1.0')

        self.i += 1

        # beta = galaxy.spectra['total'].measure_beta()



    def generate_constant_galaxy(self, duration = None, Z = None, fesc = None, fesc_LyA = None, tauV = None):

        """ generate SED for an constant burst including nebular emission and dust """

        # --- define the functional form of the star formation and metal enrichment histories
        sfh = SFH.Constant({'duration': duration }) # constant star formation
        Zh = ZH.deltaConstant({'Z': Z}) # constant metallicity

        # --- get the 2D star formation and metal enrichment history for the given SPS grid. This is (age, Z).
        sfzh = generate_sfzh(self.grid.log10ages, self.grid.metallicities, sfh, Zh)

        galaxy = SEDGenerator(self.grid, sfzh)
        galaxy.pacman(fesc = fesc, fesc_LyA = fesc_LyA, tauV = tauV)

        self.write_template(galaxy, np.log10(duration))

    def write_parameter_file(self):

        """ write parameter file """

        with open(f'{self.out_dir}/{self.template_set_name}.spectra.param', 'w') as f:
            for line in self.param_file:
                f.write(f'{line}\n')




if __name__ == '__main__':

    template_set_name = 'Augmented-v0.1'

    sps_grid = 'fsps-v3.2_Chabrier03'
    cloudy_grid = 'cloudy-v17.03_log10Uref-2'
    Z = 0.01

    te = TemplateGenerator(sps_grid, cloudy_grid, template_set_name = template_set_name)


    te.generate_constant_galaxy(duration = 10 * Myr, Z = Z, fesc = 0.0, fesc_LyA = 1.0, tauV = 0.0) # 10 Myr + nebular + LyA + no dust
    te.generate_constant_galaxy(duration = 10 * Myr, Z = Z, fesc = 0.0, fesc_LyA = 0.0, tauV = 0.0) # 10 Myr + nebular + no LyA + no dust
    te.generate_constant_galaxy(duration = 10 * Myr, Z = Z, fesc = 1.0, fesc_LyA = 1.0, tauV = 0.0) # 10 Myr + no nebular + no dust

    te.write_parameter_file()
