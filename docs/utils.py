


import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
import cmasher as cmr
from astropy.io import ascii
from synthesizer.sed import convert_flam_to_fnu

import flare.plt as fplt



class template:
    pass

def read_templates(template_set_prameter_file, path_to_templates):

    """ note templates are assumed to live in a folder called templates in the top-level eazy directory """

    column_names = ['Template number', 'Template file name', 'Lambda_conv', 'Age', 'Template error amplitude']

    params = ascii.read(f'{path_to_templates}/templates/{template_set_prameter_file}', names = column_names)

    templates = {}

    for template_number, template_file_name, template_age in zip(params['Template number'].data, params['Template file name'].data, params['Age'].data):

        lam, flam = np.loadtxt(f'{path_to_templates}/{template_file_name}', unpack = True)

        t = template()
        t.number = template_number
        t.file_name = template_file_name
        t.age = template_age
        t.lam = lam
        t.log10lam = np.log10(lam)
        t.flam = flam
        t.fnu = convert_flam_to_fnu(t.lam, t.flam) # --- convert to f_nu, normalisation doesn't matter

        templates[template_number] = t

    return templates
