

import numpy as np


from astropy.table import Table

from unyt import yr, Myr
from pathlib import Path

from synthesizer.grid import SpectralGrid
from synthesizer.parametric.galaxy import SEDGenerator
from synthesizer.parametric.sfzh import SFH, ZH, generate_sfzh, generate_instant_sfzh
from synthesizer.sed import convert_fnu_to_flam
from unyt import yr, Myr

param_file = []


class TemplateGenerator:

    def __init__(self, sps_grid, cloudy_grid, out_dir='../templates', template_set_name='Wilkins22'):

        self.out_dir = out_dir
        self.sps_grid = sps_grid
        self.template_set_name = template_set_name
        self.grid = SpectralGrid(f'{sps_grid}_{cloudy_grid}')
        self.i = 1  # running index of template

        # --- create output path
        Path(f'{self.out_dir}/{self.template_set_name}/{self.sps_grid}').mkdir(parents=True, exist_ok=True)

        # --- create parameter file
        self.param_file = []

        # --- info list

        self.info_list = []

        # --- create info table
        # self.info_table = Table()

    def write_template(self, galaxy, log10age):

        lam = galaxy.spectra['total'].lam

        llam = convert_fnu_to_flam(lam, galaxy.spectra['total'].lnu)

        np.savetxt(f'{self.out_dir}/{self.template_set_name}/{self.sps_grid}/{self.i}.dat',
                   np.array([lam, llam]).T)

        self.param_file.append(
            f'{self.i} templates/{self.template_set_name}/{self.sps_grid}/{self.i}.dat 1.0 {10**(log10age-9):.2f} 1.0')

        self.i += 1

        # beta = galaxy.spectra['total'].measure_beta()

    def generate_constant_galaxy(self, duration=None, Z=None, fesc=None, fesc_LyA=None, tauV=None):
        """ generate SED for an constant burst including nebular emission and dust """

        # --- define the functional form of the star formation and metal enrichment histories
        sfh = SFH.Constant({'duration': duration})  # constant star formation
        Zh = ZH.deltaConstant({'Z': Z})  # constant metallicity

        # --- get the 2D star formation and metal enrichment history for the given SPS grid. This is (age, Z).
        sfzh = generate_sfzh(self.grid.log10ages, self.grid.metallicities, sfh, Zh)

        galaxy = SEDGenerator(self.grid, sfzh)
        galaxy.pacman(fesc=fesc, fesc_LyA=fesc_LyA, tauV=tauV)

        self.write_template(galaxy, np.log10(duration))

    def generate_instant_galaxy(self, log10age=None, Z=None):
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

    template_set_name = 'Wilkins22-v0.3'

    # sps_grids = [
    #     # 'bc03_chabrier03',
    #     # 'bpass-v2.2.1-bin_100-100',
    #     # 'bpass-v2.2.1-bin_100-300',
    #     # 'bpass-v2.2.1-bin_135-100',
    #     # 'bpass-v2.2.1-bin_135-300',
    #     # 'bpass-v2.2.1-bin_135all-100',
    #     # 'bpass-v2.2.1-bin_170-100',
    #     # 'bpass-v2.2.1-bin_170-300',
    #     # 'fsps-v3.2_Chabrier03',
    #     # 'bpass-v2.2.1-bin_chab-100',
    #     # 'bpass-v2.2.1-bin_chab-300',
    #     # 'maraston-rhb_kroupa',
    #     # 'maraston-rhb_salpeter',
    #     # 'bc03-2016-Stelib_chabrier03',
    #     # 'bc03-2016-BaSeL_chabrier03',
    #     # 'bc03-2016-Miles_chabrier03',
    # ]
    cloudy_grid = 'cloudy-v17.03_log10Uref-2'
    Z = 0.01

    sps_grids = [f'fsps-v3.2_imf3:{imf3:.1f}' for imf3 in np.arange(1.5, 3.1, 0.1)]

    for sps_grid in sps_grids:

        print(sps_grid)

        te = TemplateGenerator(sps_grid, cloudy_grid, template_set_name=template_set_name)

        # # v0.2
        # te.generate_constant_galaxy(duration = 10 * Myr, Z = 0.0001, fesc = 0.0, fesc_LyA = 1.0, tauV = 0.0) # 10 Myr + nebular + LyA + no dust
        # te.generate_constant_galaxy(duration = 10 * Myr, Z = 0.0001, fesc = 0.0, fesc_LyA = 0.0, tauV = 0.0) # 10 Myr + nebular + no LyA + no dust
        # te.generate_constant_galaxy(duration = 10 * Myr, Z = 0.0001, fesc = 1.0, fesc_LyA = 1.0, tauV = 0.0) # 10 Myr + no nebular + no dust
        #
        # # v0.1, v0.2
        # te.generate_constant_galaxy(duration = 10 * Myr, Z = 0.001, fesc = 0.0, fesc_LyA = 1.0, tauV = 0.0) # 10 Myr + nebular + LyA + no dust
        # te.generate_constant_galaxy(duration = 10 * Myr, Z = 0.001, fesc = 0.0, fesc_LyA = 0.0, tauV = 0.0) # 10 Myr + nebular + no LyA + no dust
        # te.generate_constant_galaxy(duration = 10 * Myr, Z = 0.001, fesc = 1.0, fesc_LyA = 1.0, tauV = 0.0) # 10 Myr + no nebular + no dust
        #
        # v0.1, v0.2, v0.3
        te.generate_constant_galaxy(duration=10 * Myr, Z=Z, fesc=0.0,
                                    fesc_LyA=1.0, tauV=0.0)  # 10 Myr + nebular + LyA + no dust
        # 10 Myr + nebular + no LyA + no dust
        te.generate_constant_galaxy(duration=10 * Myr, Z=Z, fesc=0.0, fesc_LyA=0.0, tauV=0.0)
        te.generate_constant_galaxy(duration=10 * Myr, Z=Z, fesc=1.0,
                                    fesc_LyA=1.0, tauV=0.0)  # 10 Myr + no nebular + no dust

        # --- 100 Myr templates with dust and nebular emission

        # v0.1, v0.2, v0.3
        for tauV in [0.0, 0.3, 1.0, 3.0]:
            te.generate_constant_galaxy(duration=100 * Myr, Z=Z, fesc=0.0, fesc_LyA=1.0, tauV=tauV)

        # --- instantaneous bursts

        # v0.1, v0.2, v0.3
        for log10age in [8.0, 8.5, 9.0, 9.5, 10.0]:
            te.generate_instant_galaxy(log10age=log10age, Z=Z)

        # v0.4
        # for Z in [0.001, 0.01]:
        #     te.generate_constant_galaxy(duration = 10 * Myr, Z = Z, fesc = 0.0, fesc_LyA = 1.0, tauV = 0.0) # 10 Myr + nebular + LyA + no dust
        #     te.generate_constant_galaxy(duration = 10 * Myr, Z = Z, fesc = 0.0, fesc_LyA = 0.0, tauV = 0.0) # 10 Myr + nebular + no LyA + no dust
        #     te.generate_constant_galaxy(duration = 10 * Myr, Z = Z, fesc = 1.0, fesc_LyA = 1.0, tauV = 0.0) # 10 Myr + no nebular + no dust
        #
        #     # --- 100 Myr templates with dust and nebular emission
        #     for tauV in [0.0, 0.3, 1.0, 3.0]:
        #         te.generate_constant_galaxy(duration = 100 * Myr, Z = Z, fesc = 0.0, fesc_LyA = 1.0, tauV = tauV)
        #
        #     # --- instantaneous bursts
        #     for log10age in [8.0, 8.5, 9.0, 9.5, 10.0]:
        #         te.generate_instant_galaxy(log10age = log10age, Z = Z)

        # v0.5
        # for Z in [0.0001, 0.01]:
        #     te.generate_constant_galaxy(duration=10 * Myr, Z=Z, fesc=0.0,
        #                                 fesc_LyA=1.0, tauV=0.0)  # 10 Myr + nebular + LyA + no dust
        #     # 10 Myr + nebular + no LyA + no dust
        #     te.generate_constant_galaxy(duration=10 * Myr, Z=Z, fesc=0.0, fesc_LyA=0.0, tauV=0.0)
        #     te.generate_constant_galaxy(duration=10 * Myr, Z=Z, fesc=1.0,
        #                                 fesc_LyA=1.0, tauV=0.0)  # 10 Myr + no nebular + no dust
        #
        #     # --- 100 Myr templates with dust and nebular emission
        #     for tauV in [0.0, 0.3, 1.0, 3.0]:
        #         te.generate_constant_galaxy(duration=100 * Myr, Z=Z,
        #                                     fesc=0.0, fesc_LyA=1.0, tauV=tauV)
        #
        #     # --- instantaneous bursts
        #     for log10age in [8.0, 8.5, 9.0, 9.5, 10.0]:
        #         te.generate_instant_galaxy(log10age=log10age, Z=Z)

        te.write_parameter_file()
