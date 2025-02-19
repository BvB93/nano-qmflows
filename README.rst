.. image:: https://readthedocs.org/projects/qmflows-namd/badge/?version=latest
   :target: https://qmflows-namd.readthedocs.io/en/latest/?badge=latest
.. image:: https://zenodo.org/badge/DOI/10.5281/zenodo.2576893.svg
   :target: https://doi.org/10.5281/zenodo.2576893
.. image:: https://github.com/SCM-NV/nano-qmflows/workflows/build%20with%20conda/badge.svg
   :target: https://github.com/SCM-NV/nano-qmflows/actions
.. image:: https://codecov.io/gh/SCM-NV/nano-qmflows/branch/master/graph/badge.svg?token=L1W0fPrSUn
   :target: https://codecov.io/gh/SCM-NV/nano-qmflows
.. image:: https://badge.fury.io/py/nano-qmflows.svg
   :target: https://badge.fury.io/py/nano-qmflows

====================
nano-qmflows
====================

Nano-QMFlows is a generic python library for computing (numerically) electronic properties for nanomaterials like the non-adiabatic coupling vectors (NACV) using several quantum chemical (QM) packages.

One of the main problems to calculate (numerically) NACVs by standard QM software is the computation of the overlap matrices between two electronically excited states at two consecutive time-steps that are needed in the numerical differentiation to evaluate the coupling. This happens because most of these softwares are inherently static, i.e. properties are computed for a given structural configuration, and the computation of the overlap matrices at different times requires complicated scripting tools to handle input/outputs of several QM packages.

For further information on the theory behind nano-qmflows and how to use the program see the documentation_.

Installation
------------
Pre-compiled binaries are available on pypi and can be installed on MacOS and Linux as following:

.. code:: bash

   pip install nano-qmflows --upgrade

Building from source
--------------------
Building Nano-QMFlows from source first requires an installation of *Miniconda* as is detailed here_.

.. _here: https://docs.conda.io/en/latest/miniconda.html

Then, to install the **nano-qmflows** library type the following commands inside the conda environment:

.. code:: bash

   # Create the conda environment
   conda create -n qmflows -c conda-forge boost eigen "libint>=2.6.0" highfive
   conda activate qmflows

   # Clone the repo
   git clone https://github.com/SCM-NV/nano-qmflows
   cd nano-qmflows

   # Build and install nano-qmflows
   pip install -e . --upgrade

.. note::
   Older compilers, such as GCC <7, might not be compatible with the latest ``eigen`` version and require specification of *e.g.* ``eigen=3.3``.

Advantages and Limitations
--------------------------
nano-qmflows is based on the approximation that all excited states are represented by singly excited-state determinants. This means that the computation of the NACVs boils down to the computation of molecular orbitals (MOs) coefficients at given points of time using an electronic structure code and an overlap matrix S(t,t+dt) in atomic orbital basis (AO) computed between two consecutive time step. nano-qmflows main advantage is to use an internal module to compute efficiently the atomic overlap matrix S(t, t+dt) by employing the same basis-set used in the electronic structure calculation. In this way the QM codes are only needed to retrieve the MOs coefficients at time t and t+dt. This approach is very useful because the interfacing nano-qmflows to a QM code is reduced to writing a simple module that reads the MOs coefficients in the specific code format. At this moment, nano-qmflows handles output formats generated by CP2K, Orca, and Gamess, but, as said, it can be easily extended to other codes.

Finally, nano-qmflows can be also used in benchmarks studies to test new code developments in the field of excited state dynamics by providing a platform that uses all the functionalities of QMFlows, which automatizes the input preparation and execution of thousands of QM calculations.

In the near future, nano-qmflows is expected to offer new functionalities.


Interface to Pyxaid
-------------------

nano-qmflows has been designed mostly to be integrated with Pyxaid, a python program that performs non-adiabatic molecular dynamic (NAMD) simulations using the classical path approximation (CPA). The CPA is based on the assumption that nuclear dynamics of the system remains unaffected by the dynamics of the electronic degrees of freedom. Hence, the electronic dynamics remains driven by the ground state nuclear dynamics. CPA is usually valid for extended materials or cluster materials of nanometric size.

In this framework, nano-qmflows requires as input the coordinates of a pre-computed trajectory (at a lower level or at the same level of theory) in xyz format and the input parameters of the SCF code (HF and DFT). nano-qmflows will then calculate the overlap matrix between different MOs by correcting their phase and will also track the nature of each state at the crossing seam using a min-cost algorithm . The NACVs are computed using the Hammes-Schiffer-Tully (HST) 2-point approximation and the recent Meek-Levine approach. The NACVs are then written in Pyxaid format for subsequent NAMD simulations.


Overview
--------
 The Library contains a **C++** interface to the libint2_ library to compute the integrals and several numerical functions in Numpy_. While the scripts are set of workflows to compute different properties using different approximations that can be tuned by the user.

.. _libint2: https://github.com/evaleev/libint/wiki
.. _Numpy: http://www.numpy.org

Worflow to calculate Hamiltonians for nonadiabatic molecular simulations
************************************************************************
The figure represents schematically a Worflow to compute the **Hamiltonians** that described the behavior and coupling between the excited state of a molecular system. These **Hamiltonians** are used by thy PYXAID_ simulation package to carry out nonadiabatic molecular dynamics.

.. image:: docs/_images/nac_worflow.png

.. _PYXAID: https://www.acsu.buffalo.edu/~alexeyak/pyxaid/overview.html
.. _documentation: https://qmflows-namd.readthedocs.io/en/latest/
