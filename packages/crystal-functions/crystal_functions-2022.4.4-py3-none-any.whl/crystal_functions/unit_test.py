from asyncore import write


def crystal_input_test(folder_path):
    
    from crystal_functions.file_readwrite import Crystal_input

    import os

    test_attr = []
    test_result = []

    input_file = os.path.join(folder_path,'mgo.d12')  
    mgo_input = Crystal_input(input_file)

    print('File for input testing: %s' %input_file)

    # GEOM BLOCK

    test_attr.append('geom_block')

    geom_block = ['MGO BULK - GEOMETRY TEST\n',
                    'CRYSTAL\n',
                    '0 0 0\n',
                    '225\n',
                    '4.217\n',
                    '2\n',
                    '12 0.    0.    0.\n',
                    '8 0.5   0.5   0.5\n',
                    'END\n']
    if mgo_input.geom_block == geom_block:
        test_result.append(True)
    else:
        test_result.append(False)

    # BS BLOCK

    test_attr.append('bs_block')

    bs_block = ['12 4\n',
                '0 0 8 2.0 1.0\n',
                ' 68370.0 0.0002226\n',
                ' 9661.0 0.001901\n',
                ' 2041.0 0.011042\n',
                ' 529.6 0.05005\n',
                ' 159.17 0.1690\n',
                ' 54.71 0.36695\n',
                ' 21.236 0.4008\n',
                ' 8.791 0.1487\n',
                '0 1 5 8.0 1.0\n',
                ' 143.7 -0.00671 0.00807\n',
                ' 31.27 -0.07927 0.06401\n',
                ' 9.661 -0.08088 0.2092\n',
                ' 3.726 0.2947 0.3460\n',
                ' 1.598 0.5714 0.3731\n',
                '0 1 1 2.0 1.0\n',
                ' 0.688 1.0 1.0\n',
                '0 1 1 0.0 1.0\n',
                ' 0.28 1.0 1.0\n',
                '8 4\n',
                '0 0 8 2.0 1.0\n',
                ' 8020.0 0.00108\n',
                ' 1338.0 0.00804\n',
                ' 255.4 0.05324\n',
                ' 69.22 0.1681\n',
                ' 23.90 0.3581\n',
                ' 9.264 0.3855\n',
                ' 3.851 0.1468\n',
                ' 1.212 0.0728\n',
                '0 1 4 6.0 1.0\n',
                ' 49.43 -0.00883 0.00958\n',
                ' 10.47 -0.0915 0.0696\n',
                ' 3.235 -0.0402 0.2065\n',
                ' 1.217 0.379 0.347\n',
                '0 1 1 0.0 1.0\n',
                ' 0.4764 1.0 1.0\n',
                '0 1 1 0.0 1.0\n',
                ' 0.1802 1.0 1.0\n',
                '99 0\n',
                'ENDBS\n']

    if mgo_input.bs_block == bs_block:
        test_result.append(True)
    else:
        test_result.append(False)

    # FUNC BLOCK

    test_attr.append('func_block')

    func_block = ['DFT\n', 'B3LYP\n', 'XXLGRID\n', 'ENDDFT\n']

    if mgo_input.func_block == func_block:
        test_result.append(True)
    else:
        test_result.append(False)

    test_attr.append('scf_block')

    # SCF BLOCK

    scf_block = [['TOLINTEG\n', '7 7 7 7 14\n'],
                ['SHRINK\n', '12 24\n'],
                ['MAXCYCLE\n', '200\n'],
                ['FMIXING\n', '70\n'],
                'DIIS\n',
                'ENDSCF\n']
    if mgo_input.scf_block == scf_block:
        test_result.append(True)
    else:
        test_result.append(False)

    # ADD GHOST

    mgo_input = Crystal_input(input_file)
    
    test_attr.append('add_ghost')

    mgo_input.add_ghost([1])
    bs_block = ['GHOSTS\n', '1\n', '1\n', 'ENDBS\n']

    if mgo_input.bs_block[-4:] == bs_block:
        test_result.append(True)
    else:
        test_result.append(False)

    # SP TO OPT

    mgo_input = Crystal_input(input_file)
    
    test_attr.append('sp_to_opt')

    mgo_input.sp_to_opt()
    geom_block = ['OPTGEOM\n', 'END\n', 'END\n']

    if mgo_input.geom_block[-3:] == geom_block:
        test_result.append(True)
    else:
        test_result.append(False)
    
    # OPT TO SP

    test_attr.append('opt_to_sp')

    mgo_input.opt_to_sp()
    geom_block = ['MGO BULK - GEOMETRY TEST\n',
                    'CRYSTAL\n',
                    '0 0 0\n',
                    '225\n',
                    '4.217\n',
                    '2\n',
                    '12 0.    0.    0.\n',
                    '8 0.5   0.5   0.5\n',
                    'END\n']

    if mgo_input.geom_block == geom_block:
        test_result.append(True)
    else:
        test_result.append(False)


    return [test_attr, test_result]


