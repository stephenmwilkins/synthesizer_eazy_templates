

import numpy as np

from synthesizer.grid_sw import Grid
from synthesizer.binned import sfzh, binned

from pathlib import Path


param_file = []


class TemplateGenerator:

    def __init__(self, sps_grid, cloudy_grid, out_dir = '../templates', template_set_name = 'Wilkins22'):

        self.out_dir = out_dir
        self.sps_grid = sps_grid
        self.template_set_name = template_set_name
        self.grid = Grid(f'{sps_grid}_{cloudy_grid}')
        self.i = 1 # running index of template

        # --- create output path
        Path(f'{self.out_dir}/{self.template_set_name}_{self.sps_grid}').mkdir(parents=True, exist_ok=True)

        # --- create parameter file
        self.param_file = []


    def write_template(self, galaxy, log10age):

        llam = galaxy.spectra['total'].lnu/(galaxy.spectra['total'].lam**2*1E-10*1E11/3E8)

        np.savetxt(f'{self.out_dir}/{self.template_set_name}_{self.sps_grid}/{self.i}.dat', np.array([np.round(galaxy.spectra['total'].lam, 3), np.round(llam, 3)]).T)

        self.param_file.append(f'{self.i} templates/{self.template_set_name}_{self.sps_grid}/{self.i}.dat 1.0 {10**(log10age-9):.2f} 1.0')

        self.i += 1


    def generate_constant_galaxy(self, duration = None, Z = None, fesc = None, fesc_LyA = None, tauV = None):

        """ generate SED for an constant burst including nebular emission and dust """

        # --- define the functional form of the star formation and metal enrichment histories
        sfh = sfzh.SFH.Constant(duration) # constant star formation
        Zh = sfzh.ZH.deltaConstant(Z) # constant metallicity

        # --- get the 2D star formation and metal enrichment history for the given SPS grid. This is (age, Z).
        sfzh_ = sfzh.Binned.sfzh(self.grid.ages, self.grid.metallicities, sfh, Zh)

        galaxy = binned.SEDGenerator(self.grid, sfzh_)
        galaxy.pacman(fesc = fesc, fesc_LyA = fesc_LyA, tauV = tauV)

        self.write_template(galaxy, np.log10(duration))


    def generate_instant_galaxy(self, log10age = None, Z = None):

        """ generate SED for an instantanous burst """

        # --- get the 2D star formation and metal enrichment history for the given SPS grid. This is (age, Z).
        sfzh_ = sfzh.instant(self.grid.log10ages, self.grid.metallicities, log10age, Z)

        galaxy = binned.SEDGenerator(self.grid, sfzh_)

        self.write_template(galaxy, log10age)


    def write_parameter_file(self):

        """ write parameter file """

        with open(f'{self.out_dir}/{self.template_set_name}_{self.sps_grid}.spectra.param', 'w') as f:
            for line in self.param_file:
                f.write(f'{line}\n')



if __name__ == '__main__':


    sps_grids = ['bpass-v2.2.1_chab100-bin']
    cloudy_grid = 'cloudy-v17.0_logUref-2'
    Z = 0.01

    for sps_grid in sps_grids:

        te = TemplateGenerator(sps_grid, cloudy_grid)


        te.generate_constant_galaxy(duration = 1E7, Z = Z, fesc = 0.0, fesc_LyA = 1.0, tauV = 0.0) # 10 Myr + nebular + LyA + no dust
        te.generate_constant_galaxy(duration = 1E7, Z = Z, fesc = 0.0, fesc_LyA = 0.0, tauV = 0.0) # 10 Myr + nebular + no LyA + no dust
        te.generate_constant_galaxy(duration = 1E7, Z = Z, fesc = 1.0, fesc_LyA = 1.0, tauV = 0.0) # 10 Myr + no nebular + no dust

        # --- 100 Myr templates with dust and nebular emission

        for tauV in [0.0, 0.3, 1.0, 3.0]:

            te.generate_constant_galaxy(duration = 1E8, Z = Z, fesc = 0.0, fesc_LyA = 1.0, tauV = tauV)

        # --- instantaneous bursts

        for log10age in [8.0, 8.5, 9.0, 9.5, 9.9]:

            te.generate_instant_galaxy(log10age = log10age, Z = Z)

        te.write_parameter_file()
