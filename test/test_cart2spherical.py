# ===============================<>============================================
from math import sqrt
from nac.common import (AtomXYZ, change_mol_units, retrieve_hdf5_data, triang2mtx)
from nac.integrals import (calcMtxOverlapP, calc_transf_matrix)
from nac.schedule.components import create_dict_CGFs
from qmworks.parsers import parse_string_xyz

import h5py
import numpy as np
# ===============================<>============================================
path_hdf5 = 'test/test_files/ethylene.hdf5'

ethylene_str =  \
"""6
molecule
C   -2.580  0.068  0.000
H   -2.047  -0.859  0.000
H   -3.650  0.068  0.000
C   -1.905  1.243  0.000
H   -2.438  2.171  0.000
H   -0.835  1.243  0.000"""


def test_cart2spherical():
    """
    Test to convert the cartesian to spherical representation for ``Cd``
    with the basis DZVP-MOLOPT-SR-GTH of CP2K. It must result in a matrix
    of dimension (25, 30) with the values defined in the test.
    """
    basis_name = "DZVP-MOLOPT-SR-GTH"
    package_name = "cp2k"
    # mol = [AtomXYZ(symbol='se', xyz=[]), AtomXYZ(symbol='cd', xyz=[])]
    mol = [AtomXYZ(symbol='cd', xyz=[])]

    with h5py.File(path_hdf5) as f5:
        mtx_test = calc_transf_matrix(f5, mol, basis_name, package_name)

    print("shape ", mtx_test.shape)
    print("mtx_test ", mtx_test)

    mtx_spher2cart = np.zeros((25, 30))
    cte1 = sqrt(3 / 4)
    # S-orbitals
    mtx_spher2cart[0, 0] = 1
    mtx_spher2cart[1, 1] = 1
    # P-orbitals (order is Py, Pz, Px)
    mtx_spher2cart[2, 3] = 1
    mtx_spher2cart[3, 4] = 1
    mtx_spher2cart[4, 2] = 1

    mtx_spher2cart[5, 6] = 1
    mtx_spher2cart[6, 7] = 1
    mtx_spher2cart[7, 5] = 1

    # D-orbitals. Order in sphericals d_2, d_1, d0, d+1, d+2.
    # Order in cartesians Dxx, Dxy, Dxz, Dyy, Dyz, Dzz.
    mtx_spher2cart[8, 9] = 1   # m=-2 Dxy
    mtx_spher2cart[9, 12] = 1  # m=-1 Dyz
    # m=0 Dz^2 -0.5( Dx^2 + Dy^2)
    mtx_spher2cart[10, 13] = 1
    mtx_spher2cart[10, 8] = -0.5
    mtx_spher2cart[10, 11] = -0.5
    # m=1 Dxz
    mtx_spher2cart[11, 10] = 1
    # m=2 Dx^2 - Dy^2
    mtx_spher2cart[12, 8] = cte1
    mtx_spher2cart[12, 11] = -cte1

    # m=-2 Dxy
    mtx_spher2cart[13, 15] = 1
    # m=-1 Dyz
    mtx_spher2cart[14, 18] = 1
    # m=0 Dz^2 -0.5( Dx^2 + Dy^2)
    mtx_spher2cart[15, 19] = 1
    mtx_spher2cart[15, 14] = -0.5
    mtx_spher2cart[15, 17] = -0.5
    # m=1 Dxz
    mtx_spher2cart[16, 16] = 1
    # m=2 Dx^2 - Dy^2
    mtx_spher2cart[17, 14] = cte1
    mtx_spher2cart[17, 17] = -cte1

    # F-orbitals. Order in sphericals f_3, f_2, f_1, f0, f+1, f+2, f+3.
    # Order in cartesians
    # Fxxx, Fxxy, Fxxz, Fxyy, Fxyz, Fxzz, Fyyy, Fyyz, Fyzz, Fzzz

    # m=-3 Fy(3x^2 - y^2)
    mtx_spher2cart[18, 21] = 1.06066017
    mtx_spher2cart[18, 26] = -0.79056942
    # m=-2 Fxyz
    mtx_spher2cart[19, 24] = 1
    # m=-1 some combination of Fx^2y Fy^3 Fyz^2
    mtx_spher2cart[20, 21] = -0.27386128
    mtx_spher2cart[20, 26] = -0.61237244
    mtx_spher2cart[20, 28] = 1.09544512
    # m=0 Dz^3 - 3/(2 Sqrt(5)) (Dx^2z + Dy^2z )
    mtx_spher2cart[21, 29] = 1
    mtx_spher2cart[21, 22] = -3 / (2 * sqrt(5))
    mtx_spher2cart[21, 27] = -3 / (2 * sqrt(5))
    # m=+1 Some combination of Fx^3 Fxy^2 FxZ^2
    mtx_spher2cart[22, 20] = -0.61237244
    mtx_spher2cart[22, 23] = -0.27386128
    mtx_spher2cart[22, 25] = 1.09544512
    # m=+2 Fz(x^2 - y^2)
    mtx_spher2cart[23, 22] = cte1
    mtx_spher2cart[23, 27] = -cte1
    # m=+3 Fx(x^2 - 3y^2)
    mtx_spher2cart[24, 20] = 0.79056942
    mtx_spher2cart[24, 23] = -1.06066017

    assert np.sum(mtx_test - mtx_spher2cart) < 1e-8


def test_compare_with_cp2k():
    """
    Test overlap matrix transformation from cartesian to spherical
    """
    # Overlap matrix in cartesian coordinates
    basisname = "DZVP-MOLOPT-SR-GTH"
    # Molecular geometry in a.u.
    atoms = change_mol_units(parse_string_xyz(ethylene_str))
    dictCGFs = create_dict_CGFs(path_hdf5, basisname, atoms)
    rs = calcMtxOverlapP(atoms, dictCGFs)
    mtx_overlap = triang2mtx(rs, 48)  # there are 48 Cartesian basis CGFs

    transf_matrix = retrieve_hdf5_data(path_hdf5, ['ethylene/trans_mtx'])[0]
    transpose = np.transpose(transf_matrix)

    test = np.dot(transf_matrix, np.dot(mtx_overlap, transpose))
    expected = np.load('test/test_files/overlap_ethylene_sphericals.npy')

    assert abs(np.sum(test - expected)) > 1e-5


if __name__ == '__main__':
    test_compare_with_cp2k()
