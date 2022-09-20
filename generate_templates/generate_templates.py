

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
        self.i = 1 # running index of template

        # --- create output path
        Path(f'{self.out_dir}/{self.template_set_name}_{self.sps_grid}').mkdir(parents=True, exist_ok=True)

        # --- create parameter file
        self.param_file = []


        # --- info list

        self.info_list = []

        # --- create info table
        # self.info_table = Table()





    def write_template(self, galaxy, log10age):

        llam = convert_fnu_to_flam(galaxy.spectra['total'].lam, galaxy.spectra['total'].lnu)

        np.savetxt(f'{self.out_dir}/{self.template_set_name}_{self.sps_grid}/{self.i}.dat', np.array([np.round(galaxy.spectra['total'].lam, 3), np.round(llam, 3)]).T)

        self.param_file.append(f'{self.i} templates/{self.template_set_name}_{self.sps_grid}/{self.i}.dat 1.0 {10**(log10age-9):.2f} 1.0')

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


    def generate_instant_galaxy(self, log10age = None, Z = None):

        """ generate SED for an instantanous burst """

        # --- get the 2D star formation and metal enrichment history for the given SPS grid. This is (age, Z).
        sfzh = generate_instant_sfzh(self.grid.log10ages, self.grid.metallicities, log10age, Z)

        galaxy = SEDGenerator(self.grid, sfzh)


        self.write_template(galaxy, log10age)


    def write_parameter_file(self):

        """ write parameter file """

        with open(f'{self.out_dir}/{self.template_set_name}_{self.sps_grid}.spectra.param', 'w') as f:
            for line in self.param_file:
                f.write(f'{line}\n')


    def write_info_file(self):

        """ write parameter file """

        with open(f'{self.out_dir}/{self.template_set_name}_{self.sps_grid}.spectra.param', 'w') as f:
            for line in self.param_file:
                f.write(f'{line}\n')




if __name__ == '__main__':


    sps_grids = ['bpass-v2.2.1-bin_chab-100']
    cloudy_grid = 'cloudy-v17.03_log10Uref-2'
    Z = 0.01

    for sps_grid in sps_grids:

        te = TemplateGenerator(sps_grid, cloudy_grid)


        te.generate_constant_galaxy(duration = 10 * Myr, Z = Z, fesc = 0.0, fesc_LyA = 1.0, tauV = 0.0) # 10 Myr + nebular + LyA + no dust
        te.generate_constant_galaxy(duration = 10 * Myr, Z = Z, fesc = 0.0, fesc_LyA = 0.0, tauV = 0.0) # 10 Myr + nebular + no LyA + no dust
        te.generate_constant_galaxy(duration = 10 * Myr, Z = Z, fesc = 1.0, fesc_LyA = 1.0, tauV = 0.0) # 10 Myr + no nebular + no dust

        # --- 100 Myr templates with dust and nebular emission

        for tauV in [0.0, 0.3, 1.0, 3.0]:

            te.generate_constant_galaxy(duration = 100 * Myr, Z = Z, fesc = 0.0, fesc_LyA = 1.0, tauV = tauV)

        # --- instantaneous bursts

        for log10age in [8.0, 8.5, 9.0, 9.5, 9.9]:

            te.generate_instant_galaxy(log10age = log10age, Z = Z)

        te.write_parameter_file()
