# -*- coding: utf-8 -*-
import numpy as np
try:
    import pandas as pd
except ImportError:
    print("No module pandas.")
from euler_io import rot_matrix, read_euler


def read_parameters(filename='parameters_AlSi10Mg.xlsx', constants=208, temperature=20):
    """
    Read parameters from the excel file.
    :param filename:
    :param constants:
    :param temperature:
    :return:
    """
    parameters = np.zeros(constants)

    for sheet_name in ['parameters']:
        df = pd.read_excel(filename, sheet_name=sheet_name)

    for i in range(len(df['Number'])):
        parameters[df['Number'][i] - 1] = df[temperature][i]

    return parameters


def write_parameters(parameters=[], filename='', format=''):
    if format == 'txt':
        np.savetxt(filename, parameters)
    if format == 'npy':
        np.save(filename, parameters)


def get_grains_parameters(parameters=[], grains_euler=[]):
    """
    Create parameters for grains.
    :param parameters:
    :param grains_euler:
    :return:
    """
    grains_parameters = {}

    grain_id = grains_euler.keys()

    for i in grain_id:
        para = parameters.copy()

        phi1 = grains_euler[i][0]
        Phi = grains_euler[i][1]
        phi2 = grains_euler[i][2]

        rot = rot_matrix(phi1, Phi, phi2)

        para[57 - 1] = rot[0, 0]
        para[58 - 1] = rot[0, 1]
        para[59 - 1] = rot[0, 2]
        para[65 - 1] = rot[1, 0]
        para[66 - 1] = rot[1, 1]
        para[67 - 1] = rot[1, 2]

        grains_parameters[i] = para

    return grains_parameters


def parameters_to_input(grains_parameters=[], grain_prefix='GRAIN_', constants=208, depvar=1000):
    """
    Write parameters to the input file.
    :param grains_parameters:
    :param grain_prefix:
    :param constants:
    :param depvar:
    :return:
    """
    grain_id = grains_parameters.keys()

    outfile = open('materials.inp', 'w')

    outfile.writelines('**\n')
    outfile.writelines('** MATERIALS\n')
    outfile.writelines('**\n')

    for i in grain_id:
        parameters = grains_parameters[i]

        grain_name = grain_prefix + str(i)

        outfile.writelines('*Material, name=%s\n' % grain_name)
        outfile.writelines('*Depvar\n')
        outfile.writelines('%s,\n' % depvar)
        outfile.writelines('*User Material, constants=%s\n' % constants)

        for i in range(constants / 8):
            outfile.writelines('%16f,%16f,%16f,%16f,%16f,%16f,%16f,%16f\n' % (
                parameters[i * 8],
                parameters[i * 8 + 1],
                parameters[i * 8 + 2],
                parameters[i * 8 + 3],
                parameters[i * 8 + 4],
                parameters[i * 8 + 5],
                parameters[i * 8 + 6],
                parameters[i * 8 + 7]))

    outfile.close()


if __name__ == "__main__":
    grains_euler = read_euler(filename='euler.csv')
    parameters = read_parameters(filename='parameters_AlSi10Mg.xlsx',
                                 constants=208,
                                 temperature=20)
    grains_parameters = get_grains_parameters(parameters=parameters,
                                              grains_euler=grains_euler)
    parameters_to_input(grains_parameters=grains_parameters,
                        grain_prefix='GRAIN_',
                        constants=208,
                        depvar=1000)
    write_parameters(parameters=parameters,
                     filename='parameters.txt',
                     format='txt')
    write_parameters(parameters=parameters,
                     filename='parameters.npy',
                     format='npy')

    p = np.load('parameters.npy')
    print(p)
    p = np.loadtxt('parameters.txt')
    print(p)
