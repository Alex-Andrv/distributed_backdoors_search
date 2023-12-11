#!/bin/bash -i
source activate multithreading_solver
./../kissat/build/kissat ./data/mults_inversion_cnfs/MultColumn32x32_randinp_3.cnf >> MultColumn32x32_randinp_3_kissat.log