def crystal_output_test(folder_path):
    
    from crystal_functions.file_readwrite import Crystal_output

    import numpy as np
    import os

    test_attr = []
    test_result = []

    output_file = os.path.join(folder_path,'mgo.out')  
    mgo_output = Crystal_output(output_file)

    print('File for input testing: %s' %output_file)

    # CONVERGED

    test_attr.append('converged')

    if mgo_output.converged == True:
        test_result.append(True)
    else:
        test_result.append(False)

    # GET DIMENSIONALITY

    test_attr.append('get_dimensionality')

    if mgo_output.get_dimensionality() == 3:
        test_result.append(True)
    else:
        test_result.append(False)

    # GET DIMENSIONALITY

    test_attr.append('get_final_energy')

    if abs(mgo_output.get_final_energy() - (-7495.341792877063)) < 10E-6:
        test_result.append(True)
    else:
        test_result.append(False)

    
    # GET SCF CONVERGENCE

    test_attr.append('get_scf_convergence')
    
    get_scf_convergence_0 = np.array([-7476.83111864, -7489.9832359 , -7494.92298163, -7495.34019539,
       -7495.34166646, -7495.34179102, -7495.34179278, -7495.34179288])
    get_scf_convergence_1 = np.array([-7.48313500e+03, -1.31431062e+01, -4.95247480e+00, -4.16334420e-01,
       -1.47213674e-03, -1.24628212e-04, -1.75513530e-06, -1.02586978e-07])
    
    if abs(np.sum(mgo_output.get_scf_convergence()[0] - get_scf_convergence_0) + \
        np.sum(mgo_output.get_scf_convergence()[1] - get_scf_convergence_1)) < 10E-6:
        test_result.append(True)
    else:
        test_result.append(False)

    # GET NUM CYCLES

    test_attr.append('get_num_cycles')

    if mgo_output.get_num_cycles() == 7:
        test_result.append(True)
    else:
        test_result.append(False)

    # GET FERMI ENERGY

    test_attr.append('get_fermi_energy')

    fermi_energy = -4.13671240282

    if abs(mgo_output.get_fermi_energy() - fermi_energy) < 10E-6:
        test_result.append(True)
    else:
        test_result.append(False)

    # GET PRIMITIVE LATTICE

    test_attr.append('get_primitive_lattice')

    primitive_lattice = np.array([[0.    , 2.1085, 2.1085],
                                    [2.1085, 0.    , 2.1085],
                                    [2.1085, 2.1085, 0.    ]])
    
    if np.all(mgo_output.get_primitive_lattice() == primitive_lattice):
        test_result.append(True)
    else:
        test_result.append(False)

    # GET reciprocal LATTICE

    test_attr.append('get_reciprocal_lattice')

    reciprocal_lattice = np.array([[-1.48996571,  1.48996571,  1.48996571],
                                    [ 1.48996571, -1.48996571,  1.48996571],
                                    [ 1.48996571,  1.48996571, -1.48996571]])
    returned_reciprocal_lattice = np.round(np.array(mgo_output.get_reciprocal_lattice()),8)
    
    if np.all(returned_reciprocal_lattice == reciprocal_lattice):
        test_result.append(True)
    else:
        test_result.append(False)
    
    # GET BAND GAP

    test_attr.append('get_band_gap')

    if abs(mgo_output.get_band_gap() - 7.1237) < 10E-6:
        test_result.append(True)
    else:
        test_result.append(False)
    
    # GET LAST GEOM

    test_attr.append('get_last_geom')

    get_lat_geom_0 = np.array([[0.    , 2.1085, 2.1085],
                                [2.1085, 0.    , 2.1085],
                                [2.1085, 2.1085, 0.    ]])

    get_lat_geom_1 = np.array([12,  8])

    get_lat_geom_2 = np.array([[0.    , 0.    , 0.    ],
                                [2.1085, 2.1085, 2.1085]])

    if np.all(mgo_output.get_last_geom(write_gui_file=False)[0] == get_lat_geom_0) and \
        np.all(mgo_output.get_last_geom(write_gui_file=False)[1] == get_lat_geom_1) and \
        np.all(mgo_output.get_last_geom(write_gui_file=False)[2] == get_lat_geom_2):
        test_result.append(True)
    else:
        test_result.append(False)

    

    '''# 

    test_attr.append('')

    if mgo_output.() == 7:
        test_result.append(True)
    else:
        test_result.append(False)



    # 

    test_attr.append('')

    if mgo_output.() == 7:
        test_result.append(True)
    else:
        test_result.append(False)'''

    

    return [test_attr, test_result]



def test_all(folder_path):

    crystal_input_test_out = crystal_input_test(folder_path)




        