# fodMC - Fermi-orbital descriptor Monte-Carlo 
[![license](https://img.shields.io/badge/license-APACHE2-green)](https://www.apache.org/licenses/LICENSE-2.0)
[![language](https://img.shields.io/badge/language-Fortran90-red)](https://www.fortran90.org/)
[![language](https://img.shields.io/badge/language-Python3-blue)](https://www.python.org/)
[![version](https://img.shields.io/badge/version-1.1.1-lightgrey)](https://gitlab.com/opensic/fodMC/-/blob/main/README.md)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.6326392.svg)](https://doi.org/10.5281/zenodo.6326392)


## Installation
Using pip
```bash 
$ pip3 install fodMC
```
or install locally
```bash 
$ git clone https://gitlab.com/opensic/fodMC.git
$ cd fodMC
$ pip3 install -e .
```

The Python module is called fodmc. 

## Example   
Download the CH<sub>4</sub> molecule as [3D mol](http://www.chemspider.com/Chemical-Structure.291.html) file.       
Afterwards, run the following Python script      
```python
from fodMC.pyfodmc import pyfodmc
from fodMC.pyfodmc.mol2fodmc import mol2fodmc

mol2fodmc('CH4.mol')
pyfodmc.get_guess('PyFLOSIC','CH4.xyz')
```

More examples can be found in the examples folder.


## Citation
For publications, please consider citing the following articles        

- **Interpretation and automatic generation of Fermi-orbital descriptors**         
    [S. Schwalbe et al., J. Comput. Chem. 40, 2843-2857, 2019](https://onlinelibrary.wiley.com/doi/full/10.1002/jcc.26062)

- **Chemical bonding theories as guides for self-interaction corrected solutions: multiple local minima and symmetry breaking**      
    K. Trepte, S. Schwalbe, S. Liebing, W. T. Schulze, J. Kortus, H. Myneni, A. V. Ivanov, and S. Lehtola    
    arXiv e-prints, Subject: Computational Physics (physics.comp-ph), 2021, [arXiv:2109.08199](https://arxiv.org/abs/2109.08199)     
    [J. Chem. Phys., vol. 155, no. 22, p. 224109, 2021](https://doi.org/10.1063/5.0071796)

- **Why the energy is sometimes not enough - A dive into self-interaction corrected density functional theory**     
   S. Liebing, K. Trepte, and S. Schwalbe      
    arXiv e-prints, Subject: Chemical Physics (physics.chem-ph); Computational Physics (physics.comp-ph), 2022, [arXiv:2201.11648](https://arxiv.org/abs/2201.11648)    


# ATTENTION
While the fodMC can create FODs for      
any system, we do not recommend using       
guesses for systems containing transition metals.
